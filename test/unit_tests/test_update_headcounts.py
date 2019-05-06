import crmrequestfactory
import test.requesthandlermock.responses.courselists as responses_courselists
import test.requesthandlermock.responses.courses as responses_courses
import test.requesthandlermock.responses.general as responses_general
import test.requesthandlermock.responses.studentlists as responses_studentlists
from test.unit_tests.minicrmtestbase import MiniCrmTestBase


class TestUpdateHeadcounts(MiniCrmTestBase):

    def test_headcount_is_1_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_1_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_1_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_1_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_2_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_2_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_1_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_1_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 1}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_2_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_2_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 1}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_headcount_is_0_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 1}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_active_student_count_is_set_to_1(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.ACTIVE_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 1}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_active_and_1_info_sent_count_is_set_to_2(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.ONE_ACTIVE_AND_ONE_INFO_SENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 2}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_did_not_answer_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.DID_NOT_ANSERT_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_cancelled_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.CANCELLED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_not_payed_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.NOT_PAYED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_spectator_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.SPECTATORS_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_waiting_list_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_subscribed_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.SUBSCRIBED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_applied_count_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.APPLIED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_finished_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.FINISHED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_is_1_student_in_unsubscribed_is_set_to_0(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.UNSUBSCRIBED_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 0}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()

    def test_there_are_2_info_sent_3_active_2_waiting_list_1_did_not_answer_1_spectator_count_is_set_to_5(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.COMPLEX_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam": 5}),
            responses_general.XPUT_RESPONSE)
        self.crm_facade.update_headcounts()
