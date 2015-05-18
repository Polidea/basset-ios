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

    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""

    def setUp(self):
        self.tempDirPath = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.tempDirPath, self.converterOutputTestsResourcePath))
        shutil.copytree("./Resources/tests_converter", os.path.join(self.tempDirPath, self.converterTestsResourcePath))

        self.absolute_input_path = os.path.join(self.tempDirPath, self.converterTestsResourcePath)
        self.absolute_output_path = os.path.join(self.tempDirPath, self.converterOutputTestsResourcePath)

    def teardown(self):
        shutil.rmtree(self.tempDirPath)

    def test_set_up(self):
        assert (os.path.isdir(self.absolute_input_path))
        assert (os.path.isdir(self.absolute_output_path))

        for i in range(1, 5):
            test_file_path = os.path.join(self.absolute_input_path, "test-0" + str(i) + ".eps")
            assert (os.path.isfile(test_file_path))
            self.assertEqual(Image(filename=test_file_path).size, (100, 100))
            self.assertEqual(Image(filename=test_file_path).format, "EPT")

    def test_convert(self):
        converter = Converter(self.absolute_input_path, self.absolute_output_path)
        converter.convert()

        for i in range(1, 5):
            test_file_path_1x = os.path.join(self.absolute_output_path, "test-0" + str(i) + ".png")
            test_file_path_2x = os.path.join(self.absolute_output_path, "test-0" + str(i) + "@2x.png")
            test_file_path_3x = os.path.join(self.absolute_output_path, "test-0" + str(i) + "@3x.png")

            assert (os.path.isfile(test_file_path_1x))
            assert (os.path.isfile(test_file_path_2x))
            assert (os.path.isfile(test_file_path_3x))

            self.assertEqual(Image(filename=test_file_path_1x).size, (100, 100))
            self.assertEqual(Image(filename=test_file_path_2x).size, (200, 200))
            self.assertEqual(Image(filename=test_file_path_3x).size, (300, 300))

            self.assertEqual(Image(filename=test_file_path_1x).format, "PNG")
            self.assertEqual(Image(filename=test_file_path_2x).format, "PNG")
            self.assertEqual(Image(filename=test_file_path_3x).format, "PNG")