# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function

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
def send_scheduled_emails(crm_facade):
    """
    Loops through active students and spectators and sends them scheduled letters based on the dates and other conditions. Sets done students to "Elvégezte"
    """

    trace("ACTIVE STUDENTS")
    active_students = crm_facade.get_student_list_with_status(COURSE_IN_PROGRESS_STATE)

    trace("SPECTATORS: ")
    spectators = crm_facade.get_student_list_with_status(SPECTATOR_STATE)

    students = merge_dicts(active_students, spectators)

    trace("STUDENT LIST: ")
    pretty_print(students)

    for student in students:
        student_data = crm_facade.get_student(student)

        update_data = {}

        mails_to_send = student_data[MAILS_TO_SEND_FIELD]
        mails_to_send_old = mails_to_send

        student_is_beginner = (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE) or \
                              (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_BEGINNER_COURSE_TYPE)

        student_is_beginner_not_company = student_data[COURSE_TYPE_FIELD_IN_STUDENT] == BEGINNER_COURSE_TYPE

        student_is_advanced = (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE) or \
                              (student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE)

        student_is_company_advanced = student_data[COURSE_TYPE_FIELD_IN_STUDENT] == COMPANY_ADVANCED_COURSE_TYPE

        student_is_advanced_not_company = student_data[COURSE_TYPE_FIELD_IN_STUDENT] == ADVANCED_COURSE_TYPE

        if date_is_not_less_than(crm_facade, student_data[FIRST_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[SECOND_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[THIRD_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[FOURTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FOURTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FOURTH_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[FIFTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIFTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIFTH_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[SIXTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SIXTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SIXTH_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[SEVENTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SEVENTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SEVENTH_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[EIGTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, EIGHT_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, EIGHT_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[NINTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, NINTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, NINTH_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[TENTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, TENTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, TENTH_OCCASION_ADVANCED_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[TENTH_OCCASION_DATE_FIELD], +0):
            if student_is_beginner_not_company:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FINAL_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FINAL_MAIL_NAME_ADVANCED)

        if date_is_not_less_than(crm_facade, student_data[TENTH_OCCASION_DATE_FIELD], +1):
            update_data[STATUS_ID_FIELD] = crm_facade.get_student_status_number_by_name(FINISHED_STATE)
            if student_is_company_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME_ADVANCED)
            if ok_for_certification(student_data):
                if student_is_beginner_not_company:
                    mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME)
                elif student_is_advanced_not_company:
                    mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME_ADVANCED)

        if student_data[FIRST_DAYOFF_FIELD] != "":
            if date_is_not_less_than(crm_facade, student_data[FIRST_DAYOFF_FIELD], -2):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_DAYOFF_MAIL_NAME)
        if student_data[SECOND_DAYOFF_FIELD] != "":
            if date_is_not_less_than(crm_facade, student_data[SECOND_DAYOFF_FIELD], -2):
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_DAYOFF_MAIL_NAME)
        if student_data[THIRD_DAYOFF_FIELD] != "":
            if date_is_not_less_than(crm_facade, student_data[THIRD_DAYOFF_FIELD], -2):
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_DAYOFF_MAIL_NAME)

        if mails_to_send != mails_to_send_old:
            trace("CHANGE IN LEVELKULDESEK")
            update_data[MAILS_TO_SEND_FIELD] = mails_to_send
        else:
            trace("NO CHANGE IN LEVELKULDESEK")

        if update_data:
            crm_facade.set_student_data(student, update_data)


@stacktrace
def ok_for_certification(student_data):
    visited_classes = len(student_data[ATTENDANCE_FIELD_NAME].split(", "))
    sent_homeworks = len(student_data[HOMEWORK_FIELD_NAME].split(", "))
    return visited_classes >= 8 and sent_homeworks >= 8
