from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.courselists as apioutputs_courselists
import test.minicrm_api_mock.apioutputs.courses as apioutputs_courses
import test.minicrm_api_mock.apioutputs.studentlists as apioutputs_studentlists


class TestUpdateHeadcounts(MiniCrmTestBase):

    def test_headcount_is_1_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_1_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_headcount_is_1_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_1_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_headcount_is_2_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_2_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_headcount_is_1_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_1_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.INFO_SENT_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":1}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_headcount_is_2_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_2_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.INFO_SENT_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":1}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_headcount_is_0_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.INFO_SENT_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":1}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_active_student_count_is_set_to_1(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.ACTIVE_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":1}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_active_and_1_info_sent_count_is_set_to_2(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.ONE_ACTIVE_AND_ONE_INFO_SENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":2}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_did_not_answer_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.DID_NOT_ANSERT_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_cancelled_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.CANCELLED_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_not_payed_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.NOT_PAYED_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_spectator_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.SPECTATORS_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_waiting_list_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.WAITING_LIST_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_subscribed_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.SUBSCRIBED_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_applied_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.APPLIED_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_finished_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.FINISHED_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_unsubscribed_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.UNSUBSCRIBED_ONE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()

    def test_there_are_2_info_sent_3_active_2_waiting_list_1_did_not_answer_1_spectator_count_is_set_to_5(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_0_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.COMPLEX_LIST)
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":5}),
            apioutputs_general.XPUT_RESPONSE)
        self.crm_data.update_headcounts()
