# -*- coding: utf-8 -*-
"""
This module contains requirements for CrmFacade.

Note that some requirements are covered in module tests, so redundant tests are not included here.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import datetime

import minicrm.crmrequestfactory as crmrequestfactory
import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.locationlists as responses_locationlists
import requesthandlermock.responses.locations as responses_locations
import requesthandlermock.responses.studentlists as responses_studentlists
from test.unit_tests.minicrmtestbase import MiniCrmTestBase

ARBITRARY_STUDENT_ID = 42
STUDENT_IN_PROGRESS_STATUS_NUMBER = 2749
STUDENT_IN_PROGRESS_STATUS_NAME = "Kurzus folyamatban"
APPLICATION_OPEN_STATUS_NUMBER = 2753
FAKE_COURSE_ID_NUMBER = 2037
FAKE_COURSE_COURSE_CODE = "2019-1-Q"


class TestGetApplicationDeadline(MiniCrmTestBase):
    """
    Contains tests for CrmFacade._get_application_deadline() (Private method.)
    """

    def test_if_course_starts_in_not_less_than_7_days_away_and_more_than_places_30_percent_if_free_deadline_is_5_days(
            self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 10, 9, 8))
        self.assertEqual(
            "2019-01-15 09:08:00",
            self.crm_facade._get_application_deadline(responses_courses.COURSE_2019_1_Q)
        )

    def test_if_course_starts_in_less_than_7_days_away_and_more_than_places_30_percent_if_free_deadline_is_3_days(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 23, 9, 8))
        self.assertEqual(
            "2019-01-26 09:08:00",
            self.crm_facade._get_application_deadline(responses_courses.COURSE_2019_1_Q)
        )

    def test_if_course_starts_in_not_less_than_7_days_away_and_less_than_places_30_percent_if_free_deadline_is_3_days(
            self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 10, 9, 8))
        self.assertEqual(
            "2019-01-13 09:08:00",
            self.crm_facade._get_application_deadline(responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)
        )

    def test_if_course_starts_in_less_than_3_days_and_there_is_no_more_than_3_places_deadline_is_1_day(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 26, 9, 8))
        self.assertEqual(
            "2019-01-27 09:08:00",
            self.crm_facade._get_application_deadline(responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)
        )

    def test_if_course_start_is_earlier_than_the_calculated_deadline_deadline_is_course_start_minus_one_day(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 26, 9, 8))
        self.assertEqual(
            "2019-01-27 23:59:59",
            self.crm_facade._get_application_deadline(responses_courses.COURSE_2019_1_Q)
        )

    def test_if_deadline_is_earlier_than_today_deadline_is_today_plus_one_day(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 9, 8))
        self.assertEqual(
            "2019-01-30 09:08:00",
            self.crm_facade._get_application_deadline(responses_courses.COURSE_2019_1_Q)
        )

    def test_if_all_spots_is_zero_function_does_not_raise(self):
        self.crm_facade._get_application_deadline(responses_courses.MAX_SPOTS_IS_ZERO)


class TestGetCourseByCourseCode(MiniCrmTestBase):

    def test_get_course_by_course_code_returns_correct_course(self):
        wanted_course_code = "2019-1-Q"
        wanted_course_id = 1164

        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(wanted_course_code),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_course(wanted_course_id),
            responses_courses.COURSE_2019_1_Q
        )
        course_info = self.crm_facade.get_course_by_course_code(wanted_course_code)
        self.assertEqual(course_info["TanfolyamBetujele"], wanted_course_code)


class TestGetDateDescription(MiniCrmTestBase):

    def set_course(self, api_response):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(ARBITRARY_STUDENT_ID),
            api_response
        )
        self.course_data = self.request_handler.fetch(
            crmrequestfactory.get_student(ARBITRARY_STUDENT_ID)
        )

    def test_date_description_returns_correct_string(self):
        self.set_course(responses_courses.COURSE_2019_1_Q_3_BREAKS)
        expected_string = u'   - 2019-01-28\n   - 2019-02-04\n   - 2019-02-11\n   - 2019-02-18\n   - 2019-02-25\n   - 2019-03-04\n   - 2019-03-11 - sz\xfcnet\n   - 2019-03-18\n   - 2019-03-21 - sz\xfcnet\n   - 2019-03-25\n   - 2019-03-31 - sz\xfcnet\n   - 2019-04-01\n   - 2019-04-08'
        self.assertEqual(self.crm_facade._get_date_description(self.course_data), expected_string)


class TestGetLocationByName(MiniCrmTestBase):
    def test_get_location_by_name_returns_correct_course(self):
        location_name = u"Pannon Kincstár"
        location_id = 19

        self.request_handler.expect_request(
            crmrequestfactory.get_location_list_by_location_name(location_name),
            responses_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_location(location_id),
            responses_locations.PANNON_KINCSTAR
        )

        result = self.crm_facade.get_location_by_name(location_name)
        self.assertEqual(result, responses_locations.PANNON_KINCSTAR)

    def test_get_location_by_name_returns_none_for_nonexistent_course_code(self):
        nonexistent_location_name = "NONEXISTENT"

        self.request_handler.expect_request(
            crmrequestfactory.get_location_list_by_location_name(nonexistent_location_name),
            responses_general.EMPTY_LIST
        )

        result = self.crm_facade.get_location_by_name(nonexistent_location_name)
        self.assertIsNone(result)


class TestQueryProjectListWithStatus(MiniCrmTestBase):
    def test_query_project_list_with_status_returns_all_projects_even_if_there_are_more_pages(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(STUDENT_IN_PROGRESS_STATUS_NUMBER),
            responses_studentlists.STUDENT_LIST_105_ACTIVE_PAGE_0
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status_page1(STUDENT_IN_PROGRESS_STATUS_NUMBER),
            responses_studentlists.STUDENT_LIST_105_ACTIVE_PAGE_1
        )
        results = self.crm_facade.get_student_list_with_status(STUDENT_IN_PROGRESS_STATUS_NAME)
        self.assertEqual(len(results), 105)


class TestUpdateHeadcounts(MiniCrmTestBase):

    def test_headcount_is_1_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_1_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_2_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_2_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_1_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_1_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 1}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_2_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_2_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 1}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_0_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 1}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_active_student_count_is_set_to_1(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.ACTIVE_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 1}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_active_and_1_info_sent_count_is_set_to_2(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.ONE_ACTIVE_AND_ONE_INFO_SENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 2}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_did_not_answer_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.DID_NOT_ANSWER_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_cancelled_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.CANCELLED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_not_payed_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.NOT_PAYED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_spectator_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.SPECTATORS_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_waiting_list_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_subscribed_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.SUBSCRIBED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_applied_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.APPLIED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_finished_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.FINISHED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_unsubscribed_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.UNSUBSCRIBED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_are_2_info_sent_3_active_2_waiting_list_1_did_not_answer_1_spectator_count_is_set_to_5(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.COMPLEX_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 5}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()
