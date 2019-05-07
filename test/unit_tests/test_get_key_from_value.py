# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school
import unittest

from minicrm.commonfunctions import get_key_from_value


class TestGetKeyFromValue(unittest.TestCase):

    def test_get_key_from_value_returns_correct_key_if_unique_value(self):
        dictionary = {
            "one": "alpha",
            "two": "beta",
            "three": "gamma"
        }
        self.assertEqual(get_key_from_value(dictionary, "beta"), "two")

    def test_get_key_from_value_returns_a_key_if_not_unique_value(self):
        dictionary = {
            "one": "alpha",
            "two": "beta",
            "three": "gamma",
            "four": "beta"
        }
        self.assertEqual(get_key_from_value(dictionary, "beta"), "four")

    def test_get_key_from_value_raises_if_value_doesnt_exist(self):
        dictionary = {
            "one": "alpha",
            "two": "beta",
            "three": "gamma",
            "four": "beta"
        }

        with self.assertRaises(ValueError) as cm:
            get_key_from_value(dictionary, "omega")
