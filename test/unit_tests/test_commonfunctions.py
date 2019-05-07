import unittest

from minicrm.commonfunctions import add_element_to_commasep_list, get_key_from_value


class TestAddElementToCommaseparatedList(unittest.TestCase):

    def test_if_input_list_is_empty_output_is_same_as_new_element(self):
        input_list = ""
        added_element = "new element"
        self.assertEqual(add_element_to_commasep_list(input_list, added_element), added_element)

    def test_if_input_list_has_one_element_new_element_is_concatenated_by_comma_and_space(self):
        input_list = "old element"
        added_element = "new element"
        expected_out_list = "old element, new element"
        self.assertEqual(add_element_to_commasep_list(input_list, added_element), expected_out_list)

    def test_if_input_list_has_multiple_elements_new_element_is_concatenated_by_comma_and_space(self):
        input_list = "first old element, second old element"
        added_element = "new element"
        expected_out_list = "first old element, second old element, new element"
        self.assertEqual(add_element_to_commasep_list(input_list, added_element), expected_out_list)

    def test_if_new_element_is_already_in_the_list_out_list_is_same_as_input_list(self):
        input_list = "first old element, new element, second old element"
        added_element = "new element"
        self.assertEqual(add_element_to_commasep_list(input_list, added_element), input_list)


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
