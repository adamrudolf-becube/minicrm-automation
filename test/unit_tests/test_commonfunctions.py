"""
Contains unittests for all of the functions in minicrm.commonfunctions.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import unittest

from minicrm.commonfunctions import add_element_to_commasep_list,\
    get_key_from_value,\
    commaseparated_list_is_subset_of,\
    all_element_of_commaseparated_list_is_expluded_from


class TestAddElementToCommaseparatedList(unittest.TestCase):
    """
    Contains tests for add_element_to_commasep_list()
    """

    def test_if_input_list_is_empty_output_is_same_as_new_element(self):
        """When an element is added to an empty list (empty string) the output list is equel to the added element."""
        input_list = ""
        added_element = "new element"
        self.assertEqual(add_element_to_commasep_list(input_list, added_element), added_element)

    def test_if_input_list_has_one_element_new_element_is_concatenated_by_comma_and_space(self):
        """
        When an element is added to another element (single element comma separated list) the output list is the two
        elements concatenated by the given separator.
        """

        input_list = "old element"
        added_element = "new element"
        expected_out_list = "old element, new element"
        self.assertEqual(add_element_to_commasep_list(input_list, added_element), expected_out_list)

    def test_if_input_list_has_multiple_elements_new_element_is_concatenated_by_comma_and_space(self):
        """
        When an element is added to a multi element comma separated list, the output list is the new element
        concatenated to the end of the list by the given separator.
        """

        input_list = "first old element, second old element"
        added_element = "new element"
        expected_out_list = "first old element, second old element, new element"
        self.assertEqual(add_element_to_commasep_list(input_list, added_element), expected_out_list)

    def test_if_new_element_is_already_in_the_list_out_list_is_same_as_input_list(self):
        """
        When the added element is already in the comma separated list, the output list is equal to the input list.
        """

        input_list = "first old element, new element, second old element"
        added_element = "new element"
        self.assertEqual(add_element_to_commasep_list(input_list, added_element), input_list)


class TestGetKeyFromValue(unittest.TestCase):
    """
    Contains tests for minicrm.commonfunctions.get_key_from_value()
    """

    def test_get_key_from_value_returns_correct_key_if_unique_value(self):
        """When searched value exists in dictionary and is unique, corresponding key is returned."""
        dictionary = {
            "one": "alpha",
            "two": "beta",
            "three": "gamma"
        }
        self.assertEqual(get_key_from_value(dictionary, "beta"), "two")

    def test_get_key_from_value_returns_a_key_if_not_unique_value(self):
        """When searched value exists in dictionary and is not unique, one of the keys is returned."""
        dictionary = {
            "one": "alpha",
            "two": "beta",
            "three": "gamma",
            "four": "beta"
        }
        self.assertEqual(get_key_from_value(dictionary, "beta"), "four")

    def test_get_key_from_value_raises_if_value_doesnt_exist(self):
        """When nonexistent value is searched, ValueError is raised."""
        dictionary = {
            "one": "alpha",
            "two": "beta",
            "three": "gamma",
            "four": "beta"
        }

        with self.assertRaises(ValueError) as cm:
            get_key_from_value(dictionary, "omega")


class TestCommaseparatedListIsSubsetOf(unittest.TestCase):
    """
    Contains tests for minicrm.commonfunctions.commaseparated_list_is_subset_of()
    """

    def test_returns_true_for_empty_lists_and_default_separator(self):
        """When commaseparated_list_is_subset_of is called with two empty stirings and default separator, returns True"""
        self.assertTrue(commaseparated_list_is_subset_of("", ""))

    def test_returns_true_for_empty_lists_and_nondefault_separator(self):
        """
        When commaseparated_list_is_subset_of is called with two empty stirings and nondefault separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of("", "", "asdf"))

    def test_returns_true_for_single_element_inputlist_and_empty_testee_list_and_default_separator(self):
        """
        When commaseparated_list_is_subset_of is called with single element input list and empty testee string and
        default separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of("single", ""))

    def test_returns_true_for_single_element_inputlist_and_empty_testee_list_and_nondefault_separator(self):
        """
        When commaseparated_list_is_subset_of is called with single element input list and empty testee string and
        nondefault separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of("single", "", "asdf"))

    def test_returns_true_for_single_element_inputlist_and_same_testee_list_and_default_separator(self):
        """
        When commaseparated_list_is_subset_of is called with single element input list and the same testee string and
        default separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of("single", "single"))

    def test_returns_true_for_single_element_inputlist_and_same_testee_list_and_nondefault_separator(self):
        """
        When commaseparated_list_is_subset_of is called with single element input list and the same testee string and
        nondefault separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of("single", "single", "asdf"))

    def test_returns_true_for_multiple_element_inputlist_and_single_element_testee_list_element_contained_and_default_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and the one element testee,
        where the element is contained by the input list and default separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of("alpha, beta", "beta"))

    def test_returns_true_for_multiple_element_inputlist_and_single_element_testee_list_element_contained_and_nondefault_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and the one element testee,
        where the element is contained by the input list and nondefault separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of("alphaasdfbeta", "beta", "asdf"))

    def test_returns_true_for_true_subset_default_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and the multiple, but less
        element testee, where all elements are contained by the input list and default separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of(
            "alpha, beta, gamma, delta, epsilon",
            "delta, epsilon, beta"))

    def test_returns_true_for_true_subset_nondefault_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and the multiple, but less
        element testee, where all elements are contained by the input list and nondefault separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of(
            "alpha.beta.gamma.delta.epsilon",
            "delta.epsilon.beta",
            "."
        ))

    def test_returns_true_for_true_equal_lists_default_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and same testee, and default
        separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of(
            "alpha, beta, gamma, delta, epsilon",
            "alpha, beta, gamma, delta, epsilon"))

    def test_returns_true_for_true_equal_lists_nondefault_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and same testee, and nondefault
        separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of(
            "alphaEbetaEgammaEdeltaEepsilon",
            "alphaEbetaEgammaEdeltaEepsilon",
            "E"
        ))

    def test_returns_true_for_true_equal_but_unordered_lists_default_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and same testee, but different
        order and default separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of(
            "alpha, beta, gamma, delta, epsilon",
            "gamma, alpha, beta, delta, epsilon"
        ))

    def test_returns_true_for_true_equal_but_unordered_lists_nondefault_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and same testee, but different
        order and nondefault separator, returns True
        """
        self.assertTrue(commaseparated_list_is_subset_of(
            "alphaEbetaEgammaEdeltaEepsilon",
            "gammaEalphaEbetaEdeltaEepsilon",
            "E"
        ))

    def test_returns_false_for_empty_input_list_and_one_element_testee_list(self):
        """
        For a one element testee list and empty input list, and default separator, returns false
        """
        self.assertFalse(commaseparated_list_is_subset_of("", "element"))

    def test_returns_false_for_empty_input_list_and_one_element_testee_list_nondefault_separator(self):
        """
        For a one element testee list and empty input list, and nondefault separator, returns false
        """
        self.assertFalse(commaseparated_list_is_subset_of("", "element", "asdf"))

    def test_returns_false_for_one_element_input_list_and_different_one_element_testee_list(self):
        """
        For a one element testee list and different one element input list, and default separator, returns false
        """
        self.assertFalse(commaseparated_list_is_subset_of("oneelement", "otherelement"))

    def test_returns_false_for_one_element_input_list_and_different_one_element_testee_list_nondefault_separator(self):
        """
        For a one element testee list and different one element input list, and nondefault separator, returns false
        """
        self.assertFalse(commaseparated_list_is_subset_of("oneelement", "otherelement", "asdf"))

    def test_returns_false_for_one_missing_element(self):
        """
        Multiple element input list, multiple element testee list, one testee element is missing, returns false
        """
        self.assertFalse(commaseparated_list_is_subset_of("alpha, beta, delta", "alpha, beta, gamma, delta"))

    def test_returns_false_for_one_missing_element_nondefault_separator(self):
        """
        Multiple element input list, multiple element testee list, one testee element is missing, returns false,
        nondefault spearator
        """
        self.assertFalse(commaseparated_list_is_subset_of("alpha.beta.delta", "alpha.beta.gamma.delta", "."))


class TestAllElementOfCommaseparatedListIsExpludedFrom(unittest.TestCase):
    """
    Contains tests for minicrm.commonfunctions.all_element_of_commaseparated_list_is_expluded_from()
    """

    def test_returns_true_for_empty_lists_and_default_separator(self):
        """When all_element_of_commaseparated_list_is_expluded_from is called with two empty stirings and default
        separator, returns True"""
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("", ""))

    def test_returns_true_for_empty_lists_and_nondefault_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with two empty stirings and nondefault
        separator, returns True
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("", "", "asdf"))

    def test_returns_true_for_single_element_inputlist_and_empty_testee_list_and_default_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with single element input list and empty
        testee string and default separator, returns True
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("single", ""))

    def test_returns_true_for_single_element_inputlist_and_empty_testee_list_and_nondefault_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with single element input list and empty
        testee string and nondefault separator, returns True
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("single", "", "asdf"))

    def test_returns_false_for_single_element_inputlist_and_same_testee_list_and_default_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with single element input list and the same
        testee string and default separator, returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from("single", "single"))

    def test_returns_false_for_single_element_inputlist_and_same_testee_list_and_nondefault_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with single element input list and the same
        testee string and nondefault separator, returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from("single", "single", "asdf"))

    def test_returns_false_for_multiple_element_inputlist_and_single_element_testee_list_element_contained_and_default_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with multiple element input list and the one
        element testee, where the element is contained by the input list and default separator, returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from("alpha, beta", "beta"))

    def test_returns_false_for_multiple_element_inputlist_and_single_element_testee_list_element_contained_and_nondefault_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with multiple element input list and the one
        element testee, where the element is contained by the input list and nondefault separator, returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from("alphaasdfbeta", "beta", "asdf"))

    def test_returns_false_for_true_subset_default_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with multiple element input list and the
        multiple, but less element testee, where all elements are contained by the input list and default separator,
        returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from(
            "alpha, beta, gamma, delta, epsilon",
            "delta, epsilon, beta"))

    def test_returns_false_for_true_subset_nondefault_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with multiple element input list and the
        multiple, but less element testee, where all elements are contained by the input list and nondefault separator,
        returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from(
            "alpha.beta.gamma.delta.epsilon",
            "delta.epsilon.beta",
            "."
        ))

    def test_returns_false_for_true_equal_lists_default_separator(self):
        """
        When commaseparatedall_element_of_commaseparated_list_is_expluded_from_list_is_subset_of is called with multiple
        element input list and same testee, and default separator, returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from(
            "alpha, beta, gamma, delta, epsilon",
            "alpha, beta, gamma, delta, epsilon"))

    def test_returns_false_for_true_equal_lists_nondefault_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with multiple element input list and same
        testee, and nondefault separator, returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from(
            "alphaEbetaEgammaEdeltaEepsilon",
            "alphaEbetaEgammaEdeltaEepsilon",
            "E"
        ))

    def test_returns_false_for_true_equal_but_unordered_lists_default_separator(self):
        """
        When all_element_of_commaseparated_list_is_expluded_from is called with multiple element input list and same
        testee, but different order and default separator, returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from(
            "alpha, beta, gamma, delta, epsilon",
            "gamma, alpha, beta, delta, epsilon"
        ))

    def test_returns_false_for_true_equal_but_unordered_lists_nondefault_separator(self):
        """
        When commaseparated_list_is_subset_of is called with multiple element input list and same testee, but different
        order and nondefault separator, returns False
        """
        self.assertFalse(all_element_of_commaseparated_list_is_expluded_from(
            "alphaEbetaEgammaEdeltaEepsilon",
            "gammaEalphaEbetaEdeltaEepsilon",
            "E"
        ))

    def test_returns_true_for_empty_input_list_and_one_element_testee_list(self):
        """
        For a one element testee list and empty input list, and default separator, returns True
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("", "element"))

    def test_returns_true_for_empty_input_list_and_one_element_testee_list_nondefault_separator(self):
        """
        For a one element testee list and empty input list, and nondefault separator, returns True
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("", "element", "asdf"))

    def test_returns_true_for_one_element_input_list_and_different_one_element_testee_list(self):
        """
        For a one element testee list and different one element input list, and default separator, returns True
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("oneelement", "otherelement"))

    def test_returns_true_for_one_element_input_list_and_different_one_element_testee_list_nondefault_separator(self):
        """
        For a one element testee list and different one element input list, and nondefault separator, returns True
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("oneelement", "otherelement", "asdf"))

    def test_returns_false_for_one_missing_element(self):
        """
        Multiple element input list, multiple element testee list, one testee element is missing, returns false
        """
        self.assertFalse(
            all_element_of_commaseparated_list_is_expluded_from("alpha, beta, delta", "alpha, beta, gamma, delta"))

    def test_returns_false_for_one_missing_element_nondefault_separator(self):
        """
        Multiple element input list, multiple element testee list, one testee element is missing, returns false,
        nondefault spearator
        """
        self.assertFalse(
            all_element_of_commaseparated_list_is_expluded_from("alpha.beta.delta", "alpha.beta.gamma.delta", "."))

    def test_empty_input_list_multielement_testee_list_returns_true_nondefault(self):
        """
        Multiple element testee list, empty input list returns true with default separator
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("", "alpha, beta, gamma, delta"))

    def test_empty_input_list_multielement_testee_list_returns_true_nondefault_separator(self):
        """
        Multiple element testee list, empty input list returns true with nondefault separator
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("", "alpha.beta.gamma.delta", "."))

    def test_totally_different_lists_returns_true(self):
        """
        Multiple element testee list, multiple element, but totally different input list returns true with default
        separator
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("alpha, beta, gamma", "delta, epsilon"))

    def test_totally_different_lists_returns_true_nondefault_separator(self):
        """
        Multiple element testee list, multiple element, but totally different input list returns true with nondefault
        separator
        """
        self.assertTrue(all_element_of_commaseparated_list_is_expluded_from("alpha.beta.gamma", "delta.epsilon", "."))

    def test_multiple_element_lists_one_overlap_returns_false(self):
        """
        Multiple element testee list, multiple element input list, one common element returns false with default
        separator
        """
        self.assertFalse(
            all_element_of_commaseparated_list_is_expluded_from("alpha, beta, gamma", "delta, gamma, epsilon"))

    def test_totally_different_lists_returns_true_nondefault_separator(self):
        """
        Multiple element testee list, multiple element input list, one common element returns false with nondefault
        separator
        """
        self.assertFalse(
            all_element_of_commaseparated_list_is_expluded_from("alpha.beta.gamma", "delta.gamma.epsilon", "."))
