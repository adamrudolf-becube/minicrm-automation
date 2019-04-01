# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function
import datetime
from tracing import stacktrace, trace, pretty_print


@stacktrace
def set_course_states(crm_data):
    """
    Loops through the courses and sets their statuses according to first and last date
    """
    open_course_list = crm_data.tanfolymok.query_project_list_with_status("Jelentkezés nyitva")["Results"]
    ongoing_course_list = crm_data.tanfolymok.query_project_list_with_status("Folyamatban")["Results"]
    freshly_finished = crm_data.tanfolymok.query_project_list_with_status("Frissen végzett")["Results"]

    course_list = dict(dict(open_course_list), **dict(ongoing_course_list))
    course_list = dict(dict(course_list), **dict(freshly_finished))

    for course in course_list:
        course_data = crm_data.get_project(course)

        pretty_print(course_data)

        update_data = {}

        try:
            if crm_data.today >= datetime.datetime.strptime(course_data["ElsoAlkalom"], "%Y-%m-%d %H:%M:%S"):
                trace("Set: ElsoAlkalom")
                update_data["StatusId"] = crm_data.tanfolymok.get_status_number_by_name("Folyamatban")
            if crm_data.today >= datetime.datetime.strptime(course_data["N10Alkalom"], "%Y-%m-%d %H:%M:%S"):
                trace("Set: N10Alkalom")
                update_data["StatusId"] = crm_data.tanfolymok.get_status_number_by_name("Frissen végzett")
            if crm_data.today >= datetime.datetime.strptime(course_data["N10Alkalom"],
                                                        "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=35):
                trace("Set: N10Alkalom + 35 nap")
                update_data["StatusId"] = crm_data.tanfolymok.get_status_number_by_name("Befejezett")
        except:
            trace("Missing date")

        if update_data:
            pretty_print(update_data)

            crm_data.command_handler.get_json_array_for_command(
                crm_data.command_mapper.set_project_data(course, update_data))
        else:
            trace("NO DATA TO UPDATE")
