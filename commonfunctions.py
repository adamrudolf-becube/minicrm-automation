import json


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
