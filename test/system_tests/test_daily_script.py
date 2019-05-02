from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import daily_script
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.courselists as apioutputs_courselists
import test.minicrm_api_mock.apioutputs.courses as apioutputs_courses
import test.minicrm_api_mock.apioutputs.students as apioutputs_students
import test.minicrm_api_mock.apioutputs.studentlists as apioutputs_studentlists

class TestDailyScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):

        self.expect_send_scheduled_mails()
        self.expect_set_course_states()

        daily_script.run(self.crm_data)

    def expect_send_scheduled_mails(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2749),
            apioutputs_studentlists.ACTIVE_ONE_STUDENT 
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2784),
            apioutputs_general.EMPTY_LIST
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs_students.FAKE_STUDENT
        )

    def expect_set_course_states(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q)
