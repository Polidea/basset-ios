import os
import yaml


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


class ConfigurationManager:
    def __init__(self):
        pass

    @staticmethod
    def get_configuration(xcassets_dir, raw_assets, generated_assets_dir, root_dir, merge_with_xcassets, config):
        configuration = StudioConfiguration()

        if not xcassets_dir and not raw_assets and not generated_assets_dir and not root_dir and not merge_with_xcassets and not config:
            raise NoConfigurationProvidedException

        if not config and (
                                not xcassets_dir or not raw_assets or not generated_assets_dir or not root_dir or not merge_with_xcassets):
            raise NotAllConfigurationParametersPresentException

        if config:
            if not os.path.isfile(config):
                raise NoConfigFileFoundException

            yml_file = open(config)
            yml_config_dict = yaml.load(yml_file)
            yml_file.close()

            if not yml_config_dict or  not all(k in yml_config_dict for k in ("xcassets_dir", "raw_assets", "generated_assets_dir", "root_dir", "merge_with_xcassets")):
                raise NotCompleteConfigurationInConfigFileException

            configuration.xcassets_dir = yml_config_dict['xcassets_dir']
            configuration.raw_assets = yml_config_dict["raw_assets"]
            configuration.generated_assets_dir = yml_config_dict["generated_assets_dir"]
            configuration.root_dir = yml_config_dict["root_dir"]
            configuration.merge_with_xcassets = yml_config_dict["merge_with_xcassets"]
        else:
            configuration.xcassets_dir = xcassets_dir
            configuration.raw_assets = raw_assets
            configuration.generated_assets_dir = generated_assets_dir
            configuration.root_dir = root_dir
            configuration.merge_with_xcassets = merge_with_xcassets

        return configuration