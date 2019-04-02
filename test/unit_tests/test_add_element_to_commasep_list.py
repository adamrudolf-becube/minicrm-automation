import unittest
from commonfunctions import add_element_to_commasep_list


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
