"""
Contains commonly used free functions for the MiniCRM module.

This package contains functions, which are not strictly connected to any classes, but are used by minicrm package. These
can be also used directly by clients of minicrm package.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import datetime
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
"""Defines constant for the date format used by MiniCRM system."""


def load_api_info(api_info_json_file):
    """
    Opens the file given in the parameter and returns the api username and api key found in it.

    Api information (username and api key) should be stored separately from the source code. This script makes it
    possible to store the api information in a json file. This funtion is to load the stored information.

    The file needs to be structured as standard JSON. It has to contain an array, and the first element has to has
    "username" and "api_key". The function reads these two values and returns them as tuple.

    :param api_info_json_file: an absolute or relative path to a .json file in the above described format.

    :return: a tuple with the system_id (username) and api_key.
    """

    with open(api_info_json_file) as api_info_file:
        api_info = json.load(api_info_file)

    system_id = api_info[0]["username"]
    api_key = api_info[0]["api_key"]

    return system_id, api_key


def get_key_from_value(dictionary, dictionary_value):
    """
    Gets a python dictionary value and returns the corresponding index.

    - Returns the key if the value is present and unique

    - Returns one of the keys (undefined) if the value is present and not unique

    - Raises ValueError if the value is not present.

    :raise ValueError: if value is not present.

    :param dictionary: any Python dictionary.

    :param dictionary_value: any value which can be a key in the dictionary.

    :return: the key corresponding the given value. One of the (undefined) keys if not unique.
    """

    keys = dictionary.keys()
    values = dictionary.values()
    return keys[values.index(dictionary_value)]


def add_element_to_commasep_list(input_list, element):
    """
    Concatenates an element to a commaseparated list stored as a string.

    :param input_list: an original commaseparated list as a single string

    :param element: a new element to be concatenated to input_list

    :return:

    - The element if the input_list was an empty string
    - The input_list of element was already in the input_list
    - input_list and element joined by ", " otherwise

    """

    if input_list == "":
        out_list = element
    elif not element in input_list:
        out_list = input_list + ", " + element
    else:
        out_list = input_list
    return out_list


def merge_dicts(left_dict, right_dict, third_dict=None):
    """
    Merges two or three Python dictionaries to one dictionary.

    :param left_dict: first dictionary to be merged

    :param right_dict: second dictionary to be merged

    :param third_dict: third  dictionary to be merged. Defaults to None. If None, doesn't contribute to merging.

    :return: a single Python dictionary, containing a union of the keys and values of the dictionaries given in the
             parameters.
    """

    if third_dict:
        out_list = dict(dict(left_dict), **dict(right_dict))
        out_list = dict(dict(out_list), **dict(third_dict))
        return out_list
    else:
        return dict(dict(left_dict, **dict(right_dict)))


def date_is_not_less_than(crm_facade, reference_date, offset=0):
    """
    Compares a given date plus the given offset in days to the date returned by CrmFacade.get_today().

    Example usage:

    .. code-block:: python

      date_is_not_less_than(crm_facade, student_data[EIGTH_OCCASION_DATE_FIELD], -3)

    The code above returns True if today is not less than the 8th occasion of the student stored in student_data minus
    3 days.

    :param crm_facade: CrmFacade instance storing a date as today.

    :param reference_date: any given date in datetime.datetime format.

    :param offset: integer. Today is compared to reference_date + offset, where offset is given in days.
    :type int:

    :return: True if the date stored in crm_facade as today is not less than reference_date + offset, False otherwise.
    """

    return crm_facade.get_today() >= datetime.datetime.strptime(reference_date, DATE_FORMAT) + \
           datetime.timedelta(days=offset)


def date_is_not_more_than(crm_facade, reference_date, offset=0):
    """
    Compares a given date plus the given offset in days to the date returned by CrmFacade.get_today().

    Example usage:

    .. code-block:: python

      date_is_not_more_than(crm_facade, student_data[EIGTH_OCCASION_DATE_FIELD], -3)

    The code above returns True if today is not more than the 8th occasion of the student stored in student_data minus
    3 days.

    :param crm_facade: CrmFacade instance storing a date as today.

    :param reference_date: any given date in datetime.datetime format.

    :param offset: integer. Today is compared to reference_date + offset, where offset is given in days.
    :type int:

    :return: True if the date stored in crm_facade as today is not more than reference_date + offset, False otherwise.
    """

    return crm_facade.get_today() <= datetime.datetime.strptime(reference_date, DATE_FORMAT) + \
           datetime.timedelta(days=offset)


def commaseparated_list_is_subset_of(input_list, subset_list_testee, separator=', '):
    """
    Tests whether all elements of a given commaseparated list is also an element of another sommaseparated list.

    :param input_list: an existing list you would like to test whether a list of elements are contained or not. Elements
                       need to be separated by separator
    :type input_list: str

    :param subset_list_testee: a list of elements you want to find in input_list. Elements
                               need to be separated by separator
    :type subset_list_testee: str

    :param separator: string which separates elements of both input_list and subset_list_testee. Defaults to ', '
    :type separator: str

    :return: True if every element of subset_list_testee is also an element of input_list, and False otherwise.
    """
    separated_input_list = input_list.split(separator)
    separated_subset_list_testee = subset_list_testee.split(separator)

    for element in separated_subset_list_testee:
        if element not in separated_input_list and element != "":
            return False

    return True


def all_element_of_commaseparated_list_is_expluded_from(input_list, subset_list_testee, separator=', '):
    """
    Tests whether all elements of a given commaseparated list is excpluded from another sommaseparated list.

    :param input_list: an existing list you would like to test whether a list of elements are excluded or not. Elements
                       need to be separated by separator
    :type input_list: str

    :param subset_list_testee: a list of elements you want to be excluded from input_list. Elements
                               need to be separated by separator
    :type subset_list_testee: str

    :param separator: string which separates elements of both input_list and subset_list_testee. Defaults to ', '
    :type separator: str

    :return: True if none of the elements of subset_list_testee are an element of input_list, and False otherwise.
    """
    separated_input_list = input_list.split(separator)
    separated_subset_list_testee = subset_list_testee.split(separator)

    for element in separated_subset_list_testee:
        if element in separated_input_list and element != "":
            return False

    return True
