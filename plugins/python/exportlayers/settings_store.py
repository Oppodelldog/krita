# This script is licensed CC 0 1.0, so that you can learn from it.

# ------ CC 0 1.0 ---------------

# The person who associated a work with this deed has dedicated the
# work to the public domain by waiving all of his or her rights to the
# work worldwide under copyright law, including all related and
# neighboring rights, to the extent allowed by law.

# You can copy, modify, distribute and perform the work, even for
# commercial purposes, all without asking permission.

# https://creativecommons.org/publicdomain/zero/1.0/legalcode
import json


#
# SettingsStore acts as a convenience wrapper to store setting values in krita of different types
#
class SettingsStore:
    def __init__(self, setting_group, storage_adapter):
        self.setting_group = setting_group
        self.storageAdapter = storage_adapter

    def dictionary(self, name):
        settings_data_json = self.storageAdapter.readSetting(self.setting_group, name, '{}')
        return json.JSONDecoder().decode(settings_data_json)

    def set_dictionary(self, name, value):
        settings_data_json = json.JSONEncoder().encode(value)
        self.storageAdapter.writeSetting(self.setting_group, name, settings_data_json)

    def sub_dictionary(self, name, key):
        dictionary = self.dictionary(name)
        if key in dictionary:
            return dictionary[key]

        return {}

    def set_sub_dictionary(self, name, key, value):
        dictionary = self.dictionary(name)
        dictionary[key] = value
        self.set_dictionary(name, dictionary)

    def remove_sub_dictionary(self, name, key):
        dictionary = self.dictionary(name)
        if key in dictionary:
            del dictionary[key]
            self.set_dictionary(name, dictionary)
