# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function

import datetime

from minicrm.commonfunctions import *
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

@stacktrace
def clean_info_level_kiment(crm_data):
    """
    Checks all students in "INFO levöl kiment" status, and
    - NOT DONE BY SCRIPT If billing info is filled, student gets to "Kurzus folyamatban" NOT DONE BY SCRIPT, autmated in MiniCRTM
    - If finalizing deadline -1 day is over, it sends a reminder
    - If finalizing deadline is over, it sends a reminder, raises a task for the responsible
    - If finalizing deadline + 1 ady is over, it sets student to "Nem valaszolt", and notifies responsible
    """

    student_list = crm_data.get_student_list_with_status(INFO_SENT_STATE)
    trace("LOOPING THROUGH STUDENTS WITH INFO SENT OUT STATUS")

    for student in student_list:
        crm_data.update_headcounts()
        trace("HEADCOUNT UPDATE DONE")
        student_data = crm_data.get_student(student)
        trace("COURSE FOR " + student_data[STUDENT_NAME_FILED] + " IS " + student_data[CHOSEN_COURSE_FIELD])

        update_data = {}

        levelkuldesek = student_data[MAILS_TO_SEND_FIELD]
        levelkuldesek_old = levelkuldesek

        trace("STUDENT [" + student + "]([" + student_data["Name"] + "]) HAS NOT FINALIZED")

        deadline = datetime.datetime.strptime(student_data[DEADLINE_FIELD], "%Y-%m-%d %H:%M:%S")

        trace("TODAY: {}, DEADLINE: {}".format(crm_data.get_today(), deadline))

        if crm_data.get_today() >= deadline + datetime.timedelta(days=-1):
            levelkuldesek = add_element_to_commasep_list(levelkuldesek, ONE_DAY_MAIL_NAME)

        if crm_data.get_today() >= deadline:
            levelkuldesek = add_element_to_commasep_list(levelkuldesek, ZERO_DAY_MAIL_NAME)

        if crm_data.get_today() >= deadline + datetime.timedelta(days=+1):
            levelkuldesek = add_element_to_commasep_list(levelkuldesek, WE_DELETED_YOU_MAIL_NAME)
            update_data[STATUS_ID_FIELD] = crm_data.get_student_status_number_by_name(DID_NOT_FINALIZE_STATE)

        if levelkuldesek != levelkuldesek_old:
            trace("CHANGE IN " + MAILS_TO_SEND_FIELD)
            update_data[MAILS_TO_SEND_FIELD] = levelkuldesek
        else:
            trace("NO CHANGE IN " + MAILS_TO_SEND_FIELD)

        if update_data:
            crm_data.set_student_data(student, update_data)

    crm_data.update_headcounts()
