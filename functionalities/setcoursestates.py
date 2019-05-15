# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function

import datetime

from minicrm.commonfunctions import merge_dicts
from minicrm.tracing import stacktrace, trace, pretty_print

APPLICATION_OPEN_STATE = "Jelentkezés nyitva"
IN_PROGRESS_STATE = "Folyamatban"
RECENTLY_FINISHED_STATE = "Frissen végzett"
FINISHED_STATE = "Befejezett"
FIRST_OCCASION_FIELD_NAME = "ElsoAlkalom"
LAST_OCCASION_FIELD_NAME = "N10Alkalom"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
STATUS_ID_FIELD = "StatusId"


@stacktrace
def set_course_states(crm_facade):
    """
    Loops through the courses and sets their statuses according to first and last date
    """
    open_course_list = crm_facade.get_course_list_with_status(APPLICATION_OPEN_STATE)
    ongoing_course_list = crm_facade.get_course_list_with_status(IN_PROGRESS_STATE)
    freshly_finished = crm_facade.get_course_list_with_status(RECENTLY_FINISHED_STATE)

    course_list = merge_dicts(open_course_list, ongoing_course_list, freshly_finished)

    for course in course_list:
        course_data = crm_facade.get_course(course)

        pretty_print(course_data)

        update_data = {}

        try:
            if crm_facade.get_today() >= datetime.datetime.strptime(course_data[FIRST_OCCASION_FIELD_NAME], DATE_FORMAT):
                trace("Set: " + FIRST_OCCASION_FIELD_NAME)
                update_data[STATUS_ID_FIELD] = crm_facade.get_course_status_number_by_name(IN_PROGRESS_STATE)
            if crm_facade.get_today() >= datetime.datetime.strptime(course_data[LAST_OCCASION_FIELD_NAME], DATE_FORMAT):
                trace("Set: " + LAST_OCCASION_FIELD_NAME)
                update_data[STATUS_ID_FIELD] = crm_facade.get_course_status_number_by_name(RECENTLY_FINISHED_STATE)
            if crm_facade.get_today() >= datetime.datetime.strptime(course_data[LAST_OCCASION_FIELD_NAME],
                                                                    DATE_FORMAT) + datetime.timedelta(days=35):
                trace("Set: " + LAST_OCCASION_FIELD_NAME + " + 35 nap")
                update_data[STATUS_ID_FIELD] = crm_facade.get_course_status_number_by_name(FINISHED_STATE)
        except:
            trace("Missing date")

        if update_data:
            pretty_print(update_data)

            crm_facade.set_course_data(course, update_data)
        else:
            trace("NO DATA TO UPDATE")
