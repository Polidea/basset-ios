import argparse
import sys
import shutil
import logging

import coloredlogs

from basset.exceptions import *
from basset.helpers.converter import Converter


class Extractor:
    def __init__(self):
        self.input_dir = None
        self.output_dir = None
        coloredlogs.install()

    def extract(self):
        self.input_dir = self.input_dir.rstrip('\\/')
        self.output_dir = self.output_dir.rstrip('\\/')
        logging.info("Extracting vector files from {0} to {1}".format(self.input_dir, self.output_dir))

        if not self.input_dir.endswith(".xcassets"):
            raise ExtractDirIsNotXcassetsDirException()

        extracted_files_count = 0
        for path, subdirectories, files in os.walk(self.input_dir):
            processed_assets = False
            for filename in files:
                if "." in filename and filename[0] is not ".":
                    extension = filename.split(".")[1]
                    if extension.lower() in Converter.allowed_image_types():
                        processed_assets = True
                        translated_path = os.path.relpath(path[:path.rfind("/")], self.input_dir)
                        output_dir_with_subdirectories = os.path.join(self.output_dir, translated_path)
                        if not os.path.isdir(output_dir_with_subdirectories):
                            os.makedirs(output_dir_with_subdirectories)

                        extracted_files_count += 1
                        source_path = os.path.join(path, filename)
                        destination_path = os.path.join(output_dir_with_subdirectories, filename)
                        shutil.copy2(source_path, destination_path)
                        logging.info("Extracting {0} to {1}".format(source_path, destination_path))

            if processed_assets:
                shutil.rmtree(path)
        logging.info("Extracted {0} files".format(extracted_files_count))


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
