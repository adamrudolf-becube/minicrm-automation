__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import os

from functionalities.subfunctionalities.updatecoursedatesinstudents import \
    update_course_dates_for_all_students_for_that_course
from minicrm.commonfunctions import load_api_info
from minicrm.crmfacade import CrmFacade
from minicrm.requesthandler import RequestHandler
from minicrm.tracing import trace

currentDirectory = os.path.dirname(os.path.realpath(__file__))

API_INFO_JSON_FILE = currentDirectory + "/api_info.json"

system_id, api_key = load_api_info(API_INFO_JSON_FILE)


def run(crm_facade, course_code):
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

    update_course_dates_for_all_students_for_that_course(crm_facade, course_code)
    trace("RESCHEDULER EXITED")


if __name__ == "__main__":  # pragma: no cover
    request_handler = RequestHandler(system_id, api_key)
    crm_facade = CrmFacade(request_handler)
    run(crm_facade, "2019-7-I")
