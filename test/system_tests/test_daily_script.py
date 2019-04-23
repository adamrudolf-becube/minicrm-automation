from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import daily_script
import test.minicrm_api_mock.api_outputs as apioutputs

class TestDailyScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):

        self.expect_send_scheduled_mails()
        self.expect_set_course_states()

        daily_script.run(self.crm_data)

    def expect_send_scheduled_mails(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2749),
            apioutputs.API_OUTPUTS['list_of_active_studetns_only_one_student']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2784),
            apioutputs.API_OUTPUTS['empty_student_list']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2126),
            apioutputs.API_OUTPUTS['project_2601_fake_student']
        )

    def expect_set_course_states(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs.API_OUTPUTS['status_id_2753_one_course_open'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2758),
            apioutputs.API_OUTPUTS['empty_new_applicant_list'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2797),
            apioutputs.API_OUTPUTS['empty_new_applicant_list'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q'])
