# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function

import datetime

from minicrm.commonfunctions import *
from minicrm.tracing import stacktrace, trace, pretty_print

COURSE_IN_PROGRESS_STATE = "Kurzus folyamatban"
SPECTATOR_STATE = "Megfigyelő"
FINISHED_STATE = "Elvégezte"
MAILS_TO_SEND_FIELD = "Levelkuldesek"
STATUS_ID_FIELD = "StatusId"
ATTENDANCE_FIELD_NAME = "Jelenlet"
HOMEWORK_FIELD_NAME = "Hazi"

FIRST_OCCASION_DATE_FIELD = "N1Alkalom"
SECOND_OCCASION_DATE_FIELD = "N2Alkalom2"
THIRD_OCCASION_DATE_FIELD = "N3Alkalom2"
FOURTH_OCCASION_DATE_FIELD = "N4Alkalom2"
FIFTH_OCCASION_DATE_FIELD = "N5Alkalom2"
SIXTH_OCCASION_DATE_FIELD = "N6Alkalom2"
SEVENTH_OCCASION_DATE_FIELD = "N7Alkalom2"
EIGTH_OCCASION_DATE_FIELD = "N8Alkalom2"
NINTH_OCCASION_DATE_FIELD = "N9Alkalom2"
TENTH_OCCASION_DATE_FIELD = "N10Alkalom2"

FIRST_DAYOFF_FIELD = "N2SzunetOpcionalis2"
SECOND_DAYOFF_FIELD = "N2SzunetOpcionalis3"
THIRD_DAYOFF_FIELD = "N3SzunetOpcionalis2"

COURSE_TYPE_FIELD_IN_STUDENT = "TanfolyamTipusa2"
BEGINNER_COURSE_TYPE = "Kezdő programozó tanfolyam"
ADVANCED_COURSE_TYPE = "Haladó programozó tanfolyam"
COMPANY_BEGINNER_COURSE_TYPE = "Céges kezdő"
COMPANY_ADVANCED_COURSE_TYPE = "Céges haladó"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

FIRST_OCCASION_BEGINNER_MAIL_NAME = "1. alkalom - kezdő"
SECOND_OCCASION_BEGINNER_MAIL_NAME = "2. alkalom - kezdő"
THIRD_OCCASION_BEGINNER_MAIL_NAME = "3. alkalom - kezdő"
FOURTH_OCCASION_BEGINNER_MAIL_NAME = "4. alkalom - kezdő"
FIFTH_OCCASION_BEGINNER_MAIL_NAME = "5. alkalom - kezdő"
SIXTH_OCCASION_BEGINNER_MAIL_NAME = "6. alkalom - kezdő"
SEVENTH_OCCASION_BEGINNER_MAIL_NAME = "7. alkalom - kezdő"
EIGHT_OCCASION_BEGINNER_MAIL_NAME = "8. alkalom - kezdő"
NINTH_OCCASION_BEGINNER_MAIL_NAME = "9. alkalom - kezdő"
TENTH_OCCASION_BEGINNER_MAIL_NAME = "10. alkalom - kezdő"

FIRST_OCCASION_ADVANCED_MAIL_NAME = "1. alkalom - haladó"
SECOND_OCCASION_ADVANCED_MAIL_NAME = "2. alkalom - haladó"
THIRD_OCCASION_ADVANCED_MAIL_NAME = "3. alkalom - haladó"
FOURTH_OCCASION_ADVANCED_MAIL_NAME = "4. alkalom - haladó"
FIFTH_OCCASION_ADVANCED_MAIL_NAME = "5. alkalom - haladó"
SIXTH_OCCASION_ADVANCED_MAIL_NAME = "6. alkalom - haladó"
SEVENTH_OCCASION_ADVANCED_MAIL_NAME = "7. alkalom - haladó"
EIGHT_OCCASION_ADVANCED_MAIL_NAME = "8. alkalom - haladó"
NINTH_OCCASION_ADVANCED_MAIL_NAME = "9. alkalom - haladó"
TENTH_OCCASION_ADVANCED_MAIL_NAME = "10. alkalom - haladó"

FIRST_DAYOFF_MAIL_NAME = "1. szünet"
SECOND_DAYOFF_MAIL_NAME = "2. szünet"
THIRD_DAYOFF_MAIL_NAME = "3. szünet"

FINAL_MAIL_NAME = "Útravaló"
FINAL_MAIL_NAME_ADVANCED = "Útravaló - haladó"
CERTIFICATION_MAIL_NAME = "Oklevél - kezdő"
CERTIFICATION_MAIL_NAME_ADVANCED = "Oklevél - haladó"


@stacktrace
def send_scheduled_emails(crm_data):
    """
    Loops through active students and spectators and sends them scheduled letters based on the dates and other conditions. Sets done students to "Elvégezte"
    """

    trace("ACTIVE STUDENTS")
    active_students = crm_data.get_student_list_with_status(COURSE_IN_PROGRESS_STATE)

    trace("SPECTATORS: ")
    spectators = crm_data.get_student_list_with_status(SPECTATOR_STATE)

    student_list = merge_dicts(active_students, spectators)

    trace("STUDENT LIST: ")
    pretty_print(student_list)

    for student in student_list:
        student_data = crm_data.get_student(student)

        update_data = {}

        mails_to_send = student_data[MAILS_TO_SEND_FIELD]
        mails_to_send_old = mails_to_send

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[FIRST_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + FIRST_OCCASION_DATE_FIELD + ", NOW: {}")
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[SECOND_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + SECOND_OCCASION_DATE_FIELD)
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[THIRD_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + THIRD_OCCASION_DATE_FIELD)
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[FOURTH_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + FOURTH_OCCASION_DATE_FIELD)
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FOURTH_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FOURTH_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[FIFTH_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + FIFTH_OCCASION_DATE_FIELD)
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIFTH_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIFTH_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[SIXTH_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + SIXTH_OCCASION_DATE_FIELD)
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, SIXTH_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, SIXTH_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[SEVENTH_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + SEVENTH_OCCASION_DATE_FIELD)
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, SEVENTH_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, SEVENTH_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[EIGTH_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + EIGTH_OCCASION_DATE_FIELD)
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, EIGHT_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, EIGHT_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[NINTH_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + NINTH_OCCASION_DATE_FIELD)
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, NINTH_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, NINTH_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[TENTH_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=-3):
            trace("Set: " + TENTH_OCCASION_DATE_FIELD + "")
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, TENTH_OCCASION_BEGINNER_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, TENTH_OCCASION_ADVANCED_MAIL_NAME)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[TENTH_OCCASION_DATE_FIELD], DATE_FORMAT):
            trace("Set: " + TENTH_OCCASION_DATE_FIELD + " + 1 nap")
            if (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FINAL_MAIL_NAME)
            elif (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                    (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FINAL_MAIL_NAME_ADVANCED)

        if crm_data.get_today() >= datetime.datetime.strptime(student_data[TENTH_OCCASION_DATE_FIELD],
                                                              DATE_FORMAT) + datetime.timedelta(days=1):
            trace("Set: " + TENTH_OCCASION_DATE_FIELD + " + 2 nap")
            update_data[STATUS_ID_FIELD] = crm_data.get_student_status_number_by_name(FINISHED_STATE)
            if student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE:
                mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME_ADVANCED)
            if ok_for_certification(student_data):
                trace("Set: Certified also")
                if student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE:
                    mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME)
                elif student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE:
                    mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME_ADVANCED)

        if student_data[FIRST_DAYOFF_FIELD] != "":
            if crm_data.get_today() >= datetime.datetime.strptime(student_data[FIRST_DAYOFF_FIELD],
                                                                  DATE_FORMAT) + datetime.timedelta(days=-2):
                trace("Set: " + FIRST_DAYOFF_FIELD)
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_DAYOFF_MAIL_NAME)
        if student_data[SECOND_DAYOFF_FIELD] != "":
            if crm_data.get_today() >= datetime.datetime.strptime(student_data[SECOND_DAYOFF_FIELD],
                                                                  DATE_FORMAT) + datetime.timedelta(days=-2):
                trace("Set: " + SECOND_DAYOFF_FIELD)
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_DAYOFF_MAIL_NAME)
        if student_data[THIRD_DAYOFF_FIELD] != "":
            if crm_data.get_today() >= datetime.datetime.strptime(student_data[THIRD_DAYOFF_FIELD],
                                                                  DATE_FORMAT) + datetime.timedelta(days=-2):
                trace("Set: " + THIRD_DAYOFF_FIELD)
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_DAYOFF_MAIL_NAME)

        if mails_to_send != mails_to_send_old:
            trace("CHANGE IN LEVELKULDESEK")
            update_data[MAILS_TO_SEND_FIELD] = mails_to_send
        else:
            trace("NO CHANGE IN LEVELKULDESEK")

        if update_data:
            crm_data.set_student_data(student, update_data)


@stacktrace
def ok_for_certification(student_data):
    visited_classes = len(student_data[ATTENDANCE_FIELD_NAME].split(", "))
    sent_homeworks = len(student_data[HOMEWORK_FIELD_NAME].split(", "))
    return visited_classes >= 8 and sent_homeworks >= 8
