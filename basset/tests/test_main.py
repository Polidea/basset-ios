from unittest import TestCase

from mock import Mock

from basset.helpers.configuration_manager import BassetConfiguration
from basset.helpers.converter import Converter
from basset.helpers.merger import Merger
from basset.basset_ios import Basset


class TestBasset(TestCase):
    sample_xcassets_dir = "sample_xcassets_dir"
    sample_raw_assets_dir = "sample_raw_assets_dir"
    sample_generated_assets_dir = "sample_generated_assets_dir"
    sample_extract_path = "sample_extract_path"
    sample_merge_with = True
    sample_force_covert = True

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_if_all_configuration_properties_are_passed(self):
        configuration = BassetConfiguration()

        configuration.xcassets_dir = self.sample_xcassets_dir
        configuration.raw_assets = self.sample_raw_assets_dir
        configuration.generated_assets_dir = self.sample_generated_assets_dir
        configuration.merge_with_xcassets = self.sample_merge_with
        configuration.extract_path = self.sample_extract_path
        configuration.force_convert = self.sample_force_covert

        merger = Merger()
        converter = Converter()
        extractor = Mock()
        basset = Basset(merger=merger, converter=converter, extractor=extractor, configuration=configuration)

        self.assertEqual(basset.merger.default_xcasset_dir, self.sample_xcassets_dir)
        self.assertEqual(basset.merger.source_assets_dir, self.sample_generated_assets_dir)

        self.assertEqual(basset.converter.input_dir, self.sample_raw_assets_dir)
        self.assertEqual(basset.converter.output_dir, self.sample_generated_assets_dir)
        self.assertEqual(basset.converter.force_convert, self.sample_force_covert)

        self.assertEqual(basset.extractor.input_dir, self.sample_extract_path)
        self.assertEqual(basset.extractor.output_dir, self.sample_raw_assets_dir)

    def test_if_converter_and_merger_methods_are_called(self):
        configuration = BassetConfiguration()
        configuration.merge_with_xcassets = True
        configuration.extract_path = None

        merger = Mock()
        converter = Mock()
        extractor = Mock()

        basset = Basset(merger=merger, converter=converter, extractor=extractor, configuration=configuration)
        basset.launch()

        converter.convert.assert_called_once_with()
        merger.merge.assert_called_once_with()
        self.assertEqual(extractor.extract.call_count, 0)

    def test_respect_merge_with_xcassets_flag(self):
        configuration = BassetConfiguration()
        configuration.merge_with_xcassets = False
        configuration.extract_path = None

        merger = Mock()
        converter = Mock()
        extractor = Mock()
        basset = Basset(merger=merger, converter=converter, extractor=extractor, configuration=configuration)
        basset.launch()

        converter.convert.assert_called_once_with()
        self.assertEqual(merger.merge.call_count, 0)
        self.assertEqual(extractor.extract.call_count, 0)

    def test_cont_convert_and_merge_in_extract_mode(self):
        configuration = BassetConfiguration()
        configuration.extract_path = "some_path"

        merger = Mock()
        converter = Mock()
        extractor = Mock()
        basset = Basset(merger=merger, converter=converter, extractor=extractor, configuration=configuration)
        basset.launch()

        self.assertEqual(converter.convert.call_count, 0)
        self.assertEqual(merger.merge.call_count, 0)
        extractor.extract.assert_called_once_with()
