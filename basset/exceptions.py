import abc


class BassetException(Exception):
    @abc.abstractmethod
    def get_message(self):
        pass

class AssetAlreadyGeneratedException(Exception):
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


class AssetsDirNotFoundException(BassetException):
    def __init__(self, asset_dir_candidate):
        self.asset_dir_candidate = asset_dir_candidate

    def get_message(self):
        if self.asset_dir_candidate is None:
            return "I haven't found any vector assets. In order to use basset, you need to create directory with them and run this command:\n" \
               "basset_ios -r <assets_directory_path>"
        else:
            return "I haven't found vector assets directory you've provided, but it looks like most of them are in \"{0}\" directory. You can use this directory by running basset with command: \n" \
               "basset_ios -r {1} \nor create config file.".format(self.asset_dir_candidate,self.asset_dir_candidate)


class NoDefaultXCAssetFoundException(BassetException):
    def __init__(self, assets_count):
        self.assets_count = assets_count

    def get_message(self):
        return "Found {0} xcassets, but none of them is default one!".format(str(self.assets_count))
