import os
import io
import posixpath
import unittest
from pathlib import Path

import numpy
from drb.exceptions import DrbNotImplementationException, DrbException
from drb_impl_file import DrbFileFactory

from drb_impl_image import DrbImageFactory
from drb_impl_image.image_common import DrbImageNodesValueNames


class TestDrbListNodeImage(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))

    image_fake = current_path / "files" / "fake.tiff"
    image_tif_one = current_path / "files" / 'GeogToWGS84GeoKey5.tif'
    image_png = current_path / "files" / 'png-248x300.png'
    image_jp2 = current_path / "files" / 'relax.jp2'

    def test_list_children(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()

        tags_list = root_node.get_named_child(DrbImageNodesValueNames.META
                                              .value, occurrence=1)

        self.assertTrue(tags_list.has_child())
        self.assertIsNotNone(
            tags_list.get_named_child('transform',
                                      occurrence=1))

        self.assertIsNotNone(tags_list.get_last_child())
        root_node.close()
        node.close()

    def test_list_get_named_children(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()
        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.META.value,
            occurrence=1)

        self.assertIsNotNone(tags_list)
        with self.assertRaises(DrbException):
            tags_list.get_named_child("width", occurrence=2)

        list_children = tags_list.get_named_child("height")
        self.assertEqual(list_children[0].name, 'height')

        root_node.close()
        node.close()

    def test_list_children_get_at(self):
        node_file = DrbFileFactory().create(str(self.image_png))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()

        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.META.value,
            occurrence=1)

        self.assertEqual(tags_list.get_children_count(), 8)

        self.assertIsNotNone(tags_list.get_first_child())
        self.assertIsNotNone(tags_list.get_last_child())

        with self.assertRaises(DrbException):
            tags_list.get_child_at(8)
        with self.assertRaises(DrbException):
            tags_list.get_child_at(-9)

        self.assertEqual(tags_list.get_child_at(-1),
                         tags_list.get_last_child())

        with self.assertRaises(DrbException):
            tags_list.get_named_child("toto")

        self.assertEqual(len(tags_list.children), 8)
        self.assertTrue(tags_list.has_child())
        root_node.close()
        node.close()
        node_file.close()

    def test_list_parent(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))
        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()
        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.TAGS.value,
            occurrence=1)
        self.assertEqual(tags_list.parent, root_node)
        self.assertEqual(tags_list.name, DrbImageNodesValueNames.TAGS.value)

        root_node.close()

        node.close()

    def test_list_remove_add_attributes(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()

        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.TAGS.value,
            occurrence=1)
        with self.assertRaises(NotImplementedError):
            tags_list.add_attribute("toto")
        with self.assertRaises(NotImplementedError):
            tags_list.remove_attribute("toto")

        root_node.close()

        node.close()

    def test_list_namespace_uri(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()

        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.TAGS.value,
            occurrence=1)
        self.assertIsNone(tags_list.namespace_uri)
        root_node.close()
        node.close()

    def test_list_value(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()

        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.TAGS.value,
            occurrence=1)

        self.assertIsNone(tags_list.value)
        root_node.close()

        node.close()

    def test_list_impl_not_supported(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()

        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.TAGS.value,
            occurrence=1)

        self.assertFalse(tags_list.has_impl(io.BufferedIOBase))
        self.assertFalse(tags_list.has_impl(numpy.ndarray))

        with self.assertRaises(DrbNotImplementationException):
            tags_list.get_impl(io.BufferedIOBase)
        root_node.close()

        node.close()

    def test_list_no_attributes(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()

        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.TAGS.value,
            occurrence=1)
        self.assertFalse(bool(tags_list.attributes))
        with self.assertRaises(DrbException):
            tags_list.get_attribute('toto', None)
        root_node.close()
        node.close()

    def test_path(self):
        node_file = DrbFileFactory().create(str(self.image_tif_one))

        node = DrbImageFactory().create(node_file)
        root_node = node.get_first_child()
        tags_list = root_node.get_named_child(
            DrbImageNodesValueNames.META.value,
            occurrence=1)

        self.assertEqual(tags_list.path.path,
                         str(self.image_tif_one) + posixpath.sep +
                         DrbImageNodesValueNames.IMAGE.value + posixpath.sep +
                         DrbImageNodesValueNames.META.value)

        root_node.close()
        node.close()
        node_file.close()
