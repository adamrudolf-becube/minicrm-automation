# -*- coding: utf-8 -*-
# MiniCRM automation

import os

from commonfunctions import load_api_info
from crmfacade import CrmFacade
from functionalities.cleaninfosent import clean_info_level_kiment
from functionalities.handlewaitinglist import handle_waiting_list
from functionalities.registernewapplicants import register_new_applicants
from requesthandler import RequestHandler
from tracing import trace

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)


def run(crm_facade):
    clean_info_level_kiment(crm_facade)
    handle_waiting_list(crm_facade)
    register_new_applicants(crm_facade)
    trace("QUICK SCRIPT EXITED")


if __name__ == "__main__":  # pragma: no cover
    request_handler = RequestHandler(system_id, api_key)
    crm_facade = CrmFacade(request_handler)
    run(crm_facade)