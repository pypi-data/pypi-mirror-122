import io
import os
import stat
import enum
from urllib.parse import urlparse
from typing import Any, List, Dict, Optional, Tuple

from drb import DrbNode
from drb.factory import DrbFactory
from drb.exceptions import DrbNotImplementationException
from drb.factory.factory import DrbFactoryCategory
from drb.path import ParsedPath
from drb.utils.logical_node import DrbLogicalNode
from .execptions import DrbFileNodeException, DrbFileNodeFactoryException


class DrbFileAttributeNames(enum.Enum):
    DIRECTORY = 'directory'
    SIZE = 'size'
    MODIFIED = 'modified'
    READABLE = 'readable'
    WRITABLE = 'writable'
    HIDDEN = 'hidden'


def is_hidden(path: str) -> bool:
    """
    Check if the associated file of the given path is hidden.
    :param path: file path to check
    :return: True if the file of the corresponding path is hidden
    :rtype: bool
    """
    # os_type = 'Linux' | 'Windows' | 'Java'
    os_type = os.uname()[0]
    if os_type == 'Windows':
        return bool(os.stat(path).st_file_attributes &
                    stat.FILE_ATTRIBUTE_HIDDEN)
    return os.path.basename(path).startswith('.')


def impl_stream(path: str) -> io.FileIO:
    return io.FileIO(path, 'r+')


def impl_buffered_stream(path: str) -> io.BufferedReader:
    return io.BufferedReader(impl_stream(path))


class DrbFileNode(DrbLogicalNode):
    supported_impl = {
        io.RawIOBase: impl_stream,
        io.FileIO: impl_stream,
        io.BufferedIOBase: impl_buffered_stream,
        io.BufferedReader: impl_buffered_stream,
    }

    def __init__(self, path, parent: DrbNode = None):
        if isinstance(path, ParsedPath):
            source = path
        else:
            source = os.path.abspath(path)
        DrbLogicalNode.__init__(self, source=source)
        self._parent: DrbNode = parent

    @property
    def parent(self) -> Optional[DrbNode]:
        if self._parent is None:
            parent_path = os.path.dirname(self.path.path)
            if parent_path != self.path.path:
                self._parent = DrbFileNode(parent_path)
        return self._parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            file_stat = os.stat(self.path.path)
            name = DrbFileAttributeNames.DIRECTORY.value
            self._attributes[(name, None)] = os.path.isdir(self.path.path)

            name = DrbFileAttributeNames.SIZE.value
            self._attributes[(name, None)] = file_stat.st_size

            name = DrbFileAttributeNames.MODIFIED.value
            self._attributes[(name, None)] = file_stat.st_mtime

            name = DrbFileAttributeNames.READABLE.value
            self._attributes[(name, None)] = os.access(self.path.path, os.R_OK)

            name = DrbFileAttributeNames.WRITABLE.value
            self._attributes[(name, None)] = os.access(self.path.path, os.W_OK)

            name = DrbFileAttributeNames.HIDDEN.value
            self._attributes[(name, None)] = is_hidden(self.path.path)

        return self._attributes

    @property
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            if os.path.isdir(self.path.path):
                sorted_child_names = sorted(os.listdir(self.path.path))
                for filename in sorted_child_names:
                    child = DrbFileNode(self.path / filename,
                                        parent=self)
                    self._children.append(child)
        return self._children

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        raise NotImplementedError

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        raise NotImplementedError

    def has_impl(self, impl: type) -> bool:
        if impl in DrbFileNode.supported_impl.keys():
            return not self.get_attribute(
                DrbFileAttributeNames.DIRECTORY.value)

    def get_impl(self, impl: type) -> Any:
        try:
            return DrbFileNode.supported_impl[impl](self.path.path)
        except KeyError:
            raise DrbNotImplementationException(
                f'no {impl} implementation found')


class DrbFileFactory(DrbFactory):

    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.PROTOCOL

    def valid(self, uri: str) -> bool:
        parsed_uri = urlparse(uri)
        if parsed_uri.scheme == 'file' or parsed_uri.scheme == '':
            return True
        return False

    def _create_from_uri_of_node(self, node: DrbNode):
        uri = node.path.name
        if not self.valid(uri):
            raise DrbFileNodeException(f'factory cannot open: {uri}')
        parsed_uri = urlparse(uri)
        if os.path.exists(parsed_uri.path):
            return DrbFileNode(parsed_uri.path, node)
        raise DrbFileNodeFactoryException(f'File not found: {parsed_uri.path}')

    def _create(self, node: DrbNode) -> DrbNode:
        return self._create_from_uri_of_node(node)
