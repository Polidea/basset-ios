import argparse
import logging

import coloredlogs
import sys

from basset.helpers.configuration_manager import ConfigurationManager

from basset.helpers.converter import Converter
from basset.helpers.merger import Merger
from basset.exceptions import *

class Basset:
    def __init__(self, configuration, merger, converter):
        coloredlogs.install()

        logging.info("Using configuration: \n" + str(configuration))

        self.configuration = configuration
        self.merger = merger
        self.converter = converter

        self.merger.source_assets_dir = configuration.generated_assets_dir
        self.merger.default_xcasset_dir = configuration.xcassets_dir

        self.converter.inputDir = configuration.raw_assets
        self.converter.outputDir = configuration.generated_assets_dir

    def launch(self):
        self.converter.convert()
        if self.configuration.merge_with_xcassets:
            self.merger.merge()

def main(args_to_parse):
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-x', '--xcassets_dir', default="Resources/Images.xcassets",
                        help='path to directory with default xcassets directory')
    parser.add_argument('-r', '--raw_assets_dir', default="Resources/Assets",
                        help='path to directory with raw, vector based graphics')
    parser.add_argument('-g', '--generated_assets_dir', default="Resources/GeneratedAssets",
                        help='path to directory where generated PNGs will be stored')
    parser.add_argument('-m', '--merge_with_xcassets', default=True, help='will script process xcassets directories')
    parser.add_argument('-c', '--config', help='path to config file')
    parsed_args = parser.parse_args(args=args_to_parse)

    merger = Merger()
    converter = Converter()
    configuration = ConfigurationManager.get_configuration(xcassets_dir=parsed_args.xcassets_dir,
                                                           raw_assets=parsed_args.raw_assets_dir,
                                                           generated_assets_dir=parsed_args.generated_assets_dir,
                                                           merge_with_xcassets=parsed_args.merge_with_xcassets,
                                                           config_file_path=parsed_args.config)
    basset = Basset(merger=merger, converter=converter, configuration=configuration)

    try:
        basset.launch()
    except BassetException as e:
        logging.error(e.get_message())

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)

