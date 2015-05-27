import argparse
import os
from Helpers.configuration_manager import ConfigurationManager
from Helpers.converter import Converter
from Helpers.merger import Merger
import coloredlogs, logging

class Studio:
    def __init__(self, configuration, merger, converter):
        coloredlogs.install()

        logging.info("Using configuration: \n" + str(configuration))

        self.configuration = configuration
        self.merger = merger
        self.converter = converter



        self.merger.assets_dir = configuration.generated_assets_dir
        self.merger.root_dir = configuration.root_dir
        self.merger.default_xcasset_dir = configuration.xcassets_dir

        self.converter.inputDir = configuration.raw_assets
        self.converter.outputDir = configuration.generated_assets_dir



    def launch(self):
        self.converter.convert()
        if self.configuration.merge_with_xcassets:
            self.merger.merge()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-d', '--xcassets_dir', default="Resources/Images.xcassets",
                        help='path to directory with default xcassets directory')
    parser.add_argument('-a', '--raw_assets_dir', default="Resources/Assets",
                        help='path to directory with raw, vector based graphics')
    parser.add_argument('-g', '--generated_assets_dir', default="Resources/GeneratedAssets",
                        help='path to directory where generated PNGs will be stored')
    parser.add_argument('-r', '--root_dir', default=os.getcwd(), help='path to root directory')
    parser.add_argument('-m', '--merge_with_xcassets', default=True, help='will script process xcassets directories')
    parser.add_argument('-c', '--config', help='path to config file')
    args = parser.parse_args()

    merger = Merger()
    converter = Converter()
    configuration = ConfigurationManager.get_configuration(root_dir=args.root_dir,
                                         xcassets_dir=args.xcassets_dir,
                                         raw_assets=args.raw_assets_dir,
                                         generated_assets_dir=args.generated_assets_dir,
                                         merge_with_xcassets=args.merge_with_xcassets,
                                         config_file_path=args.config)
    studio = Studio(merger=merger, converter=converter, configuration=configuration)
    studio.launch()