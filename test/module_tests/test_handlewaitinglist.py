"""
This module contains all of the tests and requirements for the functionality called handlewaitinglist
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.studentlists as responses_studentlists
import requesthandlermock.responses.students as responses_students
from functionalities.handlewaitinglist import handle_waiting_list
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase

WAITING_LIST_STATUS_NUMBER = 2750
FAKE_STUDENT_ID_NUMBER = 2790
FAKE_STUDENT_OTHER_ID_NUMBER = 2601
FAKE_STUDENT_THIRD_ID_NUMBER = 2602
FAKE_STUDENT_FOURTH_ID_NUMBER = 2797
FAKE_STUDENT_FIFTH_ID_NUMBER = 2798
FAKE_STUDENT_SIXTH_ID_NUMBER = 2799
FAKE_STUDENT_APPLIED_LATER_ID_NUMBER = 2796
FAKE_COURSE_COURSE_CODE = "2019-1-Q"
FAKE_COURSE_ID_NUMBER = 1164


class TestHandleWaitingList(MiniCrmTestBase):

    def test_there_is_one_student_on_waiting_list_but_there_are_no_free_places_do_nothing(self):
        """
        Given:
            - there is a student in waiting list
            - there is no free spot on the wanted course
        When:
            - handle_waiting_list() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(WAITING_LIST_STATUS_NUMBER),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
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
        handle_waiting_list(self.crm_facade)

    def test_there_are_multiple_students_on_waiting_list_but_there_are_no_free_places_do_nothing(self):
        """
        Given:
            - there are multiple students in waiting list
            - there is no free spot on the wanted course
        When:
            - handle_waiting_list() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(WAITING_LIST_STATUS_NUMBER),
            responses_studentlists.WAITING_LIST_TWO_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_APPLIED_LATER_ID_NUMBER),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
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
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)

    def test_there_is_one_student_on_waiting_list_and_there_is_one_free_place_put_student_to_info_sent(self):
        """
        Given:
            - there is a student in waiting list
            - there is one free spot on the wanted course
        When:
            - handle_waiting_list() is called
        Then:
            - INFO email is sent
            - "A spot freed up" email is sent
            - change student's status to "INFO sent"
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(WAITING_LIST_STATUS_NUMBER),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)

    def test_student_gets_into_chosen_course_even_if_available_courses_changed(self):
        """
        test_student_gets_into_chosen_course_even_if_available_courses_changed

        Given:
            - there is a student in waiting list
            - MelyikTanfolyamErdekli and TanfolyamKodja are different
            - there is one free spot on the wanted course
        When:
            - handle_waiting_list() is called
        Then:
            - INFO email is sent
            - "A spot freed up" email is sent
            - change student's status to "INFO sent"
            - TanfolyamKodja is considered
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(WAITING_LIST_STATUS_NUMBER),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COURSE_CODE_AND_APPLIED_TO_ARE_DIFFERENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)


    def test_there_are_multiple_students_on_waiting_list_and_there_is_one_free_place_put_earlier_student_to_info_sent(
            self):
        """
        Given:
            - there are two students in waiting list
            - there is one free spot on the wanted course
        When:
            - handle_waiting_list() is called
        Then:
            - for the one who applies earlier:
                - INFO email is sent
                - "A spot freed up" email is sent
                - change student's status to "INFO sent"
            - for the other student:
                - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(WAITING_LIST_STATUS_NUMBER),
            responses_studentlists.WAITING_LIST_TWO_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_APPLIED_LATER_ID_NUMBER),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
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
        handle_waiting_list(self.crm_facade)

    def test_there_are_multiple_students_on_waiting_list_and_there_are_two_free_places_put_both_students_to_info_sent(
            self):
        """
        Given:
            - there are two students in waiting list
            - there are two free spots on the wanted course
        When:
            - handle_waiting_list() is called
        Then:
            - for both students:
                - INFO email is sent
                - "A spot freed up" email is sent
                - change student's status to "INFO sent"
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(WAITING_LIST_STATUS_NUMBER),
            responses_studentlists.WAITING_LIST_TWO_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_APPLIED_LATER_ID_NUMBER),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
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
                FAKE_STUDENT_THIRD_ID_NUMBER,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)

    def test_there_are_5_students_on_the_waiting_list_and_there_are_two_free_places_put_the_earliest_two_to_info_sent(
            self):
        """
        Given:
            - there are 5 students in waiting list
            - there are two free spots on the wanted course
        When:
            - handle_waiting_list() is called
        Then:
            - for the two who applied the earliest:
                - INFO email is sent
                - "A spot freed up" email is sent
                - change student's status to "INFO sent"
            - for the other student:
                - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(WAITING_LIST_STATUS_NUMBER),
            responses_studentlists.WAITING_LIST_FIVE_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_FIFTH_ID_NUMBER),
            responses_students.FAKE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_SIXTH_ID_NUMBER),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_APPLIED_LATER_ID_NUMBER),
            responses_students.FAKE_STUDENT_4TH_APPLIED)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_FOURTH_ID_NUMBER),
            responses_students.FAKE_STUDENT_5TH_APPLIED)

        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_OTHER_ID_NUMBER,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
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
                FAKE_STUDENT_THIRD_ID_NUMBER,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )

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
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q_FULL
        )
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
        handle_waiting_list(self.crm_facade)
