import argparse
import os
import logging
import sys
import subprocess

import coloredlogs
from wand.image import Image

from basset.exceptions import *


class Converter:
    def __init__(self):
        coloredlogs.install()
        self.inputDir = None
        self.outputDir = None
        self.force_convert = False

    @staticmethod
    def sha1_of_file(file_path):
        import hashlib

        sha = hashlib.sha1()
        with open(file_path, 'rb') as f:
            for line in f:
                sha.update(line)
            return sha.hexdigest()


    def convert_single_file(self, source_file, destination_file, target_resolution):
        sha1_of_original_file = self.sha1_of_file(source_file)

        if self.force_convert is False and os.path.isfile(destination_file):
            comment = subprocess.check_output("identify -verbose \"{0}\" | grep comment:".format(destination_file),
                                              shell=True).decode("utf-8")
            previous_sha1 = comment.replace("comment:", "").strip(" \t\n\r")

            if previous_sha1 == sha1_of_original_file:
                raise AssetAlreadyGeneratedException()

        convert_string = "convert \"{0}\" -resize {1}x{2} -density {3}x{4} -set comment {5} \"{6}\"".format(source_file,
                                                                                                    target_resolution[
                                                                                                        0],
                                                                                                    target_resolution[
                                                                                                        1],
                                                                                                    target_resolution[
                                                                                                        0],
                                                                                                    target_resolution[
                                                                                                        1],
                                                                                                    sha1_of_original_file,
                                                                                                    destination_file)

        os.system(convert_string)

    def convert(self):
        allowed_image_types = ["eps", "pdf", "svg", "psd", "png", "jpg", "jpeg", "gif"]
        logging.info("Converting vector files from " + self.inputDir + " to " + self.outputDir)

        directories_with_vector_files = {}
        if not os.path.isdir(self.inputDir):
            for path, subdirectories, files in os.walk(os.getcwd()):
                path = os.path.relpath(path, os.getcwd())
                for filename in files:

                    if "." in filename:
                        extension = filename.split(".")[1]

                        if extension.lower() in allowed_image_types:
                            top_dir_in_path = path.split(os.sep)[0]
                            if top_dir_in_path in directories_with_vector_files:
                                directories_with_vector_files[top_dir_in_path] += 1
                            else:
                                directories_with_vector_files[top_dir_in_path] = 1

            max_vector_files_count = -1
            directory_with_max_vector_files = None
            for path in directories_with_vector_files.keys():
                if directories_with_vector_files is not None:
                    if directories_with_vector_files[path] > max_vector_files_count:
                        max_vector_files_count = directories_with_vector_files[path]
                        directory_with_max_vector_files = path

            raise AssetsDirNotFoundException(directory_with_max_vector_files)

        converted_files_count = 0

        for original_base_path, subdirectories, files in os.walk(self.inputDir):
            if original_base_path.endswith(".imageset"):
                raise AssetsDirContainsImagesetDirectoryException(original_base_path, self.inputDir)

            for filename in files:
                if "." in filename:
                    basename = filename.split(".")[0]
                    extension = filename.split(".")[1]

                    if extension.lower() in allowed_image_types:
                        new_base_path = original_base_path.replace(self.inputDir, self.outputDir)
                        if not os.path.exists(new_base_path):
                            os.makedirs(new_base_path)
                        original_full_path = os.path.join(original_base_path, filename)

                        converted_files_count += 1

                        with Image(filename=original_full_path) as img:
                            original_size = img.size

                        image_size_1x = (original_size[0], original_size[0])
                        image_size_2x = (original_size[0] * 2, original_size[0] * 2)
                        image_size_3x = (original_size[0] * 3, original_size[0] * 3)

                        try:
                            self.convert_single_file(original_full_path, os.path.join(new_base_path, basename + ".png"),
                                                     image_size_1x)
                            if not basename.endswith(("@2x", "@3x")):
                                self.convert_single_file(original_full_path,
                                                         os.path.join(new_base_path, basename + "@2x.png"),
                                                         image_size_2x)
                                self.convert_single_file(original_full_path,
                                                         os.path.join(new_base_path, basename + "@3x.png"),
                                                         image_size_3x)

                            logging.info("Converted {0}".format(original_full_path))
                        except AssetAlreadyGeneratedException:
                            logging.info("Skipping (already generated) {0}".format(original_full_path))

        logging.info("Images conversion finished. Processed " + str(converted_files_count) + " images")


def main(args_to_parse):
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-i', '--input_dir', default="./Assets", help='directory with raw assets')
    parser.add_argument('-f', '--force_convert', default="False", help='should regenerate assets even when they were generated before')
    parser.add_argument('-o', '--output_dir', default="./GeneratedAssets",
                        help='directory where generated PNG(s) will be stored')
    parsed_args = parser.parse_args(args_to_parse)

    converter = Converter()
    converter.inputDir = parsed_args.input_dir
    converter.outputDir = parsed_args.output_dir
    converter.outputDir = parsed_args.force_convert
    converter.convert()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)