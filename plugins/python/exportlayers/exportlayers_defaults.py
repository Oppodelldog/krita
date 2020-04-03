# This script is licensed CC 0 1.0, so that you can learn from it.

# ------ CC 0 1.0 ---------------

# The person who associated a work with this deed has dedicated the
# work to the public domain by waiving all of his or her rights to the
# work worldwide under copyright law, including all related and
# neighboring rights, to the extent allowed by law.

# You can copy, modify, distribute and perform the work, even for
# commercial purposes, all without asking permission.

# https://creativecommons.org/publicdomain/zero/1.0/legalcode
from . import settings_store
from . import settings_adapter

_DPI = 'dpi'
_RECT_WIDTH = 'rect_width'
_RECT_HEIGHT = 'rect_height'
_OUTPUT_DIRECTORY = 'output_directory'
_IGNORE_INVISIBLE_LAYERS = 'ignore_invisible_layers'
_BATCH_MODE = 'batch_mode'
_FILTER_LAYERS = 'export_filter_layers'
_CROP_TO_IMAGE_BOUNDS = 'crop_to_image_bounds'
_OUTPUT_FORMAT = 'output_format'

_SETTING_GROUP = 'exportlayers'

_SETTING_NAME = 'form_values'


#
# ExportLayersDefaultValuesFactory creates a new instance of ExportLayersDefaultValues
#
class ExportLayersDefaultValuesFactory:
    @staticmethod
    def create(krita_instance):
        setting_storage = settings_store.SettingsStore(_SETTING_GROUP, krita_instance)
        return ExportLayersDefaultValues(setting_storage)


#
# ExportLayersDefaultValues loads and saves qt control values from uiexportlayers form
#
class ExportLayersDefaultValues(settings_adapter.SettingsAdapter):
    def __init__(self, setting_storage):
        default_values = {
            _OUTPUT_FORMAT: 0,
            _CROP_TO_IMAGE_BOUNDS: False,
            _FILTER_LAYERS: False,
            _BATCH_MODE: True,
            _IGNORE_INVISIBLE_LAYERS: False,
            _OUTPUT_DIRECTORY: '',
            _RECT_HEIGHT: None,
            _RECT_WIDTH: None,
            _DPI: None,
        }
        super().__init__(setting_storage, _SETTING_NAME, default_values)

    def bind_output_format(self, combo_box):
        self._bind_combo_box(_OUTPUT_FORMAT, combo_box)

    def bind_crop_to_image_bounds(self, check_box):
        self._bind_check_box(_CROP_TO_IMAGE_BOUNDS, check_box)

    def bind_export_filter_layers_check_box(self, check_box):
        self._bind_check_box(_FILTER_LAYERS, check_box)

    def bind_batch_mode_check_box(self, check_box):
        self._bind_check_box(_BATCH_MODE, check_box)

    def bind_ignore_invisible_layers_check_box(self, check_box):
        self._bind_check_box(_IGNORE_INVISIBLE_LAYERS, check_box)

    def bind_output_directory(self, text_field):
        self._bind_text_field(_OUTPUT_DIRECTORY, text_field)

    def bind_rect_width_spin_box(self, spin_box):
        self._bind_spin_box(_RECT_WIDTH, spin_box)

    def bind_rect_height_spin_box(self, spin_box):
        self._bind_spin_box(_RECT_HEIGHT, spin_box)

    def bind_dpi_spin_box(self, spin_box):
        self._bind_spin_box(_DPI, spin_box)
