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
    Gets all students for a given course, reads the dates of the course, and copies it to the student data of all.

    Sometimes course dates change even after many students have been enrolled to it. Students keep a copy of the
    course dates, but it doesn't get automatically updated, so an additional action is needed. This is for that.

    :param crm_facade: the CrmFacade instance this script is using for communication with a MiniCRM system.
    :type crm_facade: CrmFacade

    :param course_code: the code of the course where the dates changed recently, for example "2019-4-Q"
    :type course_code: str

    :return: None
    """

    update_course_dates_for_all_students_for_that_course(crm_facade, course_code)
    trace("RESCHEDULER EXITED")


if __name__ == "__main__":  # pragma: no cover
    request_handler = RequestHandler(system_id, api_key)
    crm_facade = CrmFacade(request_handler)
    run(crm_facade, "2019-7-I")
