import abc


class BassetException(Exception):
    @abc.abstractmethod
    def get_message(self):
        pass


class NoConfigurationProvidedException(Exception):
    def get_message(self):
        return "No configuration provided!"


class NoConfigFileFoundException(Exception):
    def get_message(self):
        return "Config file not found!"


class NotCompleteConfigurationInConfigFileException(Exception):
    def get_message(self):
        return "Config file broken!"


class NotAllConfigurationParametersPresentException(Exception):
    def get_message(self):
        return "Not all config parameters found!"


class NoXCAssetsFoundException(Exception):
    def get_message(self):
        return "No xcassets found"


class NoDefaultXCAssetFoundException(Exception):
    def __init__(self, assets_count):
        self.assets_count = assets_count

    def get_message(self):
        return "Found {0} xcassets, but none of them is default one!".str(self.assets_count)
