import unittest
from becube_crm_library import get_key_from_value
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"


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