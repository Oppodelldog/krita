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
from unittest.mock import MagicMock

from settings_adapter import SettingsAdapter


class TestSavedSettings(unittest.TestCase):
    def setUp(self):
        self.settings_name = 'settings'
        self.setting_key = 'key'

    def test_construction(self):
        self.assertIsNotNone(SettingsAdapter(self._get_empty_store(), self.settings_name))

    def test_load_empty_store_should_apply_defaults(self):
        adapter = SettingsAdapter(self._get_empty_store(), self.settings_name, {'test-check-box': True})
        check_box = DummyCheckBox()
        adapter._bind_check_box('test-check-box', check_box)

        self.assertFalse(check_box.isChecked())

        adapter.load(self.setting_key)

        self.assertTrue(check_box.isChecked())

    def test_load_should_apply_stored_value(self):
        store = self._get_empty_store()
        store.sub_dictionary = MagicMock(return_value={'test-check-box': True})
        adapter = SettingsAdapter(store, self.settings_name, {'test-check-box': False})
        check_box = DummyCheckBox()
        adapter._bind_check_box('test-check-box', check_box)

        adapter.load(self.setting_key)

        self.assertTrue(check_box.isChecked())

    def test_save_writes_dictionary(self):
        store = self._get_empty_store()
        adapter = SettingsAdapter(store, 'settings', {})
        check_box = DummyCheckBox()
        check_box.setChecked(True)
        adapter._bind_check_box('test-check-box', check_box)

        adapter.save(self.setting_key)

        store.set_sub_dictionary.assert_called_once_with(self.settings_name, self.setting_key, {'test-check-box': True})

    def test_remove_calls_remove_in_store_and_applies_defaults(self):
        store = self._get_empty_store()
        adapter = SettingsAdapter(store, 'settings', {'test-check-box': False})
        check_box = DummyCheckBox()
        check_box.setChecked(True)
        adapter._bind_check_box('test-check-box', check_box)

        adapter.remove(self.setting_key)

        self.assertFalse(check_box.isChecked())
        store.remove_sub_dictionary.assert_called_once_with(self.settings_name, self.setting_key)

    def test_control_types_load_save(self):
        store = self._get_empty_store()
        default_check_box_1 = False
        default_check_box_2 = True
        default_combo_box_1 = 0
        default_combo_box_2 = 1
        default_text_field_1 = ''
        default_text_field_2 = 'hello'
        default_spin_box_1 = 0
        default_spin_box_2 = 1
        default_values = {
            'check-box-1': default_check_box_1,
            'check-box-2': default_check_box_2,
            'combo-box-1': default_combo_box_1,
            'combo-box-2': default_combo_box_2,
            'text-field-1': default_text_field_1,
            'text-field-2': default_text_field_2,
            'spin-box-1': default_spin_box_1,
            'spin-box-2': default_spin_box_2,
        }
        check_box_1 = DummyCheckBox()
        check_box_2 = DummyCheckBox()
        combo_box_1 = DummyComboBox()
        combo_box_2 = DummyComboBox()
        text_field_1 = DummyTextField()
        text_field_2 = DummyTextField()
        spin_box_1 = DummySpinBox()
        spin_box_2 = DummySpinBox()

        adapter = SettingsAdapter(store, 'settings', default_values)
        adapter._bind_check_box('check-box-1', check_box_1)
        adapter._bind_check_box('check-box-2', check_box_2)
        adapter._bind_combo_box('combo-box-1', combo_box_1)
        adapter._bind_combo_box('combo-box-2', combo_box_2)
        adapter._bind_text_field('text-field-1', text_field_1)
        adapter._bind_text_field('text-field-2', text_field_2)
        adapter._bind_spin_box('spin-box-1', spin_box_1)
        adapter._bind_spin_box('spin-box-2', spin_box_2)

        # since store is empty, load will assign default values to controls
        adapter.load(self.setting_key)

        self.assertEqual(default_check_box_1, check_box_1.isChecked())
        self.assertEqual(default_check_box_2, check_box_2.isChecked())
        self.assertEqual(default_combo_box_1, combo_box_1.currentIndex())
        self.assertEqual(default_combo_box_2, combo_box_2.currentIndex())
        self.assertEqual(default_text_field_1, text_field_1.text())
        self.assertEqual(default_text_field_2, text_field_2.text())
        self.assertEqual(default_spin_box_1, spin_box_1.value())
        self.assertEqual(default_spin_box_2, spin_box_2.value())

        # save will store the controls values
        adapter.save(self.setting_key)
        store.set_sub_dictionary.assert_called_once_with(
            'settings', 'key',
            {
                'combo-box-1': default_combo_box_1,
                'combo-box-2': default_combo_box_2,
                'check-box-1': default_check_box_1,
                'check-box-2': default_check_box_2,
                'spin-box-1': default_spin_box_1,
                'spin-box-2': default_spin_box_2,
                'text-field-1': default_text_field_1,
                'text-field-2': default_text_field_2
            }
        )

    # in this test 3 segments provide None values
    def test_control_types_none_value_is_not_assigned(self):
        store = self._get_empty_store()
        # store gives None values
        store.sub_dictionary = MagicMock(
            return_value={
                'check-box': None,
                'combo-box': None,
            }
        )
        # default values gives None values
        default_values = {
            'spin-box': None,
        }
        # 'text-field' has neither data in store nor in default values
        # it's value should also be unchanged

        check_box = DummyCheckBox()
        check_box.setChecked(True)
        combo_box = DummyComboBox()
        combo_box.setCurrentIndex(1)
        text_field = DummyTextField()
        text_field.setText("Hello")
        spin_box = DummySpinBox()
        spin_box.setValue(1)

        adapter = SettingsAdapter(store, 'settings', default_values)
        adapter._bind_check_box('check-box', check_box)
        adapter._bind_combo_box('combo-box', combo_box)
        adapter._bind_text_field('text-field', text_field)
        adapter._bind_spin_box('spin-box', spin_box)

        # since store is empty, load will assign default values to controls
        adapter.load(self.setting_key)

        self.assertEqual(True, check_box.isChecked())
        self.assertEqual(1, combo_box.currentIndex())
        self.assertEqual("Hello", text_field.text())
        self.assertEqual(1, spin_box.value())

    @staticmethod
    def _get_empty_store():
        setting_store_stub = MagicMock()
        setting_store_stub.sub_dictionary = MagicMock(return_value={})
        setting_store_stub.set_sub_dictionary = MagicMock(name="set_sub_dictionary")
        setting_store_stub.remove_sub_dictionary = MagicMock(name="remove_sub_dictionary")
        return setting_store_stub


# Test double for a QtCheckBox implementing value accessor methods
# noinspection PyPep8Naming
class DummyCheckBox:
    def __init__(self):
        self.value = False

    def isChecked(self):
        return self.value

    def setChecked(self, value):
        self.value = value


# Test double for a QtComboBox implementing value accessor methods
# noinspection PyPep8Naming
class DummyComboBox:
    def __init__(self):
        self.value = 0

    def currentIndex(self):
        return self.value

    def setCurrentIndex(self, value):
        self.value = value


# Test double for a QtTextField implementing value accessor methods
# noinspection PyPep8Naming
class DummyTextField:
    def __init__(self):
        self.value = ''

    def text(self):
        return self.value

    def setText(self, value):
        self.value = value


# Test double for a WtSpinBox implementing value accessor methods
# noinspection PyPep8Naming
class DummySpinBox:
    def __init__(self):
        self._value = 0

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value
