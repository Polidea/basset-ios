import argparse
import os
from Helpers.configuration_manager import ConfigurationManager
from Helpers.converter import Converter
from Helpers.merger import Merger

class Studio:
    def __init__(self, configuration, merger, converter):
        self.configuration = configuration
        self.merger = merger
        self.converter = converter

    def launch(self):
        self.converter.convert()
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
    parser.add_argument('-c', '--config', default="Assets/config.yml", help='path to config file')
    args = parser.parse_args()

    merger = Merger()
    converter = Converter()
    # def __init__(self, xcassets_dir, raw_assets, generated_assets_dir, root_dir, merge_with_xcassets, config):
    configuration = ConfigurationManager(root_dir=args.root_dir,
                                         xcassets_dir=args.xcassets_dir,
                                         raw_assets=args.raw_assets_dir,
                                         generated_assets_dir=args.generated_assets_dir,
                                         merge_with_xcassets=args.merge_with_xcassets,
                                         config=args.config)
    studio = Studio(merger=merger, converter=converter, configuration=configuration)
    studio.launch()