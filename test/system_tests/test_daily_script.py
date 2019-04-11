from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import daily_script


class TestDailyScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):

        self.expect_send_scheduled_mails()
        self.expect_set_course_states()

        daily_script.run(self.crm_data)

    def expect_send_scheduled_mails(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2749),
            'list_of_active_studetns_only_one_student'
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2784),
            'empty_student_list'
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2126),
            'project_2601_fake_student'
        )

    def expect_set_course_states(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2758),
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2797),
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            'project_2037_2019-1_Q')
