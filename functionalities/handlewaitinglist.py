# -*- coding: utf-8 -*-
"""
Cleans the pending students from "Info Sent" state.

BeCube MiniCRM automation project.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

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
    Loops through the students in waiting list and checks whether they got into the courses.

    Loops through all of the students in the waiting list and if there is
    free space in their course, it sends them the INFO letter and changes their
    status to INO sent. Also updates the headcounts of courses.

    Students will get to the courses in the order of original application.

    :param crm_facade: instance of the CrmFacade class this functionality will use to communicate with a MiniCRM system.

    :return: None
    """

    waiting_list_students = crm_facade.get_student_list_with_status(WAITING_LIST_STATE)
    trace("LOOPING THROUGH STUDENTS ON WAITING LIST")

    waiting_list_students_ordered = []

    for student in waiting_list_students:
        trace("GETTING DETAILED DATA FOR SORTING")
        student_data = crm_facade.get_student(student)
        waiting_list_students_ordered.append(student_data)

    waiting_list_students_ordered.sort(key=lambda student_instance: student_instance[CREATED_AT_FIELD])

    trace("ORDERED LIST IS")
    pretty_print(waiting_list_students_ordered)

    for student_data in waiting_list_students_ordered:
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

            # TODO why only beginner?
            update_data[MAILS_TO_SEND_FIELD] = add_element_to_commasep_list(
                update_data[MAILS_TO_SEND_FIELD],
                ONE_PLACE_FREED_UP_MAIL_NAME
            )

            update_data[STATUS_ID_FIELD] = crm_facade.get_student_status_number_by_name(INFO_SENT_STATE)

            trace("DATA TO UPDATE:")
            pretty_print(update_data)

            crm_facade.set_student_data(student_data[STUDENT_ID_FIELD], update_data)

    crm_facade.update_headcounts()
