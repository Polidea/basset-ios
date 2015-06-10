import os
import shutil
import tempfile
from unittest import TestCase

from basset.exceptions import *
from basset.helpers.configuration_manager import ConfigurationManager


class TestConfigurationManager(TestCase):
    temp_dir_path = ""
    config_files_path = "configs"
    sample_xcassets_dir = "sample_xcassets_dir"
    sample_raw_assets_dir = "sample_raw_assets_dir"
    sample_generated_assets_dir = "sample_generated_assets_dir"
    sample_merge_with = "sample_merge_with_xcassets"
    sample_force_convert = "sample_force_convert"

    def setUp(self):
        self.temp_dir_path = tempfile.mkdtemp()
        shutil.copytree("basset/tests/Resources/tests_configuration_manager",
                        os.path.join(self.temp_dir_path, self.config_files_path))

    def tearDown(self):
        shutil.rmtree(self.temp_dir_path)

    def test_if_parameters_are_processed_to_configuration_object(self):
        configuration = ConfigurationManager.get_configuration(xcassets_dir=self.sample_xcassets_dir,
                                                               raw_assets=self.sample_raw_assets_dir,
                                                               generated_assets_dir=self.sample_generated_assets_dir,
                                                               merge_with_xcassets=self.sample_merge_with,
                                                               force_convert=self.sample_force_convert,
                                                               config_file_path=None)

        self.assertTrue(configuration.xcassets_dir == self.sample_xcassets_dir)
        self.assertTrue(configuration.raw_assets == self.sample_raw_assets_dir)
        self.assertTrue(configuration.generated_assets_dir == self.sample_generated_assets_dir)
        self.assertTrue(configuration.merge_with_xcassets == self.sample_merge_with)

    def test_using_config_file(self):
        configuration = ConfigurationManager.get_configuration(xcassets_dir=self.sample_xcassets_dir,
                                                               raw_assets=self.sample_raw_assets_dir,
                                                               generated_assets_dir=self.sample_generated_assets_dir,
                                                               merge_with_xcassets=self.sample_merge_with,
                                                               force_convert=self.sample_force_convert,
                                                               config_file_path=os.path.join(self.config_files_path,
                                                                                             os.path.join(
                                                                                                 self.temp_dir_path,
                                                                                                 self.config_files_path,
                                                                                                 "config.yml")))

        self.assertTrue(configuration.xcassets_dir == "fake_xcassets_dir")
        self.assertTrue(configuration.raw_assets == "fake_raw_assets")
        self.assertTrue(configuration.generated_assets_dir == "fake_generated_assets")
        self.assertTrue(configuration.merge_with_xcassets == False)
        self.assertTrue(configuration.force_convert == True)

    def test_fail_when_there_are_no_parameters_and_config_file(self):
        self.assertRaises(NoConfigurationProvidedException, ConfigurationManager.get_configuration, None, None, None,
                          None, None, None)

    def test_fail_when_provided_config_file_does_not_exist(self):
        self.assertRaises(NoConfigFileFoundException, ConfigurationManager.get_configuration, None, None, None, None,
                          None, "blah_blah_blah")

    def test_fail_when_there_is_empty_config_file(self):
        self.assertRaises(NotCompleteConfigurationInConfigFileException, ConfigurationManager.get_configuration, None,
                          None, None, None, None,
                          config_file_path=os.path.join(self.config_files_path,
                                                        os.path.join(self.temp_dir_path, self.config_files_path,
                                                                     "empty.yml")))

    def test_fail_when_there_are_not_enough_parameters_in_config_file(self):
        self.assertRaises(NotCompleteConfigurationInConfigFileException, ConfigurationManager.get_configuration, None,
                          None, None, None, None,
                          config_file_path=os.path.join(self.config_files_path,
                                                        os.path.join(self.temp_dir_path, self.config_files_path,
                                                                     "half_empty.yml")))

    def test_fail_when_not_all_parameters_are_provided(self):
        wrong_args_sets = (
            (None, "b", "c", "d", "e"),
            ("", "b", "c", "d", "e"),
            ( "a", None, "c", "d", "e"),
            ( "a", "", "c", "d", "e"),
            ( "a", "b", None, "d", "e"),
            ( "a", "b", "", "d", "e"),
            ( "a", "b", "c", None, "e"),
            ( "a", "b", "c", "", "e"),
            ( "a", "b", "c", None, "e"),
            ( "a", "b", "c", "", "e"),
            ( "a", "b", "c", "d", ""),
            ( "a", "b", "c", "d", None),
        )

        for wrong_args in wrong_args_sets:
            self.assertRaises(NotAllConfigurationParametersPresentException, ConfigurationManager.get_configuration,
                              *wrong_args, config_file_path=None)
