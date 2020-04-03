# This script is licensed CC 0 1.0, so that you can learn from it.

# ------ CC 0 1.0 ---------------

# The person who associated a work with this deed has dedicated the
# work to the public domain by waiving all of his or her rights to the
# work worldwide under copyright law, including all related and
# neighboring rights, to the extent allowed by law.

# You can copy, modify, distribute and perform the work, even for
# commercial purposes, all without asking permission.

# https://creativecommons.org/publicdomain/zero/1.0/legalcode
import unittest
from unittest.mock import patch, MagicMock

from exportlayers_defaults import ExportLayersDefaultValues, ExportLayersDefaultValuesFactory


class TestExportLayersDefaultValues(unittest.TestCase):

    def setUp(self):
        self.stub = MagicMock()

    @patch("settings_adapter.SettingsAdapter.__init__")
    def test_constructor_passes_storage_key_and_defaults_to_super_class(self, mock):
        settings_storage_stub = MagicMock()
        ExportLayersDefaultValues(settings_storage_stub), settings_storage_stub
        mock.assert_called_once_with(
            settings_storage_stub,
            'form_values',
            {
                'output_format': 0,
                'crop_to_image_bounds': False,
                'export_filter_layers': False,
                'batch_mode': True,
                'ignore_invisible_layers': False,
                'output_directory': '',
                'rect_height': None,
                'rect_width': None,
                'dpi': None,
            }
        )

    @patch("settings_adapter.SettingsAdapter._bind_combo_box")
    def test_bind_output_format(self, mock):
        self.create_default_values().bind_output_format(self.stub)
        mock.assert_called_once_with('output_format', self.stub)

    @patch("settings_adapter.SettingsAdapter._bind_check_box")
    def test_bind_crop_to_image_bounds(self, mock):
        self.create_default_values().bind_crop_to_image_bounds(self.stub)
        mock.assert_called_once_with('crop_to_image_bounds', self.stub)

    @patch("settings_adapter.SettingsAdapter._bind_check_box")
    def test_bind_export_filter_layers_check_box(self, mock):
        self.create_default_values().bind_export_filter_layers_check_box(self.stub)
        mock.assert_called_once_with('export_filter_layers', self.stub)

    @patch("settings_adapter.SettingsAdapter._bind_check_box")
    def test_bind_batch_mode_check_box(self, mock):
        self.create_default_values().bind_batch_mode_check_box(self.stub)
        mock.assert_called_once_with('batch_mode', self.stub)

    @patch("settings_adapter.SettingsAdapter._bind_check_box")
    def test_bind_ignore_invisible_layers_check_box(self, mock):
        self.create_default_values().bind_ignore_invisible_layers_check_box(self.stub)
        mock.assert_called_once_with('ignore_invisible_layers', self.stub)

    @patch("settings_adapter.SettingsAdapter._bind_text_field")
    def test_bind_output_directory(self, mock):
        self.create_default_values().bind_output_directory(self.stub)
        mock.assert_called_once_with('output_directory', self.stub)

    @patch("settings_adapter.SettingsAdapter._bind_spin_box")
    def test_bind_rect_width_spin_box(self, mock):
        self.create_default_values().bind_rect_width_spin_box(self.stub)
        mock.assert_called_once_with('rect_width', self.stub)

    @patch("settings_adapter.SettingsAdapter._bind_spin_box")
    def test_bind_rect_height_spin_box(self, mock):
        self.create_default_values().bind_rect_height_spin_box(self.stub)
        mock.assert_called_once_with('rect_height', self.stub)

    @patch("settings_adapter.SettingsAdapter._bind_spin_box")
    def test_bind_dpi_spin_box(self, mock):
        self.create_default_values().bind_dpi_spin_box(self.stub)
        mock.assert_called_once_with('dpi', self.stub)

    @staticmethod
    def create_default_values():
        return ExportLayersDefaultValues(MagicMock())


class TestExportLayersDefaultValuesFactory(unittest.TestCase):
    @patch("exportlayers_defaults.ExportLayersDefaultValues", autospec=True)
    @patch("settings_store.SettingsStore", autospec=False)
    def test_create(self, mock1, mock2):
        stub = MagicMock()
        ExportLayersDefaultValuesFactory.create(stub)
        mock1.assert_called_once_with('exportlayers', stub)
        mock2.assert_called_once_with(mock1())
