# -*- coding: utf-8 -*-
# MiniCRM automation
# -*- coding: utf-8 -*-
# MiniCRM automation

import os

from minicrm.commonfunctions import load_api_info
from minicrm.crmfacade import CrmFacade
from functionalities.sendscheduledmails import send_scheduled_emails
from functionalities.setcoursestates import set_course_states
from minicrm.requesthandler import RequestHandler
from minicrm.tracing import trace

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)


def run(crm_facade):
    send_scheduled_emails(crm_facade)
    set_course_states(crm_facade)
    trace("DAILY SCRIPT EXITED")


if __name__ == "__main__":  # pragma: no cover
    request_handler = RequestHandler(system_id, api_key)
    crm_facade = CrmFacade(request_handler)
    run(crm_facade)
