import argparse
import os
import shutil
import logging

import coloredlogs
import sys
from wand.image import Image


class Converter:
    def __init__(self):
        coloredlogs.install()
        self.inputDir = None
        self.outputDir = None

    def convert(self):
        logging.info("Converting vector files from " + self.inputDir + " to " + self.outputDir)
        if os.path.isdir(self.outputDir):
            shutil.rmtree(self.outputDir)

        converted_files_count = 0

        for original_base_path, subdirectories, files in os.walk(self.inputDir):
            for original_filename in files:
                basename = original_filename.split(".")[0]
                extension = original_filename.split(".")[1]

                if extension.lower() in ["eps", "pdf", "svg", "psd"]:
                    new_base_path = original_base_path.replace(self.inputDir, self.outputDir)
                    if not os.path.exists(new_base_path):
                        os.makedirs(new_base_path)
                    original_full_path = os.path.join(original_base_path, original_filename)

                    logging.info("Converting " + original_full_path)
                    converted_files_count += 1

                    with Image(filename=original_full_path) as img:
                        img.save(filename=os.path.join(new_base_path, basename + ".png"))
                    with Image(filename=original_full_path) as img:
                        img.resize(img.width * 2, img.height * 2)
                        img.save(filename=os.path.join(new_base_path, basename + "@2x.png"))
                    with Image(filename=original_full_path) as img:
                        img.resize(img.width * 3, img.height * 3)
                        img.save(filename=os.path.join(new_base_path, basename + "@3x.png"))

        logging.info("Images conversion finished. Converted " + str(converted_files_count) + " images")

def main(args_to_parse):
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-i', '--input_dir', default="./Assets", help='directory with raw assets')
    parser.add_argument('-o', '--output_dir', default="./GeneratedAssets",
                        help='directory where generated PNG(s) will be stored')
    parsed_args = parser.parse_args(args_to_parse)

    converter = Converter()
    converter.inputDir = parsed_args.input_dir
    converter.outputDir = parsed_args.output_dir
    converter.convert()

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)