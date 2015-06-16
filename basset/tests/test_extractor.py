import tempfile

from unittest import TestCase
import shutil

from nose.tools import assert_raises

from basset.exceptions import *
from basset.helpers.converter import Converter
from basset.helpers.extractor import Extractor


class TestExtractor(TestCase):
    temp_dir_path = ""
    script_root_dir_path = ""
    resources_path = "extractor"

    @classmethod
    def setUpClass(cls):
        TestExtractor.script_root_dir_path = os.getcwd()

    @classmethod
    def tearDownClass(cls):
        os.chdir(TestExtractor.script_root_dir_path)

    def setUp(self):
        self.temp_dir_path = tempfile.mkdtemp()
        shutil.copytree(
            os.path.join(TestExtractor.script_root_dir_path, "basset/tests/Resources/tests_extractor"),
            os.path.join(self.temp_dir_path, self.resources_path))
        os.chdir(self.temp_dir_path)
        pass

    def tearDown(self):
        pass
        shutil.rmtree(self.temp_dir_path)

    def test_should_raise_exception_when_input_dir_is_not_xcassets(self):
        extractor = Extractor()
        extractor.input_dir = os.path.join("non_xcassets_directory_set_test", "assets")
        assert_raises(ExtractDirIsNotXcassetsDirException, extractor.extract)

    def test_move_all_assets_to_output_dir_and_delete_from_input(self):
        extractor = Extractor()
        extractor.input_dir = os.path.join(self.resources_path, "extract_test", "Images.xcassets")
        extractor.output_dir = "output"

        original_files = []
        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "test-01.imageset", "test-01.png")))
        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "test-01.imageset", "test-01@2x.png")))
        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "test-01.imageset", "test-01@3x.png")))

        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "test-02.imageset", "test-02.png")))
        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "test-02.imageset", "test-02@2x.png")))
        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "test-02.imageset", "test-02@3x.png")))

        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "folder", "test-03.imageset", "test-03.png")))
        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "folder", "test-03.imageset", "test-03@2x.png")))
        original_files.append(Converter.sha1_of_file(os.path.join(extractor.input_dir, "folder", "test-03.imageset", "test-03@3x.png")))

        extractor.extract()

        output_files = []
        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "test-01.png")))
        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "test-01@2x.png")))
        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "test-01@3x.png")))

        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "test-02.png")))
        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "test-02@2x.png")))
        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "test-02@3x.png")))

        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "folder", "test-03.png")))
        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "folder", "test-03@2x.png")))
        output_files.append(Converter.sha1_of_file(os.path.join(extractor.output_dir, "folder", "test-03@3x.png")))

        self.assertFalse(os.path.isdir(os.path.join(extractor.input_dir, "test-01.imageset")))
        self.assertFalse(os.path.isdir(os.path.join(extractor.input_dir, "test-02.imageset")))
        self.assertFalse(os.path.isdir(os.path.join(extractor.input_dir, "folder", "test-03.imageset")))
        self.assertEqual(original_files, output_files)
