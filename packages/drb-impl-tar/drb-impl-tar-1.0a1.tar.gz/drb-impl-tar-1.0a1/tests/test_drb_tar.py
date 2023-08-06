import os
import posixpath
import unittest
from pathlib import Path

from drb.exceptions import DrbException
from drb_impl_file import DrbFileFactory
from drb_impl_file.drb_impl_file import DrbFileAttributeNames
from drb_impl_tar.execptions import DrbTarNodeException
from drb_impl_tar.file_tar_node import DrbTarFactory
from drb_impl_tar.tar_node import DrbTarAttributeNames

LONG_DIR = "veryveryveryveryveryveryveryveryveryveryveryveryveryvery"\
           "veryveryveryveryveryveryLongDir"

T____ANNOTATION_DAT = "S2A_OPER_PRD_HKTM___20191121T080247_20191121T080252"\
                      "_0001_annotation.dat"

T____SAFE = "S2A_OPER_PRD_HKTM___20191121T080247_20191121T080252_0001.SAFE"

T__HDR_XML = "S2__OPER_AUX_ECMWFD_PDMC_20190216T120000_V20190217T090000_" \
              "20190217T210000.HDR.xml"


class TestDrbZipFactory(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    tar_test = current_path / "files" / "test.tar"
    tar_gnu = current_path / "files" / "gnu.tar"
    tar_old_gnu = current_path / "files" / "oldgnu.tar"
    tar_posix = current_path / "files" / "posix.tar"
    tar_ustar = current_path / "files" / "ustar.tar"
    tar_v7 = current_path / "files" / "v7.tar"
    tar_file_long_names = current_path / "files" / "test_long_file.tar"
    tar_absolute_path = current_path / "files" / "test_absolute_path.tar"
    tar_relative_path = current_path / "files" / "test_relative_path.tar"
    tar_confuse_name = current_path / "files" / "tar_with_confuse_names.tar"
    empty_file = current_path / "files" / "empty.file"
    tar_fake = current_path / "files" / "fake.tar"
    node = None
    node_file = None

    def setUp(self) -> None:
        self.node = None
        self.node_file = None

    def tearDown(self) -> None:
        if self.node is not None:
            self.node.close()
        if self.node_file is not None:
            self.node_file.close()

    def open_node(self, path_file):
        self.node_file = DrbFileFactory().create(path_file)
        self.node = DrbTarFactory().create(self.node_file)
        return self.node

    def test_Valid(self):
        self.assertTrue(DrbTarFactory().valid(str(self.tar_test)))

    def test_not_Valid(self):
        self.assertFalse(DrbTarFactory().valid(str(self.empty_file)))

    def check_test_tar(self, node):
        self.assertTrue(node.has_child())

        self.assertIsNotNone(node.get_named_child("test", occurrence=1))
        self.assertIsNotNone(
            node.get_named_child("test", occurrence=1).get_named_child(
                "empty.file", occurrence=1))
        self.assertIsNotNone(
            node.get_named_child("test", occurrence=1).get_named_child(
                "not-empty.file", occurrence=1))
        self.assertIsNotNone(
            node.get_named_child("test", occurrence=1)
                .get_named_child("a", occurrence=1))
        self.assertIsNotNone(
            node.get_named_child("test", occurrence=1)
                .get_named_child("a", occurrence=1)
                .get_named_child("aaa.txt", occurrence=1))

        with self.assertRaises(DrbException):
            node.get_named_child("test", occurrence=1).\
                get_named_child("aa", occurrence=1)
        with self.assertRaises(DrbException):
            node.get_named_child("test", occurrence=1).\
                get_named_child("a", occurrence=1).\
                get_named_child("aaa.tx", occurrence=1)

        self.assertIsNotNone(
            node.get_named_child("test", occurrence=1)
                .get_named_child("b", occurrence=1)
                .get_named_child("bbb.txt", occurrence=1))

        with self.assertRaises(DrbException):
            node.get_named_child("test", occurrence=1).\
                get_named_child("a", occurrence=1).\
                get_named_child("bbb.tx", occurrence=1)
        with self.assertRaises(DrbException):
            node.get_named_child("test", occurrence=1).\
                get_named_child("b", occurrence=1).\
                get_named_child("aaa.tx", occurrence=1)

    def test_opened_file_node(self):
        node = self.open_node(str(self.tar_test))
        self.assertEqual(node.name, "test.tar")

        self.check_test_tar(node)

    def test_fake(self):
        node = self.open_node(str(self.tar_fake))

        self.assertEqual(node.name, "fake.tar")

        with self.assertRaises(DrbTarNodeException):
            node.get_children_count()

    def test_confuse_name(self):
        node = self.open_node(str(self.tar_confuse_name))

        self.check_test_tar(node)

        self.assertEqual(node.get_child_at(0)._tar_info.name, "test")

        self.assertEqual(
            node.get_named_child("test", occurrence=1).get_children_count(), 8)

        self.assertIsNotNone(
            node.get_named_child("test", occurrence=1).get_named_child(
                "xm", occurrence=1))
        self.assertFalse(
                node.get_named_child("test", occurrence=1).get_named_child(
                    "xm")[0].has_child())
        self.assertTrue(
            node.get_named_child("test", occurrence=1).get_named_child(
                "xml")[0].has_child())

        self.assertEqual(
            node.get_named_child("test", occurrence=1).get_named_child(
                "xml")[0].get_children_count(), 2)

        self.assertIsNotNone(
            node.get_named_child("test", occurrence=1).get_named_child(
                "not-empty", occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child("test", occurrence=1).\
                get_named_child("not-empty", occurrence=2)
        self.assertFalse(
            node.get_named_child("test", occurrence=1).get_named_child(
                "not-empty")[0].has_child())

        self.assertEqual(node.get_child_at(0)._tar_info.name, "test")

    def test_absolute_path(self):
        node = self.open_node(str(self.tar_absolute_path))

        self.assertTrue(node.has_child())

        self.assertEqual(node.get_child_at(0).name, "test")
        self.assertEqual(node.get_child_at(0)._tar_info.name, "/tmp/test")

    def test_relative_path(self):
        node = self.open_node(str(self.tar_relative_path))

        self.assertTrue(node.has_child())

        self.assertEqual(node.get_child_at(0).name, "test")
        self.assertEqual(node.get_child_at(0)._tar_info.name, "tmp/test")

        self.check_test_tar(node)

    def chack_small_name_tar(self, first_node):
        self.assertTrue(first_node.has_child())
        self.assertIsNotNone(
            first_node.get_named_child("SMALL_NAME", occurrence=1))
        node = first_node.get_named_child("SMALL_NAME", occurrence=1)
        self.assertIsNotNone(node.get_named_child(
            T__HDR_XML,
            occurrence=1))
        self.assertIsNotNone(node.get_named_child(
            "S2__OPER_AUX_ECMWFD_PDMC_20190216T120000_V20190217T090000"
            "_20190217T210000.DBL",
            occurrence=1))

        with self.assertRaises(DrbException):
            node.get_named_child(
                "S2__OPER_AUX_ECMWFD_PDMC_20190216T120000_V20190217T090000"
                "_20190217T210000.DBL",
                occurrence=2)

        # TODO mix XML and Tar ....
        # node_xml = node.get_named_child(
        # "S2__OPER_AUX_ECMWFD_PDMC_20190216T120000_V20190217T090000"
        # "_20190217T210000.HDR.xml", occurrence=1)
        # self.assertIsNotNone(node_xml.get_named_child(
        # "Earth_Explorer_Header", occurrence=1))

        self.assertEqual(node.get_children_count(), 2)

        list_node = node.get_named_child(
            T__HDR_XML)
        self.assertEqual(len(list_node), 1)
        self.assertEqual(list_node[0].name,
                         T__HDR_XML)

    def test_gnu_tar(self):
        first_node = self.open_node(str(self.tar_gnu))

        self.chack_small_name_tar(first_node)

    def test_old_gnu_tar(self):
        first_node = self.open_node(str(self.tar_old_gnu))

        self.chack_small_name_tar(first_node)

    def test_posix_tar(self):
        first_node = self.open_node(str(self.tar_posix))

        self.chack_small_name_tar(first_node)

    def test_ustar_tar(self):
        first_node = self.open_node(str(self.tar_ustar))

        self.chack_small_name_tar(first_node)

    def test_v7_tar(self):
        first_node = self.open_node(str(self.tar_v7))

        self.chack_small_name_tar(first_node)

    def test_file_long_names(self):
        first_node = self.open_node(str(self.tar_file_long_names))

        self.assertIsNotNone(first_node.get_named_child(T____SAFE,
                                                        occurrence=1))
        node = first_node.get_named_child(T____SAFE, occurrence=1)

        self.assertIsNotNone(node.get_named_child(T____ANNOTATION_DAT,
                                                  occurrence=1))

        self.assertIsNotNone(first_node.get_named_child(T____SAFE,
                                                        occurrence=1))

        node = first_node.get_named_child(T____SAFE, occurrence=1)

        for index in range(2):
            self.assertIsNotNone(node.get_named_child(LONG_DIR, occurrence=1))
            node = node.get_named_child(LONG_DIR, occurrence=1)
            self.assertEqual(node.name, LONG_DIR)

        # self.assertIsNotNone(node.get_named_child("manifest.safe",
        #                                          occurrence=1))

    def test_get_at(self):
        node = self.open_node(str(self.tar_test))

        with self.assertRaises(DrbException):
            node.get_child_at(1)

        self.assertIsNotNone(node.get_child_at(0))
        self.assertEqual(node.get_child_at(0).get_children_count(), 5)
        node_child = node.get_child_at(0).get_child_at(0)
        self.assertEqual(node_child.name, "a")
        node_child = node.get_child_at(0).get_child_at(1)
        self.assertEqual(node_child.name, "b")
        node_child = node.get_child_at(0).get_child_at(2)
        self.assertEqual(node_child.name, "empty.file")
        node_child = node.get_child_at(0).get_child_at(3)
        self.assertEqual(node_child.name, "not-empty.file")
        node_child = node.get_child_at(0).get_child_at(4)
        self.assertEqual(node_child.name, "xml")
        node_child = node.get_child_at(0).get_child_at(-5)
        self.assertEqual(node_child.name, "a")

        with self.assertRaises(DrbException):
            node.get_child_at(0).get_child_at(5)
        with self.assertRaises(DrbException):
            node.get_child_at(0).get_child_at(-6)

    def test_value(self):
        node = self.open_node(str(self.tar_test))

        self.assertTrue(node.get_child_at(0).has_child())

        self.assertIsNone(node.get_child_at(0).value)

    def test_namespace_uri(self):
        node = self.open_node(str(self.tar_test))

        self.assertTrue(node.get_child_at(0).has_child())

        self.assertIsNone(node.get_child_at(0).namespace_uri)

    def test_namespace_uri_file(self):
        node = self.open_node(str(self.tar_test))

        self.assertEqual(node.namespace_uri, self.node_file.namespace_uri)
        self.assertEqual(node.name, self.node_file.name)

    def test_value_file(self):
        node_file = DrbFileFactory().create(str(self.tar_test))
        node = DrbTarFactory().create(node_file)

        self.assertEqual(node.namespace_uri, node_file.namespace_uri)
        self.assertEqual(node.value, node_file.value)

    def test_first_end_child(self):
        node = self.open_node(str(self.tar_test))

        node_dir_xml = node.get_child_at(0).get_last_child()

        self.assertEqual(node_dir_xml.name, "xml")

        self.assertIsNotNone(node_dir_xml.get_first_child())
        self.assertIsNotNone(node_dir_xml.get_last_child())

        self.assertEqual(node_dir_xml.get_first_child().name, "a_xml")
        self.assertEqual(node_dir_xml.get_last_child().name, "b.xml")

        with self.assertRaises(DrbException):
            node_dir_xml.get_first_child().get_first_child()
        with self.assertRaises(DrbException):
            node_dir_xml.get_first_child().get_last_child()

    def test_attributes(self):
        first_node = self.open_node(str(self.tar_test))

        node_dir_xml = first_node.get_named_child("test", occurrence=1).\
            get_named_child("xml", occurrence=1)

        list_attributes = node_dir_xml.attributes

        self.assertIn((DrbTarAttributeNames.DIRECTORY.value, None),
                      list_attributes.keys())

        self.assertEqual(list_attributes[(DrbTarAttributeNames.DIRECTORY.value,
                                         None)], True)

        with self.assertRaises(KeyError):
            list_attributes[(DrbTarAttributeNames.DIRECTORY.value, 'test')]

    def test_get_attribute(self):
        node = self.open_node(str(self.tar_test))

        node_dir_xml = node.get_named_child("test", occurrence=1).\
            get_named_child("xml", occurrence=1)

        self.assertEqual(node_dir_xml.
                         get_attribute(DrbTarAttributeNames.SIZE.value), 0)

        self.assertEqual(node_dir_xml.
                         get_attribute(DrbTarAttributeNames.DIRECTORY.value),
                         True)

        self.assertIn("2017", node_dir_xml.
                      get_attribute(DrbTarAttributeNames.MODIFIED.value))
        self.assertIn("14", node_dir_xml.
                      get_attribute(DrbTarAttributeNames.MODIFIED.value))

        node_a_xml = node_dir_xml.get_named_child("a_xml", occurrence=1)

        self.assertEqual(node_a_xml.
                         get_attribute(DrbTarAttributeNames.SIZE.value), 44)

        self.assertEqual(node_a_xml.
                         get_attribute(DrbTarAttributeNames.DIRECTORY.value),
                         False)

    def test_attributes_zip_files(self):
        node = self.open_node(str(self.tar_test))

        list_attributes = node.attributes

        self.assertIn((DrbFileAttributeNames.DIRECTORY.value, None),
                      list_attributes.keys())

        self.assertIn((DrbFileAttributeNames.SIZE.value, None),
                      list_attributes.keys())

        self.assertEqual(node.get_attribute(
            DrbFileAttributeNames.DIRECTORY.value, None), False)

    def test_add_attribute(self):
        first_node = self.open_node(str(self.tar_test))
        first_child = first_node.get_child_at(0)

        with self.assertRaises(NotImplementedError):
            first_node.add_attribute("test")

        node = first_child
        with self.assertRaises(NotImplementedError):
            node.add_attribute("test")

    def test_remove_attribute(self):
        first_node = self.open_node(str(self.tar_test))
        first_child = first_node.get_child_at(0)

        with self.assertRaises(NotImplementedError):
            first_node.remove_attribute(DrbFileAttributeNames.DIRECTORY.value)

        node = first_child
        with self.assertRaises(NotImplementedError):
            node.remove_attribute(DrbFileAttributeNames.DIRECTORY.value)

    def test_parent(self):
        first_node = self.open_node(str(self.tar_test))

        self.assertEqual(first_node.parent, self.node_file.parent)
        self.assertEqual(first_node.value, self.node_file.value)

        first_child = first_node.get_child_at(0)
        self.assertEqual(first_child.parent, first_node)

    def test_path(self):
        first_node = self.open_node(str(self.tar_test))

        self.assertEqual(first_node.path.path, str(self.tar_test))

        node_dir_xml = first_node.get_named_child("test", occurrence=1). \
            get_named_child("xml", occurrence=1)
        self.assertEqual(node_dir_xml.path.path, str(self.tar_test) +
                         posixpath.sep + 'test' + posixpath.sep + "xml")
