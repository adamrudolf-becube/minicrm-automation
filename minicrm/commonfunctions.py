# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

import datetime
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_api_info(api_info_json_file):
    with open(api_info_json_file) as api_info_file:
        api_info = json.load(api_info_file)

    system_id = api_info[0]["username"]
    api_key = api_info[0]["api_key"]

    return system_id, api_key


def get_key_from_value(dictionary, dictionary_value):
    """
    Gets a python dictionary value and returns the corresponding index
    """
    keys = dictionary.keys()
    values = dictionary.values()
    return keys[values.index(dictionary_value)]


def add_element_to_commasep_list(input_list, element):
    if input_list == "":
        out_list = element
    elif not element in input_list:
        out_list = input_list + ", " + element
    else:
        out_list = input_list
    return out_list


def merge_dicts(left_dict, right_dict, third_dict=None):
    if third_dict:
        out_list = dict(dict(left_dict), **dict(right_dict))
        out_list = dict(dict(out_list), **dict(third_dict))
        return out_list
    else:
        return dict(dict(left_dict, **dict(right_dict)))


def date_is_not_less_than(crm_facade, reference_date, offset=0):
    return crm_facade.get_today() >= datetime.datetime.strptime(reference_date, DATE_FORMAT) + \
           datetime.timedelta(days=offset)
