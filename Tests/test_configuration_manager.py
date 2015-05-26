import os
import shutil
import tempfile
from unittest import TestCase
from Helpers.configuration_manager import ConfigurationManager, NoConfigurationProvidedException, NoConfigFileException, \
    WrongConfigFileException, NotAllConfigurationParametersPresentException


class TestConfigurationManager(TestCase):
    temp_dir_path = ""
    config_files_path = "configs"
    sample_root_dir = "sample_root_dir"
    sample_xcassets_dir = "sample_xcassets_dir"
    sample_raw_assets_dir = "sample_raw_assets_dir"
    sample_generated_assets_dir = "sample_generated_assets_dir"
    sample_merge_with = "sample_merge_with_xcassets"

    def setUp(self):
        self.temp_dir_path = tempfile.mkdtemp()
        shutil.copytree("./Tests/Resources/tests_configuration_manager",
                        os.path.join(self.temp_dir_path, self.config_files_path))

    def tearDown(self):
        shutil.rmtree(self.temp_dir_path)

    def test_if_parameters_are_processed_to_configuration_object(self):
        configuration_manager = ConfigurationManager(root_dir=self.sample_root_dir,
                                                     xcassets_dir=self.sample_xcassets_dir,
                                                     raw_assets=self.sample_raw_assets_dir,
                                                     generated_assets_dir=self.sample_generated_assets_dir,
                                                     merge_with_xcassets=self.sample_merge_with,
                                                     config="fake_config_file")
        configuration = configuration_manager.get_configuration()

        self.assertTrue(configuration.root_dir == self.sample_root_dir)
        self.assertTrue(configuration.xcassets_dir == self.sample_xcassets_dir)
        self.assertTrue(configuration.raw_assets == self.sample_raw_assets_dir)
        self.assertTrue(configuration.generated_assets_dir == self.sample_generated_assets_dir)
        self.assertTrue(configuration.merge_with_xcassets == self.sample_merge_with)

    def test_using_config_file(self):
        configuration_manager = ConfigurationManager(root_dir=self.sample_root_dir,
                                                     xcassets_dir=self.sample_xcassets_dir,
                                                     raw_assets=self.sample_raw_assets_dir,
                                                     generated_assets_dir=self.sample_generated_assets_dir,
                                                     merge_with_xcassets=self.sample_merge_with,
                                                     config=os.path.join(self.config_files_path, "config.yml"))
        configuration = configuration_manager.get_configuration()

        self.assertTrue(configuration.root_dir == "fake_root_dir")
        self.assertTrue(configuration.xcassets_dir == "fake_xcassets_dir")
        self.assertTrue(configuration.raw_assets == "fake_raw_assets")
        self.assertTrue(configuration.generated_assets_dir == "fake_generated_assets")
        self.assertTrue(configuration.merge_with_xcassets == False)

    def test_fail_when_there_are_no_parameters_and_config_file(self):
        configuration_manager = ConfigurationManager(None, None, None, None, None, None)
        self.assertRaises(NoConfigurationProvidedException, configuration_manager.get_configuration)

    def test_fail_when_provided_config_file_does_not_exist(self):
        configuration_manager = ConfigurationManager(None, None, None, None, None, "blah_blah_blah")
        self.assertRaises(NoConfigFileException, configuration_manager.get_configuration)

    def test_fail_when_there_are_not_enough_parameters_in_config_file(self):
        configuration_manager = ConfigurationManager(None, None, None, None, None, config=os.path.join(self.config_files_path, "empty.yml"))
        self.assertRaises(WrongConfigFileException, configuration_manager.get_configuration)

    def test_fail_when_not_all_parameters_are_provided (self):
        configuration_manager = ConfigurationManager(None, "b", "c", "d", "e", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("", "b", "c", "d", "e", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("a", None, "c", "d", "e", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("a", "", "c", "d", "e", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("a", "b", None, "d", "e", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("a", "b", "", "d", "e", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("a", "b", "c", None, "e", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("a", "b", "c", "", "e", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("a", "b", "c", "d", None, config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)
        configuration_manager = ConfigurationManager("a", "b", "c", "d", "", config=None)
        self.assertRaises(NotAllConfigurationParametersPresentException, configuration_manager.get_configuration)