"""
This module contains all of the tests and requirements for the functionality called cleaninfosent
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import datetime

import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.studentlists as responses_studentlists
import requesthandlermock.responses.students as responses_students
from functionalities.cleaninfosent import clean_info_sent
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase

INFO_SENT_STATUS_NUMBER = 2781
FAKE_STUDENT_ID_NUMBER = 2941


class TestInfoSent(MiniCrmTestBase):
    def setUp(self):
        super(TestInfoSent, self).setUp()
        self.crm_facade.set_today(datetime.datetime(2019, 1, 21, 7, 30))

    def test_student_did_not_finalize_deadline_has_not_spent_but_within_24_hours_send_reminder(self):
        """
        Given:
            - there is a student in INFO sent ("INFO level kiment") state
            - they did not finalize application
            - finalization deadline has not spent, but is within less than 24 hours
        When:
            - clean_info_sent() is called
        Then:
            - reminder email ("Egy napod van jelentkezni") is sent
        """

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

        clean_info_sent(self.crm_facade)

    def test_student_did_not_finalize_deadline_has_spent_but_not_more_than_24_hours_ago_send_reminder_raise_task(self):
        """
        Given:
            - there is a student in INFO sent ("INFO level kiment") state
            - they did not finalize application
            - finalization deadline has been spent, but is within less than 24 hours
        When:
            - clean_info_sent() is called
        Then:
            - 2nd reminder email ("Egy napod van jelentkezni") is sent
            - task is raised on the student
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 23, 12, 0))

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
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni, Ma kell jelentkezni"}
            ),
            responses_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

        clean_info_sent(self.crm_facade)

    def test_student_did_not_finalize_deadline_has_spent_more_than_24_hours_ago_delete(self):
        """
        Given:
            - there is a student in INFO sent ("INFO level kiment") state
            - they did not finalize application
            - finalization deadline has been spent more than 24 hours ago
        When:
            - clean_info_sent() is called
        Then:
            - "we deleted you" email is sent
            - status of student is set to deleted
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 24, 12, 0))

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
                {
                    u"StatusId": u"2782",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni, Ma kell jelentkezni, Toroltunk"
                }
            ),
            responses_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

        clean_info_sent(self.crm_facade)

    def test_student_did_not_finalize_and_deadline_is_more_than_1_day_away_do_nothing(self):
        """
        Given:
            - there is a student in INFO sent ("INFO level kiment") state
            - they did not finalize application
            - finalization deadline has not been spent and is in more than 24 hours
        When:
            - clean_info_sent() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(INFO_SENT_STATUS_NUMBER),
            responses_studentlists.INFO_SENT_ONE_STUDENT
        )
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.set_participant_number_expectations()

        clean_info_sent(self.crm_facade)
