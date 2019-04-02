# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function
from tracing import stacktrace, trace, pretty_print


@stacktrace
def handle_waiting_list(crm_data):
    """
    Loops through all of the students in the waiting list and if there is
    free space in their course, it sends them the INFO letter and chenges their
    status. Also updates the headcounts of courses.
    """
    student_list = crm_data.get_student_list_with_status("Várólistán van")
    trace("LOOPING THROUGH STUDENTS ON WAITING LIST")

    student_ordered_list = []

    for student in student_list:
        trace("GETTING DETAILED DATA FOR SORTING")
        student_data = crm_data.get_student(student)
        student_ordered_list.append(student_data)

    student_ordered_list.sort(key=lambda student_instance: student_instance["CreatedAt"])

    trace("ORDERED LIST IS")
    pretty_print(student_ordered_list)

    for student_data in student_ordered_list:
        trace("LOOPING THROUGH OERDERED LIST OF WAITING STUDENTS, CURRENTLY PROCESSING [{}]([{}])".
              format(student_data["Id"], student_data["Name"]))
        crm_data.update_headcounts()
        trace("COURSE FOR " + student_data["Name"] + " IS " + student_data["MelyikTanfolyamErdekli"])
        course_code = student_data["MelyikTanfolyamErdekli"]
        course_data = crm_data.get_course_by_course_code(course_code)

        is_there_free_spot = (course_data["MaximalisLetszam"] - course_data["AktualisLetszam"]) > 0

        if is_there_free_spot:
            update_data = {}

            trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO COURSE.".
                  format(course_data["AktualisLetszam"], course_data["MaximalisLetszam"]))

            update_data["Levelkuldesek"] = student_data[
                                               "Levelkuldesek"] + ", Kezdő INFO levél, Felszabadult egy hely"
            update_data["StatusId"] = crm_data.get_student_status_number_by_name("INFO levél kiment")

            trace("DATA TO UPDATE:")
            pretty_print(update_data)

            crm_data.set_student_data(student_data["Id"], update_data)

    crm_data.update_headcounts()
