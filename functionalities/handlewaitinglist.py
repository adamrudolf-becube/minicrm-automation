# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function

from minicrm.commonfunctions import add_element_to_commasep_list
from minicrm.tracing import stacktrace, trace, pretty_print

WAITING_LIST_STATE = "Várólistán van"
INFO_SENT_STATE = "INFO levél kiment"
CREATED_AT_FIELD = "CreatedAt"
STUDENT_NAME_FILED = "Name"
STUDENT_ID_FIELD = "Id"
STATUS_ID_FIELD = "StatusId"
CHOSEN_COURSE_FIELD = "MelyikTanfolyamErdekli"
MAX_HEADCOUNT_FIELD = "MaximalisLetszam"
CURRENT_HEADCOUNT_FIELD = "AktualisLetszam"
MAILS_TO_SEND_FIELD = "Levelkuldesek"
BEGINNER_INFO_MAIL_NAME = "Kezdő INFO levél"
ONE_PLACE_FREED_UP_MAIL_NAME = "Felszabadult egy hely"


@stacktrace
def handle_waiting_list(crm_facade):
    """
    Loops through all of the students in the waiting list and if there is
    free space in their course, it sends them the INFO letter and chenges their
    status. Also updates the headcounts of courses.
    """
    student_list = crm_facade.get_student_list_with_status(WAITING_LIST_STATE)
    trace("LOOPING THROUGH STUDENTS ON WAITING LIST")

    student_ordered_list = []

    for student in student_list:
        trace("GETTING DETAILED DATA FOR SORTING")
        student_data = crm_facade.get_student(student)
        student_ordered_list.append(student_data)

    student_ordered_list.sort(key=lambda student_instance: student_instance[CREATED_AT_FIELD])

    trace("ORDERED LIST IS")
    pretty_print(student_ordered_list)

    for student_data in student_ordered_list:
        trace("LOOPING THROUGH OERDERED LIST OF WAITING STUDENTS, CURRENTLY PROCESSING [{}]([{}])".
              format(student_data[STUDENT_ID_FIELD], student_data[STUDENT_NAME_FILED]))
        crm_facade.update_headcounts()
        trace("COURSE FOR " + student_data[STUDENT_NAME_FILED] + " IS " + student_data[CHOSEN_COURSE_FIELD])
        course_code = student_data[CHOSEN_COURSE_FIELD]
        course_data = crm_facade.get_course_by_course_code(course_code)

        is_there_free_spot = (course_data[MAX_HEADCOUNT_FIELD] - course_data[CURRENT_HEADCOUNT_FIELD]) > 0

        if is_there_free_spot:
            update_data = {}

            trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO COURSE.".
                  format(course_data[CURRENT_HEADCOUNT_FIELD], course_data[MAX_HEADCOUNT_FIELD]))

            update_data[MAILS_TO_SEND_FIELD] = add_element_to_commasep_list(
                student_data[MAILS_TO_SEND_FIELD],
                BEGINNER_INFO_MAIL_NAME
            )
            update_data[MAILS_TO_SEND_FIELD] = add_element_to_commasep_list(
                update_data[MAILS_TO_SEND_FIELD],
                ONE_PLACE_FREED_UP_MAIL_NAME
            )

            update_data[STATUS_ID_FIELD] = crm_facade.get_student_status_number_by_name(INFO_SENT_STATE)

            trace("DATA TO UPDATE:")
            pretty_print(update_data)

            crm_facade.set_student_data(student_data[STUDENT_ID_FIELD], update_data)

    crm_facade.update_headcounts()
