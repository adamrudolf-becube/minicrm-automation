# -*- coding: utf-8 -*-
"""
This module contains all of the tests and requirements for the functionality called quickscript.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import datetime

import quickscript
import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.locationlists as responses_locationlists
import requesthandlermock.responses.locations as responses_locations
import requesthandlermock.responses.studentlists as responses_studentlists
import requesthandlermock.responses.students as responses_students
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase

INFO_SENT_STATUS_NUMBER = 2781
FAKE_STUDENT_ID_NUMBER = 2941
WAITING_LIST_STATUS_NUMBER = 2750
FAKE_STUDENT_ID_NUMBER_2 = 2790
FAKE_STUDENT_OTHER_ID_NUMBER = 2601
FAKE_COURSE_ID_NUMBER = 1164
FAKE_COURSE_COURSE_CODE = "2019-1-Q"
NEW_APPLICANT_STATUS_NUMBER = 2741
LOCATION_NAME = u"Pannon Kincstár"
LOCATION_ID = 19


class TestQuickScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):
        """
        quickscript.run runs a valid sequence of

        - cleaninfosent

        - handlewaitinglist

        - registernewapplicants
        """
        self.expect_clean_info_sent()
        self.expect_handle_waiting_list()
        self.expect_register_new_applicants()

        quickscript.run(self.crm_facade)

    def expect_clean_info_sent(self):
        """Sets up expectations to a valid cleaninfosent workflow"""
        self.crm_facade.set_today(datetime.datetime(2019, 1, 22, 12, 0))

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(INFO_SENT_STATUS_NUMBER),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni"}
            ),
            responses_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

    def expect_handle_waiting_list(self):
        """Sets up expectations to a valid handlewaitinglist workflow"""
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(WAITING_LIST_STATUS_NUMBER),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER_2),
            responses_students.FAKE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()

    def expect_register_new_applicants(self):
        """Sets up expectations to a valid registernewapplicants workflow"""
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(NEW_APPLICANT_STATUS_NUMBER),
            responses_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT)

        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {u"TanfolyamKodja": u"2019-1-Q"}
            ),
            responses_general.XPUT_RESPONSE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_location_list_by_location_name(LOCATION_NAME),
            responses_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_location(LOCATION_ID),
            responses_locations.PANNON_KINCSTAR
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_OTHER_ID_NUMBER, crmrequestfactory._),
            responses_general.XPUT_RESPONSE
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {u"StatusId": u"2781", u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l"}
            ),
            responses_general.XPUT_RESPONSE
        )
