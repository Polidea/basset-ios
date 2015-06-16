import argparse
import sys
import os

import coloredlogs
from basset.exceptions import *


class Extractor:
    def __init__(self):
        self.input_dir = None
        self.output_dir = None
        coloredlogs.install()

    def extract(self):

        if not self.input_dir.endswith("xcassets"):
            raise ExtractDirIsNotXcassetsDirException()


def main(args_to_parse):
    parser = argparse.ArgumentParser(description='Extracts assets from xcassets to ordinary directories.')
    parser.add_argument('-i', '--input_dir', default="./Assets.xcassets",
                        help='path to directory with assets that will be extracted from')
    parser.add_argument('-o', '--output_dir', default="./Assets",
                        help='path to destination directory')
    parsed_args = parser.parse_args(args_to_parse)

    extractor = Extractor()
    extractor.input_dir = parsed_args.input_dir
    extractor.output_dir = parsed_args.output_dir
    Extractor.extract()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)