import os
import yaml
import coloredlogs, logging


class NoConfigurationProvidedException(Exception):
    pass


class NoConfigFileFoundException(Exception):
    pass


class NotCompleteConfigurationInConfigFileException(Exception):
    pass


class NotAllConfigurationParametersPresentException(Exception):
    pass


class StudioConfiguration:
    def __init__(self):
        self.xcassets_dir = None
        self.raw_assets = None
        self.generated_assets_dir = None
        self.root_dir = None
        self.merge_with_xcassets = None

    def __str__(self):
        return "Default xcassets: {0} \n" \
               "Assets directory: {1} \n" \
               "Generated assets directory: {2} \n" \
               "Root directory: {3} \n" \
               "Merge with xcassets: {4}".format(self.xcassets_dir, self.raw_assets, self.generated_assets_dir,
                                                 self.root_dir, self.merge_with_xcassets)


class ConfigurationManager:
    def __init__(self):
        coloredlogs.install()
        pass

    @staticmethod
    def get_configuration(xcassets_dir, raw_assets, generated_assets_dir, root_dir, merge_with_xcassets,
                          config_file_path):
        configuration = StudioConfiguration()

        if not xcassets_dir and not raw_assets and not generated_assets_dir and not root_dir and not merge_with_xcassets and not config_file_path:
            logging.error("No configuration provided!")
            raise NoConfigurationProvidedException

        if not config_file_path and (
                                not xcassets_dir or not raw_assets or not generated_assets_dir or not root_dir or not merge_with_xcassets):
            logging.error("Not all config parameters found!")
            raise NotAllConfigurationParametersPresentException

        if config_file_path:
            if not os.path.isfile(config_file_path):
                logging.error("Config file not found!")
                raise NoConfigFileFoundException

            yml_file = open(config_file_path)
            yml_config_dict = yaml.load(yml_file)
            yml_file.close()

            if not yml_config_dict or not all(k in yml_config_dict for k in (
                    "xcassets_dir", "raw_assets", "generated_assets_dir", "root_dir", "merge_with_xcassets")):
                logging.error("Config file broken!")
                raise NotCompleteConfigurationInConfigFileException

            logging.info("Using configuration from " + config_file_path + " file")
            configuration.xcassets_dir = yml_config_dict['xcassets_dir']
            configuration.raw_assets = yml_config_dict["raw_assets"]
            configuration.generated_assets_dir = yml_config_dict["generated_assets_dir"]
            configuration.root_dir = yml_config_dict["root_dir"]
            configuration.merge_with_xcassets = yml_config_dict["merge_with_xcassets"]
        else:
            logging.info("Using configuration from command line")
            configuration.xcassets_dir = xcassets_dir
            configuration.raw_assets = raw_assets
            configuration.generated_assets_dir = generated_assets_dir
            configuration.root_dir = root_dir
            configuration.merge_with_xcassets = merge_with_xcassets

        return configuration