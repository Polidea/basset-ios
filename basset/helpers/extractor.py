import argparse
import sys
import os

import coloredlogs
import shutil
from basset.exceptions import *
from basset.helpers.converter import Converter


class Extractor:
    def __init__(self):
        self.input_dir = None
        self.output_dir = None
        coloredlogs.install()

    def extract(self):

        if not self.input_dir.endswith("xcassets"):
            raise ExtractDirIsNotXcassetsDirException()

        for path, subdirectories, files in os.walk(self.input_dir):

            processed_assets = False
            for filename in files:
                if "." in filename and filename[0] is not ".":
                    extension = filename.split(".")[1]
                    if extension.lower() in Converter.allowed_image_types():
                        processed_assets = True
                        translated_path = os.path.relpath(path[:path.rfind("/")],self.input_dir)
                        output_dir_with_subdirectories = os.path.join(self.output_dir, translated_path)
                        if not os.path.isdir(output_dir_with_subdirectories):
                            os.makedirs(output_dir_with_subdirectories)

                        shutil.copy2(os.path.join(path, filename), os.path.join(output_dir_with_subdirectories, filename))

            if processed_assets:
                shutil.rmtree(path)

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