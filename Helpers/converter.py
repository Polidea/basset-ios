import argparse
import os
import shutil
from wand.image import Image


class Converter:
    def __init__(self, input_dir, output_dir):
        self.inputDir = input_dir
        self.outputDir = output_dir

    def convert(self):
        print "Converting from " + self.inputDir + " to " + self.outputDir

        for original_base_path, subdirectories, files in os.walk(self.inputDir):
            for original_filename in files:
                basename = original_filename.split(".")[0]
                extension = original_filename.split(".")[1]

                if extension.lower() == "eps":
                    new_base_path = original_base_path.replace(self.inputDir, self.outputDir)
                    if not os.path.exists(new_base_path):
                            os.makedirs(new_base_path)
                    original_full_path = os.path.join(original_base_path, original_filename)
                    temporary_png_file = "temp.png"
                    with Image(filename=original_full_path) as img:
                        original_width = img.width
                        original_height = img.height
                        new_full_path_1x = os.path.join(new_base_path, basename + ".png")
                        new_full_path_2x = os.path.join(new_base_path, basename + "@2x.png")
                        new_full_path_3x = os.path.join(new_base_path, basename + "@3x.png")

                        img.save(filename=temporary_png_file)
                        shutil.copy2(temporary_png_file, new_full_path_1x)

                        img.resize(original_width * 2, original_height * 2)
                        img.save(filename=temporary_png_file)
                        shutil.copy2(temporary_png_file, new_full_path_2x)

                        img.resize(original_width * 3, original_height * 3)
                        img.save(filename=temporary_png_file)
                        shutil.copy2(temporary_png_file, new_full_path_3x)

                    os.remove(temporary_png_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-i', '--input_dir', default="./Assets", help='directory with raw assets')
    parser.add_argument('-o', '--output_dir', default="./GeneratedAssets",
                        help='directory where generated PNG(s) will be stored')
    args = parser.parse_args()

    converter = Converter(args.input_dir, args.output_dir)
    converter.convert()

