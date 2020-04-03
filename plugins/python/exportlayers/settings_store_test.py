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

from mock import MagicMock

from settings_store import SettingsStore

setting_name = 'stub-setting-name'
group_name = 'settings-group-name'


class TestSettingsStore(unittest.TestCase):
    def setUp(self):
        self.adapter = MagicMock()
        self.adapter.readSetting = MagicMock(name='readSetting')
        self.adapter.writeSetting = MagicMock(name='writeSetting')
        self.sut = SettingsStore(group_name, self.adapter)

    def test_dictionary(self):
        self.stub_store_with_settings("{\"stub\": true}")

        self.assertDictEqual({"stub": True}, self.sut.dictionary(setting_name))

        expected_default_value = '{}'
        self.adapter.readSetting.assert_called_once_with(group_name, setting_name, expected_default_value)

    def test_set_dictionary(self):
        self.sut.set_dictionary(setting_name, {"test": 123})

        self.adapter.writeSetting.assert_called_once_with(group_name, setting_name, '{"test": 123}')

    def test_sub_dictionary(self):
        sub_dictionary_name = "test"
        self.stub_store_with_settings('{"test": {"sub-dictionary":456}}')

        sub_dictionary = self.sut.sub_dictionary(setting_name, sub_dictionary_name)

        self.assertDictEqual({"sub-dictionary": 456}, sub_dictionary)
        self.adapter.readSetting.assert_called_once_with(group_name, setting_name, '{}')

    def test_sub_dictionary_unknown_sub_dictionary_expect_to_return_empty_dictionary(self):
        sub_dictionary_name = "unknown"
        self.stub_store_with_settings('{"test": {"sub-dictionary":456}}')

        sub_dictionary = self.sut.sub_dictionary(setting_name, sub_dictionary_name)

        self.assertDictEqual({}, sub_dictionary)

    def stub_store_with_settings(self, value):
        self.adapter.readSetting.return_value = value

    def test_set_sub_dictionary(self):
        sub_dictionary_name = "test-2"
        sub_dictionary = {"sub-dictionary-1": 789}
        self.stub_store_with_settings('{}')

        self.sut.set_sub_dictionary(setting_name, sub_dictionary_name, sub_dictionary)

        self.adapter.writeSetting.assert_called_once_with(
            group_name,
            setting_name,
            '{"test-2": {"sub-dictionary-1": 789}}'
        )

    def test_set_sub_dictionary_adds_to_existing(self):
        sub_dictionary_name = "test-2"
        sub_dictionary = {"sub-dictionary-1": 789}
        self.stub_store_with_settings('{"test-1": {"sub-dictionary-1":456}}')

        self.sut.set_sub_dictionary(setting_name, sub_dictionary_name, sub_dictionary)

        self.adapter.writeSetting.assert_called_once_with(
            group_name,
            setting_name,
            '{"test-1": {"sub-dictionary-1": 456}, "test-2": {"sub-dictionary-1": 789}}'
        )

    def test_set_sub_dictionary_overwrites_existing(self):
        sub_dictionary_name = "test-1"
        sub_dictionary = {"sub-dictionary-1": 789}
        self.stub_store_with_settings('{"test-1": {"sub-dictionary-1":456}}')

        self.sut.set_sub_dictionary(setting_name, sub_dictionary_name, sub_dictionary)

        self.adapter.writeSetting.assert_called_once_with(
            group_name,
            setting_name,
            '{"test-1": {"sub-dictionary-1": 789}}'
        )

    def test_remove_sub_dictionary(self):
        sub_dictionary_name = "test-2"
        self.stub_store_with_settings('{"test-1": {"sub-dictionary-1": 456}, "test-2": {"sub-dictionary-1": 789}}')

        self.sut.remove_sub_dictionary(setting_name, sub_dictionary_name)

        self.adapter.writeSetting.assert_called_once_with(
            group_name,
            setting_name,
            '{"test-1": {"sub-dictionary-1": 456}}'
        )

    def test_remove_sub_dictionary_unknown_sub_dictionary_expect_no_change_to_stored_settings(self):
        sub_dictionary_name = "test-3"
        self.stub_store_with_settings('{"test-1": {"sub-dictionary-1": 456}}')

        self.sut.remove_sub_dictionary(setting_name, sub_dictionary_name)

        self.adapter.writeSetting.assert_not_called()

    def test_remove_sub_dictionary_empty_store_expect_no_change_to_stored_settings(self):
        sub_dictionary_name = "test-1"
        self.stub_store_with_settings('{}')

        self.sut.remove_sub_dictionary(setting_name, sub_dictionary_name)

        self.adapter.writeSetting.assert_not_called()
