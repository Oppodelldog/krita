# This script is licensed CC 0 1.0, so that you can learn from it.

# ------ CC 0 1.0 ---------------

# The person who associated a work with this deed has dedicated the
# work to the public domain by waiving all of his or her rights to the
# work worldwide under copyright law, including all related and
# neighboring rights, to the extent allowed by law.

# You can copy, modify, distribute and perform the work, even for
# commercial purposes, all without asking permission.

# https://creativecommons.org/publicdomain/zero/1.0/legalcode


#
# SettingsAdapter helps saving and loading qt form values from a settings storage
#
class SettingsAdapter:
    def __init__(self, settings_storage, setting_name_settings='settings', default_settings=None):
        self._settings_storage = settings_storage
        self._setting_name_settings = setting_name_settings
        if default_settings is None:
            default_settings = {}
        self._default_settings = default_settings
        self._settings_dictionary = {}
        self._combo_boxes = {}
        self._check_boxes = {}
        self._text_fields = {}
        self._spin_boxes = {}

    def load(self, key):
        is_saved_setting = True
        self._settings_dictionary = self._settings_storage.sub_dictionary(self._setting_name_settings, key)
        if not bool(self._settings_dictionary):
            self._settings_dictionary = self._get_default_settings()
            is_saved_setting = False
        self._apply_values()
        return is_saved_setting

    def save(self, key):
        self._fetch_values()
        self._settings_storage.set_sub_dictionary(
            self._setting_name_settings,
            key,
            self._settings_dictionary
        )

    def remove(self, key):
        self._settings_storage.remove_sub_dictionary(self._setting_name_settings, key)
        self._settings_dictionary = self._get_default_settings()
        self._apply_values()
        self._settings_dictionary = {}

    def _bind_check_box(self, name, check_box):
        self._check_boxes[name] = check_box

    def _bind_text_field(self, name, text_field):
        self._text_fields[name] = text_field

    def _bind_spin_box(self, name, spin_box):
        self._spin_boxes[name] = spin_box

    def _bind_combo_box(self, name, combo_box):
        self._combo_boxes[name] = combo_box

    def _apply_values(self):
        for config_name, combo_box in self._combo_boxes.items():
            value = self._get_setting_value(config_name)
            if value is None:
                continue
            combo_box.setCurrentIndex(value)
        for config_name, check_box in self._check_boxes.items():
            value = self._get_setting_value(config_name)
            if value is None:
                continue
            check_box.setChecked(value)
        for config_name, text_field in self._text_fields.items():
            value = self._get_setting_value(config_name)
            if value is None:
                continue
            text_field.setText(value)
        for config_name, spin_box in self._spin_boxes.items():
            value = self._get_setting_value(config_name)
            if value is None:
                continue
            spin_box.setValue(value)

    def _fetch_values(self):
        self._settings_dictionary = {}
        for config_name, combo_box in self._combo_boxes.items():
            self._settings_dictionary[config_name] = combo_box.currentIndex()
        for name, check_box in self._check_boxes.items():
            self._settings_dictionary[name] = check_box.isChecked()
        for name1, spin_box in self._spin_boxes.items():
            self._settings_dictionary[name1] = spin_box.value()
        for name2, text_field in self._text_fields.items():
            self._settings_dictionary[name2] = text_field.text()

    def _get_default_settings(self):
        return self._default_settings

    def _get_setting_value(self, config_name):
        if config_name in self._settings_dictionary:
            return self._settings_dictionary[config_name]
        default_values = self._get_default_settings()
        if config_name in default_values:
            return default_values[config_name]
        return None
