# -*- coding: utf-8 -*-
"""
Makes sure all of the mails already due have been sent to the student.

BeCube MiniCRM automation project.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

from minicrm.commonfunctions import \
    merge_dicts, \
    date_is_not_less_than, \
    date_is_not_more_than, \
    add_element_to_commasep_list
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
FRONTEND_COURSE_TYPE = "Frontend tanfolyam"

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

FIRST_OCCASION_FRONTEND_MAIL_NAME = "1. alkalom - frontend"
SECOND_OCCASION_FRONTEND_MAIL_NAME = "2. alkalom - frontend"
THIRD_OCCASION_FRONTEND_MAIL_NAME = "3. alkalom - frontend"
FOURTH_OCCASION_FRONTEND_MAIL_NAME = "4. alkalom - frontend"
FIFTH_OCCASION_FRONTEND_MAIL_NAME = "5. alkalom - frontend"
SIXTH_OCCASION_FRONTEND_MAIL_NAME = "6. alkalom - frontend"
SEVENTH_OCCASION_FRONTEND_MAIL_NAME = "7. alkalom - frontend"
EIGHT_OCCASION_FRONTEND_MAIL_NAME = "8. alkalom - frontend"
NINTH_OCCASION_FRONTEND_MAIL_NAME = "9. alkalom - frontend"
TENTH_OCCASION_FRONTEND_MAIL_NAME = "10. alkalom - frontend"

FIRST_DAYOFF_MAIL_NAME = "1. szünet"
SECOND_DAYOFF_MAIL_NAME = "2. szünet"
THIRD_DAYOFF_MAIL_NAME = "3. szünet"

FINAL_MAIL_NAME = "Útravaló"
FINAL_MAIL_NAME_ADVANCED = "Útravaló - haladó"
FINAL_MAIL_NAME_FRONTEND = "Útravaló - frontend"
CERTIFICATION_MAIL_NAME = "Oklevél - kezdő"
CERTIFICATION_MAIL_NAME_ADVANCED = "Oklevél - haladó"
CERTIFICATION_MAIL_NAME_FRONTEND = "Oklevél - frontend"


@stacktrace
def send_scheduled_emails(crm_facade):
    """
    Loops through active students and spectators and sends them scheduled mails based on the dates and other conditions.

    The following rules apply:

    - All students in "In Progress" ("Kurzus folyamatban") and "Spectator" ("Megfigyelo") are affected.

    - All mails of the occasions are sent if the date is not less than the occasion's date minus 3 days.

    - There are three types of "regular" mails (i.e. sent for every single occasion): beginner, advanded and frontend.
     There are 10 mails of each type for the 10 occasions.

    - Company advanced is counted as advanced and company beginner is counted as beginner in these regular mails.

    - On the day of the last occasion a goodbye mail is sent, also based on student is beginner, advanced or frontend.

    - This goodbye mail is not sent to company beginners, but is sent to company advanced. (So the courses can be
      accumulated to one long course and they only get goodbye mail at the very end.)

    - If the date is not less then the last date plus one day, student is put to "Finished" ("Elvegezte") state.

    - On the same day beginner/advanced/frontend certification is sent if the student is not attending a company course
      and is eligible.

    - On the same day advanced certification is sent if the student is attending a company advanced course.

    - Mail about free day is sent 2 days before each dayoff. If dayoff is added later, it is not sent.

    :param crm_facade: instance of the CrmFacade class this functionality will use to communicate with a MiniCRM system.

    :return: None
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

        student_is_frontend = student_data[COURSE_TYPE_FIELD_IN_STUDENT] == FRONTEND_COURSE_TYPE

        if date_is_not_less_than(crm_facade, student_data[FIRST_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[SECOND_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[THIRD_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, THIRD_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[FOURTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FOURTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FOURTH_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FOURTH_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[FIFTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIFTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIFTH_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIFTH_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[SIXTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SIXTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SIXTH_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SIXTH_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[SEVENTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SEVENTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SEVENTH_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, SEVENTH_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[EIGTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, EIGHT_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, EIGHT_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, EIGHT_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[NINTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, NINTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, NINTH_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, NINTH_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[TENTH_OCCASION_DATE_FIELD], -3):
            if student_is_beginner:
                mails_to_send = add_element_to_commasep_list(mails_to_send, TENTH_OCCASION_BEGINNER_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, TENTH_OCCASION_ADVANCED_MAIL_NAME)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, TENTH_OCCASION_FRONTEND_MAIL_NAME)

        if date_is_not_less_than(crm_facade, student_data[TENTH_OCCASION_DATE_FIELD], +0):
            if student_is_beginner_not_company:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FINAL_MAIL_NAME)
            elif student_is_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FINAL_MAIL_NAME_ADVANCED)
            elif student_is_frontend:
                mails_to_send = add_element_to_commasep_list(mails_to_send, FINAL_MAIL_NAME_FRONTEND)

        if date_is_not_less_than(crm_facade, student_data[TENTH_OCCASION_DATE_FIELD], +1):
            update_data[STATUS_ID_FIELD] = crm_facade.get_student_status_number_by_name(FINISHED_STATE)
            if student_is_company_advanced:
                mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME_ADVANCED)
            if ok_for_certification(student_data):
                if student_is_beginner_not_company:
                    mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME)
                elif student_is_advanced_not_company:
                    mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME_ADVANCED)
                elif student_is_frontend:
                    mails_to_send = add_element_to_commasep_list(mails_to_send, CERTIFICATION_MAIL_NAME_FRONTEND)

        if student_data[FIRST_DAYOFF_FIELD] != "":
            if date_is_not_less_than(crm_facade, student_data[FIRST_DAYOFF_FIELD], -2) and \
                    date_is_not_more_than(crm_facade, student_data[FIRST_DAYOFF_FIELD]):
                mails_to_send = add_element_to_commasep_list(mails_to_send, FIRST_DAYOFF_MAIL_NAME)
        if student_data[SECOND_DAYOFF_FIELD] != "":
            if date_is_not_less_than(crm_facade, student_data[SECOND_DAYOFF_FIELD], -2) and \
                    date_is_not_more_than(crm_facade, student_data[SECOND_DAYOFF_FIELD]):
                mails_to_send = add_element_to_commasep_list(mails_to_send, SECOND_DAYOFF_MAIL_NAME)
        if student_data[THIRD_DAYOFF_FIELD] != "":
            if date_is_not_less_than(crm_facade, student_data[THIRD_DAYOFF_FIELD], -2) and \
                    date_is_not_more_than(crm_facade, student_data[THIRD_DAYOFF_FIELD]):
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
    """
    Checks if the given student is eligible for a certification or not.

    Student is eligible if

    - student visited at least 8 occasions, AND
    - student has sent at least 8 homework solutions

    :param student_data: Full JSON array of a student as stored in the MiniCRM system-

    :return: True if the student is eligible for cerification and False if not.
    """
    visited_classes = len(student_data[ATTENDANCE_FIELD_NAME].split(", "))
    sent_homeworks = len(student_data[HOMEWORK_FIELD_NAME].split(", "))
    return visited_classes >= 8 and sent_homeworks >= 8
