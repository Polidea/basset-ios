import argparse
import json
import logging
import subprocess
import sys
import hashlib

import coloredlogs
from wand.image import Image

from basset.exceptions import *


class Converter:
    def __init__(self):
        coloredlogs.install()
        self.input_dir = ""
        self.output_dir = ""
        self.force_convert = False
        self.converted_files_hashes = {}

    @staticmethod
    def allowed_image_types():
        return ["eps", "pdf", "svg", "psd"]

    @staticmethod
    def sha1_of_file(file_path):
        sha = hashlib.sha1()
        with open(file_path, 'rb') as f:
            for line in f:
                sha.update(line)
            return sha.hexdigest()

    def convert_single_file(self, source_file, destination_file, target_resolution, scale_factor, transparent_color):
        sha1_of_original_file = self.sha1_of_file(source_file)

        add_transparency_part = ""
        if transparent_color:
            add_transparency_part = "-transparent \"{0}\"".format(transparent_color)

        self.converted_files_hashes[destination_file] = sha1_of_original_file

        convert_string = "convert " \
                         "-density {0}00% " \
                         "-background none " \
                         "\"{1}\" " \
                         " {2} " \
                         "-resize {3}x{4} " \
                         "\"{5}\"".format(scale_factor,
                                          source_file,
                                          add_transparency_part,
                                          target_resolution[0],
                                          target_resolution[1],
                                          destination_file)

        os.system(convert_string)

    def check_if_file_needs_reconverting(self, source_file, destination_file):
        sha1_of_original_file = self.sha1_of_file(source_file)

        destination_file_missing = not os.path.isfile(destination_file)
        destination_file_was_generated_from_the_different_file = destination_file in self.converted_files_hashes and \
                                                                 self.converted_files_hashes[
                                                                     destination_file] != sha1_of_original_file

        return self.force_convert or destination_file_missing or destination_file_was_generated_from_the_different_file

    @staticmethod
    def return_first_line_containing_string(lines, match_string):
        for line in lines.splitlines():
            if match_string in line:
                return line

        return None

    @staticmethod
    def get_image_metadata(path):
        raw = subprocess.check_output("identify -verbose \"{0}\"".format(path),
                                      shell=True).decode("utf-8")

        resolution_id = "Geometry:"
        transparent_color_id = "Transparent color:"

        resolution = Converter.return_first_line_containing_string(raw, resolution_id)
        resolution = resolution.replace(resolution_id, "").strip(" \t\n\r").split("+")[0]
        resolution_parts = resolution.split("x")

        transparent_color = Converter.return_first_line_containing_string(raw, transparent_color_id)
        if transparent_color:
            transparent_color = transparent_color.replace(transparent_color_id, "").strip(" \t\n\r")

        return (int(resolution_parts[0]), int(resolution_parts[1])), transparent_color

    def convert(self):
        self.input_dir = self.input_dir.rstrip('\\/')
        self.output_dir = self.output_dir.rstrip('\\/')

        self.input_dir = os.path.expandvars(os.path.expanduser(self.input_dir))
        self.output_dir = os.path.expandvars(os.path.expanduser(self.output_dir))

        logging.info("Converting vector files from {0} to {1}".format(self.input_dir, self.output_dir))

        temp_file = os.path.join(self.output_dir, ".basset_temp")
        if os.path.isfile(temp_file):
            with open(temp_file, "r") as data_file:
                self.converted_files_hashes = json.load(data_file)

        self.check_if_input_dir_contains_vector_assets()
        self.check_if_input_dir_contains_xcassets()

        converted_files_count = 0
        for original_base_path, subdirectories, files in os.walk(self.input_dir):

            for filename in files:
                if "." in filename and filename[0] is not ".":
                    basename = filename.split(".")[0]
                    extension = filename.split(".")[1].lower()

                    if extension in Converter.allowed_image_types():
                        new_base_path = original_base_path.replace(self.input_dir, self.output_dir)
                        if not os.path.exists(new_base_path):
                            os.makedirs(new_base_path)
                        original_full_path = os.path.join(original_base_path, filename)

                        destination_templates = [(1, ".png")]
                        if extension is not "png":
                            destination_templates.append((2, "@2x.png"))
                            destination_templates.append((3, "@3x.png"))

                        selected_destination_templates = []
                        for template in destination_templates:
                            destination_path = os.path.join(new_base_path, basename + template[1])
                            if self.check_if_file_needs_reconverting(original_full_path, destination_path):
                                selected_destination_templates.append(template)

                        if len(selected_destination_templates) > 0:
                            original_size, transparent_color = Converter.get_image_metadata(original_full_path)

                            for template in selected_destination_templates:
                                converted_files_count += 1
                                new_image_size = (original_size[0] * template[0], original_size[1] * template[0])
                                destination_path = os.path.join(new_base_path, basename + template[1])

                                self.convert_single_file(original_full_path, destination_path, new_image_size,
                                                         template[0], transparent_color)
                                logging.info("Converted {0} to {1}".format(original_full_path, destination_path))

        if converted_files_count > 0:
            with open(temp_file, "w+") as data_file:
                json.dump(self.converted_files_hashes, data_file, indent=1)

        logging.info("Images conversion finished. Processed " + str(converted_files_count) + " images")

    def check_if_input_dir_contains_xcassets(self):
        for original_base_path, subdirectories, files in os.walk(self.input_dir):
            if original_base_path.endswith(".imageset"):
                raise AssetsDirContainsImagesetDirectoryException(original_base_path, self.input_dir)

    def check_if_input_dir_contains_vector_assets(self):
        directories_with_vector_files = {}
        if not os.path.isdir(self.input_dir):
            for path, subdirectories, files in os.walk(os.getcwd()):
                path = os.path.relpath(path, os.getcwd())
                for filename in files:
                    if "." in filename and filename[0] is not ".":
                        extension = filename.split(".")[1]

                        if extension.lower() in Converter.allowed_image_types():
                            top_dir_in_path = path.split(os.sep)[0]
                            if top_dir_in_path in directories_with_vector_files:
                                directories_with_vector_files[top_dir_in_path] += 1
                            else:
                                directories_with_vector_files[top_dir_in_path] = 1

            if directories_with_vector_files is not None:
                max_vector_files_count = -1
                directory_with_max_vector_files = None
                for path in directories_with_vector_files.keys():
                    if not path.endswith(".xcassets"):
                        if directories_with_vector_files[path] > max_vector_files_count:
                            max_vector_files_count = directories_with_vector_files[path]
                            directory_with_max_vector_files = path

                raise AssetsDirNotFoundException(directory_with_max_vector_files)


def main(args_to_parse):
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-i', '--input_dir', default="./Assets", help='directory with raw assets')
    parser.add_argument('-f', '--force_convert', default="False",
                        help='should regenerate assets even when they were generated before')
    parser.add_argument('-o', '--output_dir', default="./GeneratedAssets",
                        help='directory where generated PNG(s) will be stored')
    parsed_args = parser.parse_args(args_to_parse)

    converter = Converter()
    converter.input_dir = parsed_args.input_dir
    converter.output_dir = parsed_args.output_dir
    converter.output_dir = parsed_args.force_convert
    converter.convert()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
