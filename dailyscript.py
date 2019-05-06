# -*- coding: utf-8 -*-
# MiniCRM automation
# -*- coding: utf-8 -*-
# MiniCRM automation

import os

from functionalities.sendscheduledmails import send_scheduled_emails
from functionalities.setcoursestates import set_course_states
from commonfunctions import load_api_info
from crmfacade import CrmData
from requesthandler import CommandHandler
from tracing import trace

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)


def run(crm_data):
    send_scheduled_emails(crm_data)
    set_course_states(crm_data)
    trace("DAILY SCRIPT EXITED")


if __name__ == "__main__": # pragma: no cover
    command_handler = CommandHandler(system_id, api_key)
    crm_data = CrmData(command_handler)
    run(crm_data)
