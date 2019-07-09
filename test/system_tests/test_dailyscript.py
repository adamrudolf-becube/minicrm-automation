"""
This module contains all of the tests and requirements for the functionality called dailyscript.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import dailyscript
import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.studentlists as responses_studentlists
import requesthandlermock.responses.students as responses_students
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase

ACTIVE_STATUS_NUMBER = 2749
SPECTATOR_STATUS = 2784
FAKE_STUDENT_ID_NUMBER = 2941
APPLICATION_OPEN_STATUS_NUMBER = 2753
IN_PROGRESS_STATUS_NUMBER = 2758
RECENTLY_FINISHED_STATUS_NUMBER = 2797
FAKE_COURSE_ID_NUMBER = 2037


class TestDailyScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):
        """
        dailyscript.run runs a valid sequence of

        - sendscheduledmails

        - setcoursestates
        """
        self.expect_send_scheduled_mails()
        self.expect_set_course_states()

        dailyscript.run(self.crm_facade)

    def expect_send_scheduled_mails(self):
        """Sets up expectations to a valid sendscheduledmails workflow"""
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(ACTIVE_STATUS_NUMBER),
            responses_studentlists.ACTIVE_ONE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(SPECTATOR_STATUS),
            responses_general.EMPTY_LIST
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )

    def expect_set_course_states(self):
        """Sets up expectations to a valid setcoursestates workflow"""
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
