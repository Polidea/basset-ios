import abc


class BassetException(Exception):
    @abc.abstractmethod
    def get_message(self):
        pass


class NoConfigurationProvidedException(BassetException):
    def get_message(self):
        return "No configuration provided!"


class NoConfigFileFoundException(BassetException):
    def get_message(self):
        return "Config file not found!"


class NotCompleteConfigurationInConfigFileException(BassetException):
    def get_message(self):
        return "Config file broken!"


class NotAllConfigurationParametersPresentException(BassetException):
    def get_message(self):
        return "Not all config parameters found!"


class NoXCAssetsFoundException(BassetException):
    def get_message(self):
        return "No xcassets found"


class NoDefaultXCAssetFoundException(BassetException):
    def __init__(self, assets_count):
        self.assets_count = assets_count

    def get_message(self):
        return "Found {0} xcassets, but none of them is default one!".format(str(self.assets_count))
