import os
import shutil
import tempfile
from unittest import TestCase
from Helpers.converter import Converter
from wand.image import Image


class TestConverter(TestCase):
    tempDirPath = ""
    converterTestsResourcePath = "converter"
    converterOutputTestsResourcePath = "converterOutput"
    absolute_input_path = ""
    absolute_output_path = ""

    def setUp(self):
        self.tempDirPath = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.tempDirPath, self.converterOutputTestsResourcePath))
        shutil.copytree("./Tests/Resources/tests_converter", os.path.join(self.tempDirPath, self.converterTestsResourcePath))

        self.absolute_input_path = os.path.join(self.tempDirPath, self.converterTestsResourcePath)
        self.absolute_output_path = os.path.join(self.tempDirPath, self.converterOutputTestsResourcePath)

    def tearDown(self):
        shutil.rmtree(self.tempDirPath)

    def test_set_up(self):
        self.assertTrue(os.path.isdir(self.absolute_input_path))
        self.assertTrue(os.path.isdir(self.absolute_output_path))

        def assert_valid_eps_file(test_file_path):
            self.assertTrue(os.path.isfile(test_file_path))
            self.assertEqual(Image(filename=test_file_path).size, (100, 100))
            self.assertEqual(Image(filename=test_file_path).format, "EPT")

        for i in range(1, 3):
            assert_valid_eps_file(os.path.join(self.absolute_input_path, "test-0" + str(i) + ".eps"))

        assert_valid_eps_file(os.path.join(self.absolute_input_path, "subfolder", "test-04.eps"))
        assert_valid_eps_file(os.path.join(self.absolute_input_path, "subfolder", "subsubfolder", "test-05.eps"))


    def test_convert(self):
        converter = Converter()
        converter.inputDir = self.absolute_input_path
        converter.outputDir = self.absolute_output_path
        converter.convert()

        def assert_valid_png_file(test_file_path, size):
            self.assertTrue(os.path.isfile(test_file_path))
            self.assertEqual(Image(filename=test_file_path).size, size)
            self.assertEqual(Image(filename=test_file_path).format, "PNG")

        for i in range(1, 3):
            test_file_path_1x = os.path.join(self.absolute_output_path, "test-0" + str(i) + ".png")
            test_file_path_2x = os.path.join(self.absolute_output_path, "test-0" + str(i) + "@2x.png")
            test_file_path_3x = os.path.join(self.absolute_output_path, "test-0" + str(i) + "@3x.png")

            assert_valid_png_file(test_file_path=test_file_path_1x, size=(100, 100))
            assert_valid_png_file(test_file_path=test_file_path_2x, size=(200, 200))
            assert_valid_png_file(test_file_path=test_file_path_3x, size=(300, 300))

        assert_valid_png_file(os.path.join(self.absolute_output_path, "subfolder", "test-04.png"), (100, 100))
        assert_valid_png_file(os.path.join(self.absolute_output_path, "subfolder", "test-04@2x.png"), (200, 200))
        assert_valid_png_file(os.path.join(self.absolute_output_path, "subfolder", "test-04@3x.png"), (300, 300))

        assert_valid_png_file(os.path.join(self.absolute_output_path, "subfolder", "subsubfolder", "test-05.png"),
                              (100, 100))
        assert_valid_png_file(os.path.join(self.absolute_output_path, "subfolder", "subsubfolder", "test-05@2x.png"),
                              (200, 200))
        assert_valid_png_file(os.path.join(self.absolute_output_path, "subfolder", "subsubfolder", "test-05@3x.png"),
                              (300, 300))