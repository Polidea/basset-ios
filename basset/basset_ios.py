import argparse
import logging
import sys
import time

import coloredlogs

from basset.helpers.configuration_manager import ConfigurationManager
from basset.helpers.converter import Converter
from basset.helpers.extractor import Extractor
from basset.helpers.merger import Merger
from basset.exceptions import *


class Basset:
    def __init__(self, configuration, merger, extractor, converter):
        coloredlogs.install()

        logging.info("Using configuration: \n" + str(configuration))

        self.configuration = configuration
        self.merger = merger
        self.converter = converter
        self.extractor = extractor

        self.merger.source_assets_dir = configuration.generated_assets_dir
        self.merger.default_xcasset_dir = configuration.xcassets_dir

        self.converter.input_dir = configuration.raw_assets
        self.converter.output_dir = configuration.generated_assets_dir
        self.converter.force_convert = configuration.force_convert

        self.extractor.input_dir = configuration.extract_path
        self.extractor.output_dir = configuration.raw_assets

    def launch(self):
        if self.extractor.input_dir is None:
            self.converter.convert()
            if self.configuration.merge_with_xcassets:
                self.merger.merge()
        else:
            self.extractor.extract()


def main(args_to_parse):
    begin_time = time.time()
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')

    main_group = parser.add_argument_group("Main arguments", "Assets converting and merging with xcassets")
    extract_group = parser.add_argument_group("Extract group", "Extracting assets ")

    parser.add_argument('-r', '--raw_assets_dir', default="VectorAssets",
                        help='path to directory with raw, vector based graphics')
    main_group.add_argument('-x', '--xcassets_dir', default="Assets.xcassets",
                            help='path to directory with default xcassets directory')
    main_group.add_argument('-g', '--generated_assets_dir', default="GeneratedAssets",
                            help='path to directory where generated PNGs will be stored')
    main_group.add_argument('-f', '--force_convert', default=False,
                            help='should regenerate assets even when they were generated before')
    main_group.add_argument('-m', '--merge_with_xcassets', default=True,
                            help='will script process xcassets directories')
    extract_group.add_argument('-e', '--extract_path', default=None,
                               help='if set to existing xcassets directory, will extract all assets from it to "raw_assets_dir"')
    main_group.add_argument('-c', '--config', help='path to config file')
    parsed_args = parser.parse_args(args=args_to_parse)

    try:
        merger = Merger()
        converter = Converter()
        extractor = Extractor()
        configuration = ConfigurationManager.get_configuration(xcassets_dir=parsed_args.xcassets_dir,
                                                               raw_assets=parsed_args.raw_assets_dir,
                                                               generated_assets_dir=parsed_args.generated_assets_dir,
                                                               merge_with_xcassets=parsed_args.merge_with_xcassets,
                                                               force_convert=parsed_args.force_convert,
                                                               extract_path=parsed_args.extract_path,
                                                               config_file_path=parsed_args.config)
        basset = Basset(merger=merger, converter=converter, extractor=extractor, configuration=configuration)
        basset.launch()
    except BassetException as e:
        logging.error(e.get_message())

    end_time = time.time()
    logging.info("Execution time: {0:.2f} seconds".format(end_time - begin_time))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
