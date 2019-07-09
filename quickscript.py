# MiniCRM automation
"""
This module contains a main program to be run quite frequently.

This contains methods to keep the student statuses updated, and is also needed to send the first response after a
student applied to a course. This is why it is important to be fast: the amount of time a student has to wait for the
confirmation email is highly affected by the frequency of this script.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import os

from minicrm.commonfunctions import load_api_info
from minicrm.crmfacade import CrmFacade
from functionalities.cleaninfosent import clean_info_sent
from functionalities.handlewaitinglist import handle_waiting_list
from functionalities.registernewapplicants import register_new_applicants
from minicrm.requesthandler import RequestHandler
from minicrm.tracing import trace

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)


def run(crm_facade):
    """
    Calling this function will execute 3 of the functionalities:
        - clean_info_sent
        - handle_waiting_list
        - register_new_applicants

    For more details, see the documentation of those.

    This one is intended to be run frequently, for example once in every 10-15 minutes to make initial feedback faster.
    Please note that other factors also influence how fast the student gets their first reply.

    :param crm_facade: the CrmFacade instance this script is using for communication with a MiniCRM system.
    :type crm_facade: CrmFacade

    :return: None
    """

    clean_info_sent(crm_facade)
    handle_waiting_list(crm_facade)
    register_new_applicants(crm_facade)
    trace("QUICK SCRIPT EXITED")


if __name__ == "__main__":  # pragma: no cover
    request_handler = RequestHandler(system_id, api_key)
    crm_facade = CrmFacade(request_handler)
    run(crm_facade)
