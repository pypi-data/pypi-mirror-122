import os
import unittest
from drb import DrbNode
from drb_impl_file import DrbFileNode, DrbFileFactory
from drb_impl_file.execptions import DrbFileNodeFactoryException


class TestDrbFileFactory(unittest.TestCase):
    def test_valid(self):
        factory = DrbFileFactory()
        cwd = os.getcwd()
        self.assertTrue(factory.valid(f'file://{cwd}'))
        self.assertTrue(factory.valid(cwd))
        self.assertTrue(factory.valid('.'))
        self.assertFalse(factory.valid('https://www.gael-systems.com'))

    def test_create(self):
        factory = DrbFileFactory()
        node = factory.create('.')
        self.assertIsInstance(node, (DrbFileNode, DrbNode))
        self.assertEqual(os.path.basename(os.getcwd()), node.name)

        with self.assertRaises(DrbFileNodeFactoryException):
            factory.create('/foo/bar/foobar.test.dat')

    def test_created_node(self):
        node = DrbFileFactory().create('.')
        self.assertIsInstance(node, (DrbFileNode, DrbNode))
