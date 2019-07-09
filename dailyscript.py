# MiniCRM automation
"""
This module contains a main program to be run daily.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import os

from functionalities.sendscheduledmails import send_scheduled_emails
from functionalities.setcoursestates import set_course_states
from minicrm.commonfunctions import load_api_info
from minicrm.crmfacade import CrmFacade
from minicrm.requesthandler import RequestHandler
from minicrm.tracing import trace

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)


def run(crm_facade):
    """
    Calling this function will execute 2 of the functionalities:
        - send_scheduled_emails
        - set_course_states

    For more details, see the documentation of those.

    This one is intended to be run daily, in an appropriate time to send emails for the students.

    :param crm_facade: the CrmFacade instance this script is using for communication with a MiniCRM system.
    :type crm_facade: CrmFacade

    :return: None
    """

    send_scheduled_emails(crm_facade)
    set_course_states(crm_facade)
    trace("DAILY SCRIPT EXITED")


if __name__ == "__main__":  # pragma: no cover
    request_handler = RequestHandler(system_id, api_key)
    crm_facade = CrmFacade(request_handler)
    run(crm_facade)
