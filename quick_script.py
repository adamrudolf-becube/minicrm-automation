# -*- coding: utf-8 -*-
# MiniCRM automation

from functionalities.clean_info_sent import clean_info_level_kiment
from functionalities.handlewaitinglist import handle_waiting_list
from functionalities.registernewapplicants import register_new_applicants
from commonfunctions import load_api_info
from crmdata import CrmData
from command_handler import CommandHandler
from tracing import trace
import os

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)


def run(crm_data):
    clean_info_level_kiment(crm_data)
    handle_waiting_list(crm_data)
    register_new_applicants(crm_data)
    trace("QUICK SCRIPT EXITED")


if __name__ == "__main__":
    command_handler = CommandHandler(system_id, api_key)
    crm_data = CrmData(command_handler)
    run(crm_data)