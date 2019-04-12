from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import datetime


class TestRegisterNewApplicants(MiniCrmTestBase):

    def test_headcount_is_1_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_1_student')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_headcount_is_1_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_1_student')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_headcount_is_2_when_there_are_no_students_for_this_course_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_2_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_headcount_is_1_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_1_student')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_info_sent')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":1}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_headcount_is_2_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_2_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_info_sent')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":1}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_headcount_is_0_when_there_is_1_info_sent_student_and_noone_else_count_is_set_to_1(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_info_sent')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":1}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_active_student_count_is_set_to_1(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_active')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":1}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_active_and_1_info_sent_count_is_set_to_2(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_active_and_one_info_sent')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":2}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_did_not_answer_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_did_not_answer')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_cancelled_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_cancelled')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_not_payed_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_not_payed')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_spectator_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_spectator')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_waiting_list_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_waiting_list')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_subscribed_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_subscribed')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_applied_count_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_applied')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_finished_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_finished')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_is_1_student_in_unsubscribed_is_set_to_0(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_one_unsubscribed')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":0}),
            'xput_response')
        self.crm_data.update_headcounts()

    def test_there_are_2_info_sent_3_active_2_waiting_list_1_did_not_answer_1_spectator_count_is_set_to_5(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q_0_students')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'student_list_complex')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":5}),
            'xput_response')
        self.crm_data.update_headcounts()
