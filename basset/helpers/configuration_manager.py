import os
import logging

import yaml
import coloredlogs

from basset.exceptions import *


class BassetConfiguration:
    def __init__(self):
        self.xcassets_dir = None
        self.raw_assets = None
        self.extract_path = None
        self.generated_assets_dir = None
        self.merge_with_xcassets = True
        self.force_convert = False

    def __str__(self):
        return "Default xcassets: {0} \n" \
               "Assets directory: {1} \n" \
               "Generated assets directory: {2} \n" \
               "Extract path: {3} \n" \
               "Merge with xcassets: {4}\n" \
               "Force convert: {5}".format(self.xcassets_dir, self.raw_assets, self.generated_assets_dir,
                                           self.extract_path, self.merge_with_xcassets, self.force_convert)

class ConfigurationManager:
    def __init__(self):
        coloredlogs.install()
        pass

    @staticmethod
    def get_configuration(xcassets_dir, raw_assets, generated_assets_dir, merge_with_xcassets, force_convert, extract_path,
                          config_file_path):
        configuration = BassetConfiguration()

        if not xcassets_dir and not raw_assets and not extract_path and not generated_assets_dir and not merge_with_xcassets and not force_convert and not config_file_path:
            raise NoConfigurationProvidedException()

        if not config_file_path and (
                                not xcassets_dir or not raw_assets  or not extract_path or not generated_assets_dir or not merge_with_xcassets or not force_convert):
            raise NotAllConfigurationParametersPresentException()

        if config_file_path:
            if not os.path.isfile(config_file_path):
                raise NoConfigFileFoundException()

            yml_file = open(config_file_path)
            yml_config_dict = yaml.load(yml_file)
            yml_file.close()

            if not yml_config_dict or not all(k in yml_config_dict for k in (
                    "xcassets_dir", "raw_assets", "generated_assets_dir", "merge_with_xcassets", "force_convert")):
                raise NotCompleteConfigurationInConfigFileException()

            logging.info("Using configuration from " + config_file_path + " file")
            configuration.xcassets_dir = yml_config_dict['xcassets_dir']
            configuration.raw_assets = yml_config_dict["raw_assets"]
            configuration.generated_assets_dir = yml_config_dict["generated_assets_dir"]
            configuration.merge_with_xcassets = yml_config_dict["merge_with_xcassets"]
            configuration.force_convert = yml_config_dict["force_convert"]
        else:
            logging.info("Using configuration from command line")
            configuration.xcassets_dir = xcassets_dir
            configuration.raw_assets = raw_assets
            configuration.extract_path = extract_path
            configuration.generated_assets_dir = generated_assets_dir
            configuration.merge_with_xcassets = merge_with_xcassets
            configuration.force_convert = force_convert

        return configuration
