"""
This module contains all of the tests and requirements for the functionality called setcoursestates.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import datetime

import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
from functionalities.setcoursestates import set_course_states
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase

APPLICATION_OPEN_STATUS_NUMBER = 2753
IN_PROGRESS_STATUS_NUMBER = 2758
RECENTLY_FINISHED_STATUS_NUMBER = 2797
FAKE_COURSE_ID_NUMBER = 2037


class TestSetCourseStates(MiniCrmTestBase):

    def test_application_is_open_and_first_day_hasnt_spent_do_nothing(self):
        """
        test_application_is_open_and_first_day_hasnt_spent_do_nothing

        Given:
            - One course is in Application Open state ("Jelentkezes nyitva")
            - First day hasn't spent
        When:
            - set_course_states() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q)
        set_course_states(self.crm_facade)

    def test_application_is_open_first_day_spent_but_last_didnt_put_to_in_progress(self):
        """
        test_application_is_open_first_day_spent_but_last_didnt_put_to_in_progress

        Given:
            - One course is in Application Open state ("Jelentkezes nyitva")
            - First day has spent, last day hasn't
        When:
            - set_course_states() is called
        Then:
            - Course is put to In Progress ("Folyamatban") state
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"StatusId": u"2758"}),
            responses_general.XPUT_RESPONSE)
        set_course_states(self.crm_facade)

    def test_in_progress_first_day_is_spent_but_last_didnt_set_state_to_in_progress(self):
        """
        test_in_progress_first_day_is_spent_but_last_didnt_set_state_to_in_progress

        Given:
            - One course is in In Progress state ("Folyamatban")
            - First day has spent, last day hasn't
        When:
            - set_course_states() is called
        Then:
            - Course is put to In Progress ("Folyamatban") state
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_IN_PROGRESS)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"StatusId": u"2758"}),
            responses_general.XPUT_RESPONSE)
        set_course_states(self.crm_facade)

    def test_recently_finished_first_day_spent_but_last_didnt_put_to_in_progress(self):
        """
        test_recently_finished_first_day_spent_but_last_didnt_put_to_in_progress

        Given:
            - One course is in Recently Finished state ("Frissen vegzett")
            - First day has spent, last day hasn't
        When:
            - set_course_states() is called
        Then:
            - Course is put to In Progress ("Folyamatban") state
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_RECENTLY_FINISHED)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"StatusId": u"2758"}),
            responses_general.XPUT_RESPONSE)
        set_course_states(self.crm_facade)

    def test_in_progress_last_day_has_spent_but_not_35_more_days_put_to_recently_finished(self):
        """
        test_in_progress_last_day_has_spent_but_not_35_more_days_put_to_recently_finished

        Given:
            - One course is in In Progress state ("Folyamatban")
            - Last day has spent, but not more than 35 days ago
        When:
            - set_course_states() is called
        Then:
            - Course is put to Recently Finished ("Frissen vegzett") state
        """

        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_IN_PROGRESS)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"StatusId": u"2797"}),
            responses_general.XPUT_RESPONSE)
        set_course_states(self.crm_facade)

    def test_recently_finished_last_day_has_spent_but_not_35_more_put_to_recently_finished(self):
        """
        test_recently_finished_last_day_has_spent_but_not_35_more_put_to_recently_finished

        Given:
            - One course is in Recently Finished state ("Frissen vegzett")
            - Last day has spent, but not more than 35 days ago
        When:
            - set_course_states() is called
        Then:
            - Course is put to Recently Finished ("Frissen vegzett") state
        """

        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_RECENTLY_FINISHED)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"StatusId": u"2797"}),
            responses_general.XPUT_RESPONSE)
        set_course_states(self.crm_facade)

    def test_recently_finished_and_35_days_passed_put_to_closed(self):
        """
        test_recently_finished_and_35_days_passed_put_to_closed

        Given:
            - One course is in In Progress state ("Folyamatban")
            - Last day has spent more than 35 days ago
        When:
            - set_course_states() is called
        Then:
            - Course is put to Closed ("Vegzett") state
        """

        self.crm_facade.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_RECENTLY_FINISHED)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"StatusId": u"2754"}),
            responses_general.XPUT_RESPONSE)
        set_course_states(self.crm_facade)

    def test_first_day_is_missing_no_error_is_raised_state_is_not_changed(self):
        """
        test_first_day_is_missing_no_error_is_raised_state_is_not_changed

        Given:
            - One course is in in Application open ("Jelentkezes nyitva") state
            - First day is missing
        When:
            - set_course_states() is called
        Then:
            - Error is not raised
            - State is not changed
        """

        self.crm_facade.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_FIRST_DATE_MISSING)
        set_course_states(self.crm_facade)

    def test_last_day_is_missing_no_error_is_raised_put_to_in_progress(self):
        """
        test_last_day_is_missing_no_error_is_raised_put_to_in_progress

        Given:
            - One course is in in Application open ("Jelentkezes nyitva") state
            - Last day is missing
        When:
            - set_course_states() is called
        Then:
            - Error is not raised
            - Course is put to In Progress ("Folyamatban") state
        """

        self.crm_facade.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(APPLICATION_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(IN_PROGRESS_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(RECENTLY_FINISHED_STATUS_NUMBER),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_LAST_DATE_MISSING)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"StatusId": u"2758"}),
            responses_general.XPUT_RESPONSE)
        set_course_states(self.crm_facade)

    # TODO: [PLANNED] If course is started, put waiting list students to SUBSCRIBED (erdeklodo) state and send mail
