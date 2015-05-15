import argparse

class Converter:

    def __init__(self, inputDir, outputDir):
        self.inputDir = inputDir
        self.outputDir = outputDir

    def convert(self):
        print "Converting from " + self.inputDir + " to " + self.outputDir

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-i', '--input_dir', default="./Assets", help='directory with raw assets')
    parser.add_argument('-o', '--output_dir', default="./GeneratedAssets", help='directory where generated PNG(s) will be stored')
    args = parser.parse_args()

    converter = Converter(args.input_dir, args.output_dir)
    converter.convert()

