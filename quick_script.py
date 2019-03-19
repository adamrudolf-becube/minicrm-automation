# -*- coding: utf-8 -*-
# MiniCRM automation

from becube_crm_library import CrmData, load_api_info
from command_handler import CommandHandler
from tracing import trace
import os

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)


def run(crm_data):
    crm_data.clean_info_level_kiment()
    crm_data.handle_waiting_list()
    crm_data.register_new_applicants()
    trace("QUICK SCRIPT EXITED")


if __name__ == "__main__":
    command_handler = CommandHandler()
    crm_data = CrmData(system_id, api_key, command_handler)
    run(crm_data)