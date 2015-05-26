from unittest import TestCase
from Helpers.configuration_manager import StudioConfiguration
from Helpers.converter import Converter
from Helpers.merger import Merger
from studio import Studio
from mock import MagicMock

class TestStudio(TestCase):
    sample_root_dir = "sample_root_dir"
    sample_xcassets_dir = "sample_xcassets_dir"
    sample_raw_assets_dir = "sample_raw_assets_dir"
    sample_generated_assets_dir = "sample_generated_assets_dir"
    sample_merge_with = "sample_merge_with_xcassets"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_if_all_configuration_properties_are_passed(self):
        configuration = StudioConfiguration()

        configuration.xcassets_dir = self.sample_xcassets_dir
        configuration.raw_assets = self.sample_raw_assets_dir
        configuration.generated_assets_dir = self.sample_generated_assets_dir
        configuration.root_dir = self.sample_root_dir
        configuration.merge_with_xcassets = self.sample_merge_with

        merger = Merger()
        converter = Converter()
        studio = Studio(merger=merger, converter=converter, configuration=configuration)

        self.assertTrue(studio.merger.default_xcasset_dir == self.sample_xcassets_dir)
        self.assertTrue(studio.merger.assets_dir == self.sample_generated_assets_dir)
        self.assertTrue(studio.merger.root_dir == self.sample_root_dir)

        self.assertTrue(studio.converter.inputDir == self.sample_raw_assets_dir)
        self.assertTrue(studio.converter.outputDir == self.sample_generated_assets_dir)

    def test_if_converter_and_merger_methods_are_called_in_order(self):
        configuration = StudioConfiguration()
        merger = Merger()
        converter = Converter()
        merger.merge = Merger()

        converter.convert = MagicMock()
        merger.merge = MagicMock()

        studio = Studio(merger=merger, converter=converter, configuration=configuration)
        studio.launch()

        converter.convert.assert_called_with()
        #TODO think about order
        merger.merge.assert_called_with()