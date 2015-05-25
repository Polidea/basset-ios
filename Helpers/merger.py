import argparse
import os

class NoXCAssetsFoundException(Exception):
    pass

class NoDefaultXCAssetFoundException(Exception):
    pass

class Merger:
    def __init__(self, assets_dir, default_xcasset_dir):
        self.assets_dir = assets_dir
        self.default_xcasset_dir = default_xcasset_dir

    def merge(self):
        print "Merging assets from " + self.assets_dir + " using " + self.default_xcasset_dir + " as default xcassets"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-a', '--assets_dir', default="./GeneratedAssets", help='path to directory with generated assets')
    parser.add_argument('-d', '--default_xcassets_dir', default="./GeneratedAssets",
                        help='path to default XCAssets directory')
    args = parser.parse_args()

    merger = Merger(args.assets_dir, args.default_xcasset_dir)
    Merger.merge()

