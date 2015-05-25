import os
import shutil
import tempfile
import json
from unittest import TestCase

from Helpers.merger import Merger, NoXCAssetsFoundException, NoDefaultXCAssetFoundException


class TestMerger(TestCase):
    tempDirPath = ""
    resources_path = "Assets"

    def setUp(self):
        self.tempDirPath = tempfile.mkdtemp()
        shutil.copytree("./Resources/tests_merger/SampleAssets", os.path.join(self.tempDirPath, self.resources_path))
        pass

    def tearDown(self):
        pass
        shutil.rmtree(self.tempDirPath)

    def test_no_xcassets(self):
        shutil.copytree("./Resources/tests_merger/NoXCAssetsTestResources", self.tempDirPath + "/Project")

        merger = Merger("./Assets", "./Project/NoXCAssetsTest/Images.xcassets")
        merger.merge()

        self.assertRaises(NoXCAssetsFoundException)

    def test_multiple_xcassets_no_default(self):
        shutil.copytree("./Resources/tests_merger/MultipleXCAssetsWithoutDefaultTestResources",
                        self.tempDirPath + "/Project")

        merger = Merger("./Assets", "./ProjectMultipleXCAssetsWithoutDefault/Images.xcassets")
        merger.merge()

        self.assertRaises(NoDefaultXCAssetFoundException)

    def test_single_asset(self):
        shutil.copytree("./Resources/tests_merger/SingleXCAssetTestResources", self.tempDirPath + "/Project")
        selected_asset_dir = self.tempDirPath + "/SingleXCAssetTestResources/SingleXCAssetsTest/Images.xcassets/"

        merger = Merger("./Assets", "./Project/SingleXCAssetsTest/Images.xcassets")
        merger.merge()

        self.check_if_everything_is_correct(selected_asset_dir, None)

        pass

    def test_multiple_assets_with_default(self):
        shutil.copytree("./Resources/tests_merger/MultipleXCAssetsIncludingDefaultTestResources",
                        self.tempDirPath + "/Project")
        selected_asset_dir = self.tempDirPath + "/MultipleXCAssetsIncludingDefaultTestResources/MultipleXCAssetsIncludingDefault/Images.xcassets/"
        secondary_assets_dir = self.tempDirPath + "/MultipleXCAssetsIncludingDefaultTestResources/MultipleXCAssetsIncludingDefault/Secondary.xcassets/"

        merger = Merger("./Assets", "./Project/MultipleXCAssetsIncludingDefault/Images.xcassets")
        merger.merge()

        self.check_if_everything_is_correct(selected_asset_dir, None)

        self.assertTrue(os.path.isdir(secondary_assets_dir))
        self.assertTrue(os.listdir(secondary_assets_dir) == [])

    def test_multiple_assets_with_existing_asset(self):
        shutil.copytree("./Resources/tests_merger/MultipleXCAssetsWithAssetThatNeedsUpdatingResources",
                        self.tempDirPath + "/Project")
        selected_asset_dir = self.tempDirPath + "/MultipleXCAssetsWithAssetThatNeedsUpdatingResources/MultipleXCAssetsWithAssetThatNeedsUpdating/Images.xcassets/"
        secondary_assets_dir = self.tempDirPath + "/MultipleXCAssetsWithAssetThatNeedsUpdatingResources/MultipleXCAssetsWithAssetThatNeedsUpdating/Secondary.xcassets/"

        merger = Merger("./Assets", "./Project/MultipleXCAssetsWithAssetThatNeedsUpdating/Images.xcassets")
        merger.merge()

        self.check_if_everything_is_correct(selected_asset_dir, 1)

        proper_dict = {
            "images": [
                {
                    "resizing": {
                        "mode": "3-part-vertical",
                        "center": {
                            "mode": "fill",
                            "height": 1
                        },
                        "capInsets": {
                            "top": 49,
                            "bottom": 49
                        }
                    },
                    "idiom": "universal",
                    "filename": "test-01.png",
                    "scale": "1x"
                },
                {
                    "idiom": "universal",
                    "scale": "2x",
                    "filename": "test-01@2x.png"
                },
                {
                    "idiom": "universal",
                    "scale": "3x",
                    "filename": "test-01@3x.png"
                }
            ],
            "info": {
                "version": 1,
                "author": "xcode",
                "template-rendering-intent": "template"
            }
        }

        with open(selected_asset_dir + "test-01.imageset/Contents.json") as data_file:
            json_dict = json.load(data_file)
        self.assertTrue(proper_dict == json_dict)

        self.assertTrue(os.path.isdir(secondary_assets_dir))
        self.assertTrue(os.listdir(secondary_assets_dir) == [])

    # Helpers-----------------------------------------------------------------------------------------------------------

    def check_if_everything_is_correct(self, selected_asset_dir, file_excluded_from_json_validation_index):
        assets_paths_dict = {
            1: {
                "source":
                    {
                        "1x": self.tempDirPath + "/Assets/test-01.png",
                        "2x": self.tempDirPath + "/Assets/test-01@2x.png",
                        "3x": self.tempDirPath + "/Assets/test-01@3x.png",
                    },
                "assets_dir": selected_asset_dir + "test-01.imageset"
            },
            2: {
                "source":
                    {
                        "1x": self.tempDirPath + "/Assets/test-02.png",
                        "2x": self.tempDirPath + "/Assets/test-02@2x.png",
                        "3x": self.tempDirPath + "/Assets/test-02@3x.png",
                    },
                "assets_dir": selected_asset_dir + "test-02.imageset"
            },
            3: {
                "source":
                    {
                        "1x": self.tempDirPath + "/Assets/test-03.png",
                        "2x": self.tempDirPath + "/Assets/test-03@2x.png",
                        "3x": self.tempDirPath + "/Assets/test-03@3x.png",
                    },
                "assets_dir": selected_asset_dir + "test-03.imageset"
            },
            4: {
                "source":
                    {
                        "1x": self.tempDirPath + "/Assets/subfolder/test-04.png",
                        "2x": self.tempDirPath + "/Assets/subfolder/test-04@2x.png",
                        "3x": self.tempDirPath + "/Assets/subfolder/test-04@3x.png",
                    },
                "assets_dir": selected_asset_dir + "subfolder/test-04.imageset"
            },
            5: {
                "source":
                    {
                        "1x": self.tempDirPath + "/Assets/subfolder/subsubfolder/test-05.png",
                        "2x": self.tempDirPath + "/Assets/subfolder/subsubfolder/test-05@2x.png",
                        "3x": self.tempDirPath + "/Assets/subfolder/subsubfolder/test-05@3x.png",
                    },
                "assets_dir": selected_asset_dir + "subfolder/subsubfolder/test-05.imageset"
            },
        }

        for i in range(1, 5):
            destination_directory_path = assets_paths_dict[i]["assets_dir"]
            images_dictionary = assets_paths_dict[i]["source"]
            json_path = destination_directory_path + "/Contents.json"

            self.check_if_images_are_copied(images_dictionary, destination_directory_path)

            if file_excluded_from_json_validation_index is not None and i != file_excluded_from_json_validation_index:
                self.validate_json_file(json_path, images_dictionary)


    def validate_json_file(self, json_file_path, images_dictionary):
        proper_dict = {
            "images": [],
            "info": {
                "version": 1,
                "author": "xcode"
            }
        }

        for scale_factor in images_dictionary:
            image_path = images_dictionary[scale_factor]
            proper_dict["images"].append(
                {
                    "idiom": "universal",
                    "filename": os.path.basename(image_path),
                    "scale": scale_factor
                }
            )

        with open(json_file_path) as data_file:
            json_dict = json.load(data_file)
        self.assertTrue(proper_dict == json_dict)

    def check_if_images_are_copied(self, source_images, destination_directory_path):
        self.assertTrue(os.path.isdir(destination_directory_path))
        json_path = destination_directory_path + "/Contents.json"
        self.assertTrue(os.path.isfile(json_path))

        for scale_factor in source_images:
            image_path = source_images[scale_factor]
            self.assertTrue(os.path.isfile(image_path))
            self.assertTrue(os.path.isfile(destination_directory_path + "/" + os.path.basename(image_path)))