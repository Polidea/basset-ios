class NoConfigurationProvidedException(Exception):
    pass

class NoConfigFileException(Exception):
    pass

class WrongConfigFileException(Exception):
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
    def __init__(self, xcassets_dir, raw_assets, generated_assets_dir, root_dir, merge_with_xcassets, config):
        pass

    def get_configuration(self):
        configuration = StudioConfiguration()

        return configuration