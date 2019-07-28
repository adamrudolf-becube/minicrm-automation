# -*- coding: utf-8 -*-
"""
This module contains all of the tests and requirements for the functionality called registernewapplicants.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.locationlists as responses_locationlists
import requesthandlermock.responses.locations as responses_locations
import requesthandlermock.responses.studentlists as responses_studentlists
import requesthandlermock.responses.students as responses_students
from functionalities.registernewapplicants import register_new_applicants
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase

NEW_APPLICANT_STATUS_NUMBER = 2741
FAKE_STUDENT_ID_NUMBER = 2941
FAKE_STUDENT_OTHER_ID_NUMBER = 2601
FAKE_COURSE_COURSE_CODE = "2019-1-Q"
NONEXISTENT_COURSE_CODE = "NONEXISTENT"
FAKE_COURSE_ID_NUMBER = 1164
LOCATION_NAME = u"Pannon Kincstár"
LOCATION_ID = 19


class TestRegisterNewApplicants(MiniCrmTestBase):
    def test_no_new_applicant_do_nothing(self):
        """
        Given:
            - there is no new applicant
        When:
            - register_new_applicants() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(NEW_APPLICANT_STATUS_NUMBER),
            responses_general.EMPTY_LIST
        )
        register_new_applicants(self.crm_facade)

    def test_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data(
            self):
        """
        test_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data

        Given:
            - one beginner student is in applied ("Jelentkezett") state
            - current headcount is less than maximal headcount. (there is at least one free spot) in the wanted course.)
        When:
            - register_new_applicants() is called
        Then:
            - student's info is filled
            - student is put to INFO sent ("INFO level kiment") state
            - beginner INFO mail is sent
            - application deadline is set
            - headcount is updated
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(NEW_APPLICANT_STATUS_NUMBER),
            responses_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ZERO_MAILS)

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
        register_new_applicants(self.crm_facade)

    def test_advanced_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data(
            self):
        """
        test_advanced_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data

        Given:
            - one advanced student is in applied ("Jelentkezett") state
            - current headcount is less than maximal headcount. (there is at least one free spot) in the wanted course.)
        When:
            - register_new_applicants() is called
        Then:
            - student's info is filled
            - student is put to INFO sent ("INFO level kiment") state
            - advanced INFO mail is sent
            - application deadline is set
            - headcount is updated
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(NEW_APPLICANT_STATUS_NUMBER),
            responses_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED_ZERO_MAILS)

        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_ADVANCED_ONE_PLACE_FREE
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
                {u"StatusId": u"2781", u"Levelkuldesek": u"Halad\u00f3 INFO lev\u00e9l"}
            ),
            responses_general.XPUT_RESPONSE
        )
        register_new_applicants(self.crm_facade)

    def test_student_is_applied_course_doesnt_exist_raise_task_with_errormessage(self):
        """
        Given:
            - one beginner student is in applied ("Jelentkezett") state
            - student's course doesn't exist
        When:
            - register_new_applicants() is called
        Then:
            - task is raised on student
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(NEW_APPLICANT_STATUS_NUMBER),
            responses_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_NONEXISTENT_COURSE
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(NONEXISTENT_COURSE_CODE),
            responses_general.EMPTY_LIST
        )

        self.request_handler.expect_request(
            crmrequestfactory.raise_task(
                crmrequestfactory._,
                crmrequestfactory._,
                crmrequestfactory._),
            responses_general.XPUT_RESPONSE
        )

        register_new_applicants(self.crm_facade)

    def test_beginner_student_is_applied_headcount_is_not_less_than_the_limit_put_student_to_waiting_list_and_send_mail(self):
        """
        test_beginner_student_is_applied_headcount_is_not_less_than_the_limit_put_student_to_waiting_list_and_send_mail

        Given:
            - one beginner student is in applied ("Jelentkezett") state
            - current headcount is equal to maximal headcount. (there is no free spot) in the wanted course.)
        When:
            - register_new_applicants() is called
        Then:
            - student is put to waiting list ("Varolistan van") state
            - waiting list mail
            - headcount is updated
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(NEW_APPLICANT_STATUS_NUMBER),
            responses_studentlists.NEW_APPLICANTS_ONE_STUDENT
        )

        self.set_participant_number_expectations()

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {u"TanfolyamKodja": u"2019-1-Q"}
            ),
            responses_general.XPUT_RESPONSE
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {
                    u"StatusId": u"2750",
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"V\u00e1r\u00f3lista"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )

        register_new_applicants(self.crm_facade)

    def test_advanced_student_is_applied_headcount_is_not_less_than_the_limit_put_student_to_waiting_list_and_send_mail(self):
        """
        Given:
            - one advanced student is in applied ("Jelentkezett") state
            - current headcount is equal to minimal headcount. (there is no free spot) in the wanted course.)
        When:
            - register_new_applicants() is called
        Then:
            - student is put to waiting list ("Varolistan van") state
            - waiting list mail
            - headcount is updated
        """
        # TODO: update documentation

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(NEW_APPLICANT_STATUS_NUMBER),
            responses_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED_ZERO_MAILS)

        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_ADVANCED_FULL)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {u"TanfolyamKodja": u"2019-1-Q"}
            ),
            responses_general.XPUT_RESPONSE
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {
                    u"StatusId": u"2750",
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"V\u00e1r\u00f3lista"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )

        register_new_applicants(self.crm_facade)