import os
import shutil
import tempfile
from unittest import TestCase

from nose.tools import assert_raises

from wand.image import Image

from basset.exceptions import *

from basset.helpers.converter import Converter


class TestConverter(TestCase):
    temp_dir_path = ""
    converter_tests_resource_path = "converter"
    converter_output_tests_resource_path = "converterOutput"
    script_root_dir_path = ""

    @classmethod
    def setUpClass(cls):
        TestConverter.script_root_dir_path = os.getcwd()

    @classmethod
    def tearDownClass(cls):
        os.chdir(TestConverter.script_root_dir_path)

    def setUp(self):
        self.temp_dir_path = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.temp_dir_path, self.converter_output_tests_resource_path))
        shutil.copytree(os.path.join(TestConverter.script_root_dir_path, "basset/tests/Resources/tests_converter"),
                        os.path.join(self.temp_dir_path, self.converter_tests_resource_path))
        os.chdir(self.temp_dir_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir_path)

    def test_set_up(self):
        def assert_valid_eps_file(test_file_path):
            self.assertTrue(os.path.isfile(test_file_path))
            self.assertEqual(Image(filename=test_file_path).size, (100, 100))
            self.assertEqual(Image(filename=test_file_path).format, "EPT")

        for i in range(1, 3):
            assert_valid_eps_file(
                os.path.join(self.converter_tests_resource_path, "convert_test", "test-0" + str(i) + ".eps"))

        assert_valid_eps_file(
            os.path.join(self.converter_tests_resource_path, "convert_test", "subfolder", "test-04.eps"))
        assert_valid_eps_file(
            os.path.join(self.converter_tests_resource_path, "convert_test", "subfolder", "subsubfolder",
                         "test-05.eps"))

    def test_convert(self):
        converter = Converter()
        converter.inputDir = os.path.join(self.converter_tests_resource_path, "convert_test")
        converter.outputDir = self.converter_output_tests_resource_path
        converter.convert()

        def assert_valid_png_file(test_file_path, size):
            self.assertTrue(os.path.isfile(test_file_path))
            self.assertEqual(Image(filename=test_file_path).size, size)
            self.assertEqual(Image(filename=test_file_path).format, "PNG")

        for i in range(1, 3):
            test_file_path_1x = os.path.join(self.converter_output_tests_resource_path, "test-0" + str(i) + ".png")
            test_file_path_2x = os.path.join(self.converter_output_tests_resource_path, "test-0" + str(i) + "@2x.png")
            test_file_path_3x = os.path.join(self.converter_output_tests_resource_path, "test-0" + str(i) + "@3x.png")

            assert_valid_png_file(test_file_path=test_file_path_1x, size=(100, 100))
            assert_valid_png_file(test_file_path=test_file_path_2x, size=(200, 200))
            assert_valid_png_file(test_file_path=test_file_path_3x, size=(300, 300))

        assert_valid_png_file(os.path.join(self.converter_output_tests_resource_path, "subfolder", "test-04.png"),
                              (100, 100))
        assert_valid_png_file(os.path.join(self.converter_output_tests_resource_path, "subfolder", "test-04@2x.png"),
                              (200, 200))
        assert_valid_png_file(os.path.join(self.converter_output_tests_resource_path, "subfolder", "test-04@3x.png"),
                              (300, 300))

        assert_valid_png_file(
            os.path.join(self.converter_output_tests_resource_path, "subfolder", "subsubfolder", "test-05.png"),
            (100, 100))
        assert_valid_png_file(
            os.path.join(self.converter_output_tests_resource_path, "subfolder", "subsubfolder", "test-05@2x.png"),
            (200, 200))
        assert_valid_png_file(
            os.path.join(self.converter_output_tests_resource_path, "subfolder", "subsubfolder", "test-05@3x.png"),
            (300, 300))

    def test_clear_output_directory_before_conversion(self):
        dummy_file_path = os.path.join(self.converter_output_tests_resource_path, "dummy.file")
        open(dummy_file_path, 'a').close()
        self.assertTrue(os.path.isfile(dummy_file_path))

        converter = Converter()
        converter.inputDir = os.path.join(self.converter_tests_resource_path, "convert_test")
        converter.outputDir = self.converter_output_tests_resource_path
        converter.convert()

        self.assertFalse(os.path.isfile(dummy_file_path))

    def test_should_raise_exception_with_assets_dir_not_present(self):
        converter = Converter()
        os.chdir(os.path.join(self.converter_tests_resource_path, "suggest_asset_diretory_test"))
        converter.inputDir = "FaceAssetsDir"
        converter.outputDir = self.converter_output_tests_resource_path

        try:
            converter.convert()
            self.fail("This should fail")
        except AssetsDirNotFoundException as e:
            self.assertEqual(e.asset_dir_candidate, "Vector_assets")

    def test_should_raise_exception_with_empty_parameter_if_no_vector_files_found(self):
        converter = Converter()
        os.chdir(os.path.join(self.converter_tests_resource_path, "suggest_asset_diretory_test", "Images.xcassets"))
        converter.inputDir = "FaceAssetsDir"
        converter.outputDir = self.converter_output_tests_resource_path

        try:
            converter.convert()
            self.fail("This should fail")
        except AssetsDirNotFoundException as e:
            self.assertEqual(e.asset_dir_candidate, None)