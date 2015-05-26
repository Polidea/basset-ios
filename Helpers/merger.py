import argparse
import json
import os
import shutil


class NoXCAssetsFoundException(Exception):
    pass


class NoDefaultXCAssetFoundException(Exception):
    pass


class Merger:
    def __init__(self):
        self.root_dir = None
        self.assets_dir = None
        self.default_xcasset_dir = None

    def get_selected_xcassets_dir(self):
        xcassets_list = []
        selected_xcassets = None
        for path, subdirectories, files in os.walk(self.root_dir):
            if path.endswith(".xcassets") and os.path.isdir(path):
                xcassets_list.append(path)

        xcassets_count = len(xcassets_list)
        if xcassets_count == 0:
            raise NoXCAssetsFoundException
        elif xcassets_count == 1:
            selected_xcassets = xcassets_list[0]
        elif xcassets_count >= 2:
            if os.path.join(self.root_dir, self.default_xcasset_dir) in xcassets_list:
                selected_xcassets = self.default_xcasset_dir
            else:
                raise NoDefaultXCAssetFoundException
        return selected_xcassets

    def merge(self):
        print "Merging assets from " + self.assets_dir + " using " + self.default_xcasset_dir + " as default xcassets"

        absolute_source_assets_dir = os.path.join(self.root_dir, self.assets_dir)
        relative_destination_xcassets = self.get_selected_xcassets_dir()

        assets_dict = {}
        for path, subdirectories, files in os.walk(absolute_source_assets_dir):
            for filename in files:
                if filename.lower().endswith(".png") or filename.lower().endswith(".jpg"):
                    basename = filename.split(".")[0]
                    relative_asset_directory_path = os.path.relpath(path, absolute_source_assets_dir)

                    if basename[-3:] in ["@2x", "@3x"]:
                        asset_scale = basename[-2:]
                        asset_name = basename[:-3]
                    else:
                        asset_scale = "1x"
                        asset_name = basename

                    asset_dir_in_destination_xcasset = os.path.join(self.root_dir, relative_destination_xcassets,
                                                                    relative_asset_directory_path,
                                                                    asset_name + ".imageset")
                    if not os.path.isdir(asset_dir_in_destination_xcasset):
                        os.makedirs(asset_dir_in_destination_xcasset)


                    # Create / update JSON file
                    content_json_file_path = os.path.join(asset_dir_in_destination_xcasset, "Contents.json")

                    contents_json = {
                        "images": [],
                        "info": {
                            "version": 1,
                            "author": "xcode",
                        }
                    }

                    if os.path.isfile(content_json_file_path):
                        with open(content_json_file_path, "r") as data_file:
                            contents_json = json.load(data_file)

                    image_found = False

                    for index, scaled_image_dict in enumerate(contents_json["images"]):
                        if scaled_image_dict["idiom"] == "universal" and scaled_image_dict["scale"] == asset_scale:
                            contents_json["images"][index]["filename"] = filename
                            image_found = True

                    if not image_found:
                        contents_json["images"].append(
                            {
                                "idiom": "universal",
                                "scale": asset_scale,
                                "filename": filename
                            }
                        )

                    with open(content_json_file_path, "w+") as data_file:
                        json.dump(contents_json, data_file, indent=1)



                    # Copy image
                    destination_path = os.path.join(asset_dir_in_destination_xcasset, filename)
                    source_path = os.path.join(absolute_source_assets_dir, relative_asset_directory_path, filename)
                    shutil.copy2(source_path, destination_path)

        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts raw assets to proper PNG(s).')
    parser.add_argument('-a', '--assets_dir', default="./GeneratedAssets",
                        help='path to directory with generated assets')
    parser.add_argument('-r', '--root_dir', default=os.getcwd(), help='path to root directory')
    parser.add_argument('-d', '--default_xcassets_dir', default="./GeneratedAssets",
                        help='path to default XCAssets directory')
    args = parser.parse_args()

    merger = Merger()
    merger.root_dir = args.root_dir
    merger.assets_dir = args.assets_dir
    merger.default_xcasset_dir = args.default_xcasset_dir
    Merger.merge()

