# -*- coding: utf-8 -*-
"""
Contains a function to enroll a student to a selected course.

BeCube MiniCRM automation project.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

from minicrm.commonfunctions import add_element_to_commasep_list
from minicrm.tracing import pretty_print
from minicrm.tracing import stacktrace, trace

INFO_SENT_STATE = "INFO levél kiment"
WAITING_LIST_STATE = "Várólistán van"
APPLIED_STATE = "Jelentkezett"
STUDENT_NAME_FILED = "Name"
MAILS_TO_SEND_FIELD = "Levelkuldesek"
MAX_HEADCOUNT_FIELD = "MaximalisLetszam"
CURRENT_HEADCOUNT_FIELD = "AktualisLetszam"
STATUS_ID_FIELD = "StatusId"
STUDENT_ID_FIELD = "Id"
COURSE_TYPE_FIELD = "TanfolyamTipusa"
CHOSEN_COURSE_FIELD = "MelyikTanfolyamErdekli"
BEGINNER_COURSE_TYPE = "Kezdő programozó tanfolyam"
ADVANCED_COURSE_TYPE = "Haladó programozó tanfolyam"
WAITING_LIST_MAIL_NAME = "Várólista"
BEGINNER_INFO_MAIL_NAME = "Kezdő INFO levél"
ADVANCED_INFO_MAIL_NAME = "Haladó INFO levél"


@stacktrace
def enroll_student_to_course(crm_facade, student_data, course_data):
    """
    This function enrolls the student to the given course.

    - It copies all needed information from the course's data to the student's data in the system.
    - It sends the first response to the given student.
    - It puts the student to "INFO sent" (INFO levél kiment) state.

    This mail is information about the course. The function assembles
    the initial mail by fetching information about the course and the location. Based on the course data this function
    also decides whether it has to be a beginner or an advanced INFO mail.

    :param crm_facade: instance of the CrmFacade class this functionality will use to communicate with a MiniCRM system.
    :type crm_facade: CrmFacade

    :param student_data: full JSON array of a student as stored in the MiniCRM system.
    :type student_data: dict

    :param course_data: full JSON array of a course as stored in the MiniCRM system. The student will be enrolled to
    this course.
    :type course_data: dict

    :return: None
    """

    crm_facade.fill_student_data(student_data, course_data)

    update_data = {}

    trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO COURSE.".
          format(course_data[CURRENT_HEADCOUNT_FIELD], course_data[MAX_HEADCOUNT_FIELD]))

    trace("TYPE OF COURSE IS: [{}] ".format(course_data[COURSE_TYPE_FIELD]))

    if course_data[COURSE_TYPE_FIELD] == BEGINNER_COURSE_TYPE:
        update_data[MAILS_TO_SEND_FIELD] = add_element_to_commasep_list(
            student_data[MAILS_TO_SEND_FIELD],
            BEGINNER_INFO_MAIL_NAME
        )

    elif course_data[COURSE_TYPE_FIELD] == ADVANCED_COURSE_TYPE:
        update_data[MAILS_TO_SEND_FIELD] = add_element_to_commasep_list(
            student_data[MAILS_TO_SEND_FIELD],
            ADVANCED_INFO_MAIL_NAME
        )

    update_data[STATUS_ID_FIELD] = crm_facade.get_student_status_number_by_name(INFO_SENT_STATE)

    trace("DATA TO UPDATE:")
    pretty_print(update_data)

    crm_facade.set_student_data(student_data[STUDENT_ID_FIELD], update_data)
