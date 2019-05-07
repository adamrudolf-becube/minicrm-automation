from minicrm import crmrequestfactory
import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.studentlists as responses_studentlists
import requesthandlermock.responses.students as responses_students
from functionalities.handlewaitinglist import handle_waiting_list
from test.unit_tests.minicrmtestbase import MiniCrmTestBase


class TestHandleWaitingList(MiniCrmTestBase):

    def test_there_is_one_student_on_waiting_list_but_there_are_no_free_places_do_nothing(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2750),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2790),
            responses_students.FAKE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)

    def test_there_are_multiple_students_on_waiting_list_but_there_are_no_free_places_do_nothing(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2750),
            responses_studentlists.WAITING_LIST_TWO_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2790),
            responses_students.FAKE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2796),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)

    def test_there_is_one_student_on_waiting_list_and_there_is_one_free_place_put_student_to_info_sent(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2750),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2790),
            responses_students.FAKE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2601,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)

    def test_there_are_multiple_students_on_waiting_list_and_there_is_one_free_place_put_earlier_student_to_info_sent(
            self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2750),
            responses_studentlists.WAITING_LIST_TWO_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2790),
            responses_students.FAKE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2796),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2601,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)

    def test_there_are_multiple_students_on_waiting_list_and_there_are_two_free_places_put_both_students_to_info_sent(
            self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2750),
            responses_studentlists.WAITING_LIST_TWO_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2790),
            responses_students.FAKE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2796),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2601,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE
        )

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2602,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)

    def test_there_are_5_students_on_the_waiting_list_and_there_are_two_free_places_put_the_earliest_two_to_info_sent(
            self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2750),
            responses_studentlists.WAITING_LIST_FIVE_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2798),
            responses_students.FAKE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2790),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2799),
            responses_students.FAKE_STUDENT_APPLIED_LATER)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2796),
            responses_students.FAKE_STUDENT_4TH_APPLIED)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2797),
            responses_students.FAKE_STUDENT_5TH_APPLIED)

        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2601,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE
        )

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2602,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            responses_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_FULL
        )

        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_facade)
