import os
import unittest
from drb.exceptions import DrbException
from drb_impl_file import DrbFileFactory
from drb_impl_file.drb_impl_file import DrbFileAttributeNames
from drb_impl_zip import DrbZipFactory

from pathlib import Path
from drb_impl_zip.zip_node import DrbZipAttributeNames

MY_DATA1_TXT = "mydata1.txt"
MY_DATA2_TXT = "mydata2.txt"

EMPTY_DIR = "empty_dir"

ROOT_DIR_DATA = "data"

MY_DATA_TXT = "mydata.txt"

SENTINEL_1_ROOT = "sentinel-1"


class TestDrbZip(unittest.TestCase):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    zip_ok1 = current_path / "files" / "data-ok.zip"
    zip_ko1 = current_path / "files" / "data-nok.zip"

    zip_ok2 = current_path / "files" / "data-ok2.zip"
    zip_ko2 = current_path / "files" / "data-nok2.zip"
    zip_s1 = current_path / "files" / "sentinel-1.zip"
    zip_confused_names = current_path / "files" / "data-name-confused.zip"
    not_zip_files = current_path / "files" / "mydata.txt"
    file_without_ext = current_path / "files" / "wihthout_ext"

    zip_fake = current_path / "files" / "fake.zip"
    zip_case = current_path / "files" / "data-ok.ZIp"

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
        self.node = DrbZipFactory().create(self.node_file)
        return self.node

    def test_Valid(self):
        self.assertTrue(DrbZipFactory().valid(str(self.zip_ok2)))

    def test_Valid_case(self):
        self.assertTrue(DrbZipFactory().valid(str(self.zip_case)))

    def test_not_Valid(self):
        self.assertFalse(DrbZipFactory().valid(str(self.not_zip_files)))
        self.assertFalse(DrbZipFactory().valid(str(self.file_without_ext)))

    def test_opened__file_node(self):
        node = self.open_node(str(self.zip_ok1))
        self.assertIsNotNone(node.get_named_child(ROOT_DIR_DATA, occurrence=1))

    def test_fake(self):
        node = self.open_node(str(self.zip_fake))

        self.assertEqual(node.name, "fake.zip")

        with self.assertRaises(DrbException):
            node.get_children_count()

    def test_open_URL_ok1(self):
        node = self.open_node(str(self.zip_ok1))
        self.assertIsNotNone(node.get_named_child(ROOT_DIR_DATA, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=2)
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                MY_DATA_TXT, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                ROOT_DIR_DATA,
                occurrence=1)
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1)

        self.assertEqual(node.get_children_count(), 1)
        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA,
                                 occurrence=1).get_children_count(),
            1)

    def test_open_URL_ko1(self):
        node = self.open_node(str(self.zip_ok2))

        self.assertEqual(node.get_children_count(), 1)

        self.assertIsNotNone(node.get_named_child(ROOT_DIR_DATA, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(MY_DATA_TXT, occurrence=1)
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                ROOT_DIR_DATA,
                occurrence=1)
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                MY_DATA_TXT, occurrence=1))

    def test_open_URL_ok2(self):
        node = self.open_node(str(self.zip_ok2))

        self.assertIsNotNone(node.get_named_child(ROOT_DIR_DATA, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=2)
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                MY_DATA_TXT, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                ROOT_DIR_DATA,
                occurrence=1)

        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1))
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=2)

        self.assertEqual(node.get_children_count(), 1)
        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA,
                                 occurrence=1).get_children_count(),
            2)
        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_children_count(),
            1)
        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                MY_DATA_TXT,
                occurrence=1).get_children_count(),
            0)

        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1).get_children_count(), 2)
        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1).get_children_count(), 2)
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1).get_named_child(MY_DATA1_TXT,
                                                         occurrence=1))
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1).get_named_child(MY_DATA2_TXT,
                                                         occurrence=1))

    def test_open_URL_ko2(self):
        node = self.open_node(str(self.zip_ok2))

        self.assertIsNotNone(node.get_named_child(ROOT_DIR_DATA, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=2)
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                MY_DATA_TXT, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                ROOT_DIR_DATA,
                occurrence=1)

        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1))
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=2)

        self.assertEqual(node.get_children_count(), 1)
        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA,
                                 occurrence=1).get_children_count(),
            2)
        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_children_count(),
            1)
        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                MY_DATA_TXT,
                occurrence=1).get_children_count(),
            0)

        self.assertEqual(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1).get_children_count(), 2)
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1).get_named_child(MY_DATA1_TXT,
                                                         occurrence=1))
        self.assertIsNotNone(
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1).get_named_child(MY_DATA2_TXT,
                                                         occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=1).get_named_child(
                EMPTY_DIR,
                occurrence=1).get_named_child(
                EMPTY_DIR, occurrence=1).get_named_child("mydata3.txt",
                                                         occurrence=1)

    def test_first_end_child(self):
        node = self.open_node(str(self.zip_ok2))

        self.assertEqual(node.get_children_count(), 1)
        self.assertIsNotNone(node.get_first_child())

        self.assertEqual(node.get_first_child().name, ROOT_DIR_DATA)
        self.assertEqual(node.get_last_child().name, ROOT_DIR_DATA)

        self.assertEqual(node.get_first_child().get_first_child().name,
                         EMPTY_DIR)
        self.assertEqual(node.get_first_child().get_last_child().name,
                         MY_DATA_TXT)

        with self.assertRaises(DrbException):
            node.get_first_child().get_last_child().get_first_child()
        with self.assertRaises(DrbException):
            node.get_first_child().get_last_child().get_last_child()

        self.assertEqual(node.get_first_child().get_named_child(EMPTY_DIR,
                                                                occurrence=1)
                         .get_first_child().name,
                         EMPTY_DIR)
        self.assertEqual(node.get_first_child().get_named_child(EMPTY_DIR,
                                                                occurrence=1)
                         .get_last_child().name,
                         EMPTY_DIR)

        self.assertEqual(
            node.get_first_child().get_first_child().get_last_child()
                .get_first_child().name, MY_DATA1_TXT)
        self.assertEqual(
            node.get_first_child().get_first_child().get_last_child()
                .get_last_child().name, MY_DATA2_TXT)

    def test_get_named_child_without_occurrence(self):
        node = self.open_node(str(self.zip_ok2))

        list_occurrence = node.get_named_child(
            ROOT_DIR_DATA, occurrence=1).get_named_child(EMPTY_DIR)
        self.assertEqual(len(list_occurrence), 1)
        self.assertEqual(list_occurrence[0].name, EMPTY_DIR)
        list_occurrence_bis = list_occurrence[0].get_named_child(EMPTY_DIR)
        self.assertEqual(len(list_occurrence_bis), 1)
        self.assertEqual(list_occurrence_bis[0].name, EMPTY_DIR)

    def test_has_child(self):
        node = self.open_node(str(self.zip_ok2))

        self.assertTrue(node.get_first_child().has_child())
        self.assertTrue(
            node.get_first_child().get_named_child(EMPTY_DIR,
                                                   occurrence=1).has_child())
        self.assertTrue(
            node.get_first_child().get_named_child(EMPTY_DIR, occurrence=1)
                .get_named_child(EMPTY_DIR, occurrence=1).has_child())
        self.assertFalse(
            node.get_first_child().get_first_child().get_last_child()
                .get_last_child().has_child())

    def test_get_child_at(self):
        node = self.open_node(str(self.zip_ok2))

        self.assertTrue(node.get_child_at(0).has_child())

        self.assertEqual(node.get_child_at(0).get_child_at(0).name, EMPTY_DIR)
        self.assertEqual(node.get_child_at(0).get_child_at(0).get_child_at(0).
                         get_child_at(0).name, MY_DATA1_TXT)
        self.assertEqual(node.get_child_at(0).get_child_at(0).get_child_at(0).
                         get_child_at(1).name, MY_DATA2_TXT)
        with self.assertRaises(DrbException):
            node.get_child_at(0).get_child_at(0).get_child_at(0).\
                get_child_at(3)

        self.assertEqual(node.get_child_at(0).get_child_at(0).get_child_at(0)
                         .get_child_at(-1).name, MY_DATA2_TXT)

    def test_namespace_uri(self):
        node = self.open_node(str(self.zip_ok2))

        self.assertTrue(node.get_child_at(0).has_child())
        self.assertIsNone(node.get_child_at(0).namespace_uri)

    def test_value_uri(self):
        node = self.open_node(str(self.zip_ok2))

        self.assertTrue(node.get_child_at(0).has_child())
        self.assertIsNone(node.get_child_at(0).value)

    def test_test_namespace_uri_file(self):
        node = self.open_node(str(self.zip_ok1))

        self.assertEqual(node.namespace_uri, self.node_file.namespace_uri)
        self.assertEqual(node.name, self.node_file.name)

    def test_value_file(self):
        node = self.open_node(str(self.zip_ok1))

        self.assertEqual(node.namespace_uri, self.node_file.namespace_uri)
        self.assertEqual(node.value, self.node_file.value)

    def test_attributes_zip_files(self):
        node = self.open_node(str(self.zip_s1))

        list_attributes = node.attributes
        self.assertIn((DrbFileAttributeNames.DIRECTORY.value, None),
                      list_attributes.keys())
        self.assertIn((DrbFileAttributeNames.SIZE.value, None),
                      list_attributes.keys())
        self.assertEqual(node.get_attribute(
            DrbFileAttributeNames.DIRECTORY.value, None), False)

    def test_attributes(self):
        node = self.open_node(str(self.zip_s1))

        self.assertIsNotNone(node.get_named_child(
            SENTINEL_1_ROOT, occurrence=1).attributes)
        list_attributes = node.get_named_child(
            SENTINEL_1_ROOT, occurrence=1).attributes
        self.assertIn((DrbZipAttributeNames.DIRECTORY.value, None),
                      list_attributes.keys())
        self.assertEqual(list_attributes[(DrbZipAttributeNames.DIRECTORY.value,
                                         None)], True)

        with self.assertRaises(KeyError):
            list_attributes[(DrbZipAttributeNames.DIRECTORY.value, 'toto')]

    def test_get_attribute(self):
        node = self.open_node(str(self.zip_s1))

        self.assertIsNotNone(node.get_named_child(SENTINEL_1_ROOT,
                             occurrence=1).get_attribute(DrbZipAttributeNames.
                                                         DIRECTORY.value))
        self.assertEqual(node.get_named_child(SENTINEL_1_ROOT, occurrence=1).
                         get_attribute(DrbZipAttributeNames.DIRECTORY.value),
                         True)

        self.assertEqual(node.get_named_child(SENTINEL_1_ROOT, occurrence=1)
                         .get_named_child("manifest.safe", occurrence=1).
                         get_attribute(DrbZipAttributeNames.DIRECTORY.value),
                         False)

        self.assertEqual(node.get_named_child(SENTINEL_1_ROOT, occurrence=1)
                         .get_named_child("manifest.safe", occurrence=1)
                         .get_attribute(DrbZipAttributeNames.SIZE.value),
                         14945)
        self.assertAlmostEqual(node.get_named_child(SENTINEL_1_ROOT,
                                                    occurrence=1)
                               .get_named_child("manifest.safe", occurrence=1)
                               .get_attribute(
                                    DrbZipAttributeNames.RATIO.value, None),
                               4.9, delta=0.1)
        self.assertAlmostEqual(node.get_named_child(SENTINEL_1_ROOT,
                                                    occurrence=1)
                               .get_named_child("manifest.safe", occurrence=1)
                               .get_attribute(DrbZipAttributeNames.PACKED.
                                              value),
                               3014, delta=10)
        self.assertEqual(node.get_named_child(SENTINEL_1_ROOT, occurrence=1)
                         .get_named_child("measurement", occurrence=1).
                         get_attribute(DrbZipAttributeNames.SIZE.value),
                         0)
        self.assertEqual(node.get_named_child(SENTINEL_1_ROOT, occurrence=1)
                         .get_named_child("measurement", occurrence=1).
                         get_attribute(DrbZipAttributeNames.RATIO.value),
                         0)
        self.assertEqual(node.get_named_child(SENTINEL_1_ROOT, occurrence=1)
                         .get_named_child("measurement", occurrence=1).
                         get_attribute(DrbZipAttributeNames.PACKED.value),
                         0)

    def test_open_name_confused(self):
        node = self.open_node(str(self.zip_confused_names))

        self.assertIsNotNone(node.get_named_child(ROOT_DIR_DATA, occurrence=1))
        with self.assertRaises(DrbException):
            node.get_named_child(ROOT_DIR_DATA, occurrence=2)

        first_node = node.get_named_child(ROOT_DIR_DATA, occurrence=1)
        self.assertEqual(first_node.get_children_count(), 6)

        node_file = first_node.get_named_child(MY_DATA_TXT, occurrence=1)
        self.assertFalse(node_file.has_child())
        self.assertEqual(node_file.get_children_count(), 0)

        node_dir = first_node.get_named_child("mydata", occurrence=1)
        self.assertEqual(node_dir.get_children_count(), 2)
        self.assertTrue(node_dir.has_child())

        node_dir = first_node.get_named_child("myd", occurrence=1)
        self.assertEqual(node_dir.get_children_count(), 1)
        self.assertTrue(node_dir.has_child())

        node_dir = first_node.get_named_child("mydata_empty", occurrence=1)
        self.assertEqual(node_dir.get_children_count(), 0)
        self.assertFalse(node_dir.has_child())

        node_file = first_node.get_named_child("my", occurrence=1)
        self.assertFalse(node_file.has_child())
        self.assertEqual(node_file.get_children_count(), 0)

        node_file = first_node.get_named_child("mydata_txt", occurrence=1)
        self.assertFalse(node_file.has_child())
        self.assertEqual(node_file.get_children_count(), 0)
        self.assertEqual(node_file.name, "mydata_txt")

    def test_parent(self):
        first_node = self.open_node(str(self.zip_ok2))

        self.assertEqual(first_node.parent, self.node_file.parent)
        self.assertEqual(first_node.value, self.node_file.value)

        first_child = first_node.get_child_at(0)
        self.assertEqual(first_child.parent, first_node)

    def test_path(self):
        first_node = self.open_node(str(self.zip_ok2))

        self.assertEqual(str(first_node.path.name), str(self.zip_ok2))

        first_child = first_node.get_child_at(0)
        path_child = str(self.zip_ok2) + '/' + first_child.name
        self.assertEqual(str(first_child.path.name), path_child)
