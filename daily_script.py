# -*- coding: utf-8 -*-
# MiniCRM automation
# -*- coding: utf-8 -*-
# MiniCRM automation

from becube_crm_library import CrmData, load_api_info, send_scheduled_emails
from command_handler import CommandHandler
from tracing import trace
import os

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)

def run(crm_data):
    send_scheduled_emails(crm_data)
    crm_data.set_course_states()
    trace("DAILY SCRIPT EXITED")


if __name__ == "__main__":
    command_handler = CommandHandler()
    crm_data = CrmData(system_id, api_key, command_handler)
    run(crm_data)
