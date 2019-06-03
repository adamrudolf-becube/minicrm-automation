# -*- coding: utf-8 -*-
"""
Updates the course stated based on their set states.

BeCube MiniCRM automation project.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

from minicrm.commonfunctions import merge_dicts, date_is_not_less_than
from minicrm.tracing import stacktrace, trace, pretty_print

APPLICATION_OPEN_STATE = "Jelentkezés nyitva"
IN_PROGRESS_STATE = "Folyamatban"
RECENTLY_FINISHED_STATE = "Frissen végzett"
FINISHED_STATE = "Befejezett"
FIRST_OCCASION_FIELD_NAME = "ElsoAlkalom"
LAST_OCCASION_FIELD_NAME = "N10Alkalom"
STATUS_ID_FIELD = "StatusId"


@stacktrace
def set_course_states(crm_facade):
    """
    Loops through the courses and sets their statuses according to first and last date.

    - If current date is not less than course's 1st occasion, function sets the state to "In progress" ("Kurzus
      folyamatban").
    - If current date is not less than course's last occasion, function sets the state to "Recently finished" ("Frissen
      vegzett"). This state if to make it possible to make certain actions (make statistics / calculate salaries)
      monthly and the monthly script has to loop through the in progress and recently finished courses.
    - If current date is not less than course's last occasion plus 35 days, function sets the state to "Finished"
      ("Befejezett").

    :param crm_facade: instance of the CrmFacade class this functionality will use to communicate with a MiniCRM system.

    :return: None
    """
    open_courses = crm_facade.get_course_list_with_status(APPLICATION_OPEN_STATE)
    ongoing_courses = crm_facade.get_course_list_with_status(IN_PROGRESS_STATE)
    freshly_finished_courses = crm_facade.get_course_list_with_status(RECENTLY_FINISHED_STATE)

    courses = merge_dicts(open_courses, ongoing_courses, freshly_finished_courses)

    for course in courses:
        course_data = crm_facade.get_course(course)

        pretty_print(course_data)

        update_data = {}

        try:
            if date_is_not_less_than(crm_facade, course_data[FIRST_OCCASION_FIELD_NAME]):
                trace("Set: " + FIRST_OCCASION_FIELD_NAME)
                update_data[STATUS_ID_FIELD] = crm_facade.get_course_status_number_by_name(IN_PROGRESS_STATE)
            if date_is_not_less_than(crm_facade, course_data[LAST_OCCASION_FIELD_NAME]):
                trace("Set: " + LAST_OCCASION_FIELD_NAME)
                update_data[STATUS_ID_FIELD] = crm_facade.get_course_status_number_by_name(RECENTLY_FINISHED_STATE)
            if date_is_not_less_than(crm_facade, course_data[LAST_OCCASION_FIELD_NAME], +35):
                trace("Set: " + LAST_OCCASION_FIELD_NAME + " + 35 nap")
                update_data[STATUS_ID_FIELD] = crm_facade.get_course_status_number_by_name(FINISHED_STATE)
        except:
            trace("Missing date")

        if update_data:
            pretty_print(update_data)
            crm_facade.set_course_data(course, update_data)
        else:
            trace("NO DATA TO UPDATE")
