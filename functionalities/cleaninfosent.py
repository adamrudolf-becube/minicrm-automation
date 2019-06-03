# -*- coding: utf-8 -*-
"""
Cleans the pending students from "Info Sent" state.
"""


__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"


import datetime

from minicrm.commonfunctions import add_element_to_commasep_list
from minicrm.tracing import stacktrace, trace

INFO_SENT_STATE = "INFO levél kiment"
DID_NOT_FINALIZE_STATE = "Nem jelzett vissza"
STUDENT_NAME_FILED = "Name"
CHOSEN_COURSE_FIELD = "MelyikTanfolyamErdekli"
MAILS_TO_SEND_FIELD = "Levelkuldesek"
DEADLINE_FIELD = "VeglegesitesiHatarido"
STATUS_ID_FIELD = "StatusId"
ONE_DAY_MAIL_NAME = "Egy napod van jelentkezni"
ZERO_DAY_MAIL_NAME = "Ma kell jelentkezni"
WE_DELETED_YOU_MAIL_NAME = "Toroltunk"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

@stacktrace
def clean_info_sent(crm_facade):
    """
    Cleans the pending students from "Info Sent" state.

    Loops though all students in "Info Sent" ("INFO levél kiment" in Hungarian) status, and

    - If finalizing deadline -1 day is over, it sends a reminder

    - If finalizing deadline is over, it sends a reminder, raises a task for the responsible

    - If finalizing deadline + 1 ady is over, it sets student to "Did Not Finalize" ("Nem valaszolt"), and notifies responsibles

    Note that if billing info is filled (student finalized his/her application), student gets to "Course In Progress"
    ("Kurzus folyamatban") status. This logic is although not implemented by script, but the MiniCRM system itself. So
    this function only loops through the students who haven't done this yet.

    :param crm_facade: instance of the CrmFacade class this functionality will use to communicate with a MiniCRM system.

    :return: None
    """

    students_in_info_sent_state = crm_facade.get_student_list_with_status(INFO_SENT_STATE)
    trace("LOOPING THROUGH STUDENTS WITH INFO SENT OUT STATUS")

    for student in students_in_info_sent_state:
        crm_facade.update_headcounts()
        trace("HEADCOUNT UPDATE DONE")
        student_data = crm_facade.get_student(student)
        trace("COURSE FOR " + student_data[STUDENT_NAME_FILED] + " IS " + student_data[CHOSEN_COURSE_FIELD])

        update_data = {}

        mails_to_send = student_data[MAILS_TO_SEND_FIELD]
        mails_to_send_old = mails_to_send

        trace("STUDENT [" + student + "]([" + student_data["Name"] + "]) HAS NOT FINALIZED")

        deadline = datetime.datetime.strptime(student_data[DEADLINE_FIELD], DATE_FORMAT)

        trace("TODAY: {}, DEADLINE: {}".format(crm_facade.get_today(), deadline))

        if crm_facade.get_today() >= deadline + datetime.timedelta(days=-1):
            mails_to_send = add_element_to_commasep_list(mails_to_send, ONE_DAY_MAIL_NAME)

        if crm_facade.get_today() >= deadline:
            mails_to_send = add_element_to_commasep_list(mails_to_send, ZERO_DAY_MAIL_NAME)

        if crm_facade.get_today() >= deadline + datetime.timedelta(days=+1):
            mails_to_send = add_element_to_commasep_list(mails_to_send, WE_DELETED_YOU_MAIL_NAME)
            update_data[STATUS_ID_FIELD] = crm_facade.get_student_status_number_by_name(DID_NOT_FINALIZE_STATE)

        if mails_to_send != mails_to_send_old:
            trace("CHANGE IN " + MAILS_TO_SEND_FIELD)
            update_data[MAILS_TO_SEND_FIELD] = mails_to_send
        else:
            trace("NO CHANGE IN " + MAILS_TO_SEND_FIELD)

        if update_data:
            crm_facade.set_student_data(student, update_data)

    crm_facade.update_headcounts()
