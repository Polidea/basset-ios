from _ast import operator

import os
import shutil
import tempfile
import json
from unittest import TestCase
from nose.tools import assert_raises
from basset.helpers.merger import Merger
from basset.exceptions import *


class TestMerger(TestCase):
    temp_dir_path = ""
    script_root_dir_path = ""
    resources_path = "Assets"

    @classmethod
    def setUpClass(cls):
        TestMerger.script_root_dir_path = os.getcwd()

    @classmethod
    def tearDownClass(cls):
        os.chdir(TestMerger.script_root_dir_path)

    def setUp(self):
        self.temp_dir_path = tempfile.mkdtemp()
        shutil.copytree(
            os.path.join(TestMerger.script_root_dir_path, "basset/tests/Resources/tests_merger/SampleAssets"),
            os.path.join(self.temp_dir_path, self.resources_path))
        os.chdir(self.temp_dir_path)
        pass

    def tearDown(self):
        pass
        shutil.rmtree(self.temp_dir_path)

    def test_no_xcassets(self):
        shutil.copytree(
            os.path.join(TestMerger.script_root_dir_path,
                         "basset/tests/Resources/tests_merger/NoXCAssetsTestResources"),
            os.path.join(self.temp_dir_path, "Project"))

        merger = Merger()
        merger.source_assets_dir = "Assets"
        merger.default_xcasset_dir = "Project/NoXCAssetsTest/Images.xcassets"
        assert_raises(NoXCAssetsFoundException, merger.merge)

    def test_multiple_xcassets_no_default(self):
        shutil.copytree(os.path.join(TestMerger.script_root_dir_path,
                                     "basset/tests/Resources/tests_merger/MultipleXCAssetsWithoutDefaultTestResources"),
                        os.path.join(self.temp_dir_path, "Project"))

        merger = Merger()
        merger.source_assets_dir = "Assets"
        merger.default_xcasset_dir = "Project/MultipleXCAssetsWithoutDefault/Images.xcassets"

        assert_raises(NoDefaultXCAssetFoundException, merger.merge)

    def test_single_asset(self):
        shutil.copytree(
            os.path.join(TestMerger.script_root_dir_path,
                         "basset/tests/Resources/tests_merger/SingleXCAssetTestResources"),
            os.path.join(self.temp_dir_path, "Project"))
        selected_asset_dir = "Project/SingleXCAssetsTest/Images.xcassets"

        merger = Merger()
        merger.source_assets_dir = "Assets"
        merger.default_xcasset_dir = selected_asset_dir
        merger.merge()

        self.check_if_images_are_copied_and_jsons_are_valid(os.path.join(self.temp_dir_path, selected_asset_dir), None)

        pass

    def test_multiple_assets_with_default(self):
        shutil.copytree(os.path.join(TestMerger.script_root_dir_path,
                                     "basset/tests/Resources/tests_merger/MultipleXCAssetsIncludingDefaultTestResources"),
                        os.path.join(self.temp_dir_path, "Project"))
        selected_asset_dir = "Project/MultipleXCAssetsIncludingDefault/Images.xcassets"
        secondary_assets_dir = os.path.join(self.temp_dir_path,
                                            "Project/MultipleXCAssetsIncludingDefault/Secondary.xcassets")

        merger = Merger()
        merger.source_assets_dir = "Assets"
        merger.default_xcasset_dir = selected_asset_dir
        merger.merge()

        self.check_if_images_are_copied_and_jsons_are_valid(os.path.join(self.temp_dir_path, selected_asset_dir), None)

        self.assertTrue(os.path.isdir(secondary_assets_dir))
        self.assertTrue(os.listdir(secondary_assets_dir) == ['empty_xcassets_here'])

    def test_multiple_assets_with_existing_asset(self):
        shutil.copytree(os.path.join(TestMerger.script_root_dir_path,
                                     "basset/tests/Resources/tests_merger/MultipleXCAssetsWithAssetThatNeedsUpdatingResources"),
                        os.path.join(self.temp_dir_path, "Project"))
        selected_asset_dir = "Project/MultipleXCAssetsWithAssetThatNeedsUpdating/Images.xcassets"
        secondary_assets_dir = os.path.join(self.temp_dir_path,
                                            "Project/MultipleXCAssetsWithAssetThatNeedsUpdating/Secondary.xcassets")

        merger = Merger()
        merger.source_assets_dir = "Assets"
        merger.default_xcasset_dir = selected_asset_dir
        merger.merge()

        self.check_if_images_are_copied_and_jsons_are_valid(selected_asset_dir, 1)

        expected_dict = {
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

        with open(os.path.join(os.path.join(self.temp_dir_path, selected_asset_dir),
                               "test-01.imageset/Contents.json")) as data_file:
            actual_dict = json.load(data_file)
            actual_dict["images"] = sorted(actual_dict["images"], key=lambda k: k["filename"])
            expected_dict["images"] = sorted(expected_dict["images"], key=lambda k: k["filename"])
            self.assertDictEqual(expected_dict, actual_dict)

        self.assertTrue(os.path.isdir(secondary_assets_dir))
        self.assertTrue(os.listdir(secondary_assets_dir) == ['empty_xcassets_here'])

    # Helpers-----------------------------------------------------------------------------------------------------------


    def check_if_images_are_copied_and_jsons_are_valid(self, selected_asset_dir,
                                                       file_excluded_from_json_validation_index):
        assets_paths_dict = {
            1: {
                "source":
                    {
                        "1x": os.path.join(self.temp_dir_path, "Assets/test-01.png"),
                        "2x": os.path.join(self.temp_dir_path, "Assets/test-01@2x.png"),
                        "3x": os.path.join(self.temp_dir_path, "Assets/test-01@3x.png"),
                    },
                "assets_dir": os.path.join(selected_asset_dir, "test-01.imageset")
            },
            2: {
                "source":
                    {
                        "1x": os.path.join(self.temp_dir_path, "Assets/test-02.png"),
                        "2x": os.path.join(self.temp_dir_path, "Assets/test-02@2x.png"),
                        "3x": os.path.join(self.temp_dir_path, "Assets/test-02@3x.png"),
                    },
                "assets_dir": os.path.join(selected_asset_dir, "test-02.imageset")
            },
            3: {
                "source":
                    {
                        "1x": os.path.join(self.temp_dir_path, "Assets/test-03.png"),
                        "2x": os.path.join(self.temp_dir_path, "Assets/test-03@2x.png"),
                        "3x": os.path.join(self.temp_dir_path, "Assets/test-03@3x.png"),
                    },
                "assets_dir": os.path.join(selected_asset_dir, "test-03.imageset")
            },
            4: {
                "source":
                    {
                        "1x": os.path.join(self.temp_dir_path, "Assets/subfolder/test-04.png"),
                        "2x": os.path.join(self.temp_dir_path, "Assets/subfolder/test-04@2x.png"),
                        "3x": os.path.join(self.temp_dir_path, "Assets/subfolder/test-04@3x.png"),
                    },
                "assets_dir": os.path.join(selected_asset_dir, "subfolder/test-04.imageset")
            },
            5: {
                "source":
                    {
                        "1x": os.path.join(self.temp_dir_path, "Assets/subfolder/subsubfolder/test-05.png"),
                        "2x": os.path.join(self.temp_dir_path, "Assets/subfolder/subsubfolder/test-05@2x.png"),
                        "3x": os.path.join(self.temp_dir_path, "Assets/subfolder/subsubfolder/test-05@3x.png"),
                    },
                "assets_dir": os.path.join(selected_asset_dir, "subfolder/subsubfolder/test-05.imageset")
            },
        }

        for i in range(1, 5):
            destination_directory_path = assets_paths_dict[i]["assets_dir"]
            images_dictionary = assets_paths_dict[i]["source"]
            json_path = os.path.join(destination_directory_path, "Contents.json")

            self.check_if_images_are_copied(images_dictionary, destination_directory_path)

            if file_excluded_from_json_validation_index is not None and i != file_excluded_from_json_validation_index:
                self.validate_json_file(json_path, images_dictionary)


    def validate_json_file(self, json_file_path, images_dictionary):
        expected_dict = {
            "images": [],
            "info": {
                "version": 1,
                "author": "xcode"
            }
        }

        for scale_factor in images_dictionary:
            image_path = images_dictionary[scale_factor]
            expected_dict["images"].append(
                {
                    "idiom": "universal",
                    "filename": os.path.basename(image_path),
                    "scale": scale_factor
                }
            )

        with open(json_file_path) as data_file:
            actual_dict = json.load(data_file)
            actual_dict["images"] = sorted(actual_dict["images"], key=lambda k: k["filename"])
            expected_dict["images"] = sorted(expected_dict["images"], key=lambda k: k["filename"])
            self.assertDictEqual(expected_dict, actual_dict)

    def check_if_images_are_copied(self, source_images, destination_directory_path):
        self.assertTrue(os.path.isdir(destination_directory_path))
        json_path = os.path.join(destination_directory_path, "Contents.json")
        self.assertTrue(os.path.isfile(json_path))

        for scale_factor in source_images:
            image_path = source_images[scale_factor]
            self.assertTrue(os.path.isfile(image_path))
            self.assertTrue(os.path.isfile(os.path.join(destination_directory_path, os.path.basename(image_path))))