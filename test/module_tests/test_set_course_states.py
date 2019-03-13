from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import datetime


class TestRegisterNewApplicants(MiniCrmTestBase):

    def test_application_is_open_and_first_day_hasnt_spent_do_nothing(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q')
        self.crm_data.set_course_states()

    def test_application_is_open_first_day_spent_but_last_didnt_put_to_in_progress(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"StatusId":"2758"}\'',
            'xput_response')
        self.crm_data.set_course_states()

    def test_in_progress_first_day_is_spent_but_last_didnt_set_state_to_in_rpogress(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q_in_progress')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"StatusId":"2758"}\'',
            'xput_response')
        self.crm_data.set_course_states()

    def test_recently_finished_first_day_spent_but_last_didnt_put_to_in_progress(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q_recently_finished')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"StatusId":"2758"}\'',
            'xput_response')
        self.crm_data.set_course_states()

    def test_in_progress_last_day_has_spent_but_not_35_more_days_put_to_recently_finished(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q_in_progress')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"StatusId":"2797"}\'',
            'xput_response')
        self.crm_data.set_course_states()

    def test_recently_finished_last_day_has_spent_but_not_35_more_put_to_recently_finished(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q_recently_finished')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"StatusId":"2797"}\'',
            'xput_response')
        self.crm_data.set_course_states()

    def test_recently_finished_and_35_days_passed_put_to_closed(self):
        self.crm_data.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q_recently_finished')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"StatusId":"2754"}\'',
            'xput_response')
        self.crm_data.set_course_states()

    def test_first_day_is_missing_no_error_is_raised_state_is_not_changed(self):
        self.crm_data.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q_first_date_missing')
        self.crm_data.set_course_states()

    def test_last_day_is_missing_no_error_is_raised_put_to_in_progress(self):
        self.crm_data.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"',
            'status_id_2753_one_course_open')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2758"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2797"',
            'empty_new_applicant_list')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"',
            'project_2037_2019-1_Q_last_date_missing')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"StatusId":"2758"}\'',
            'xput_response')
        self.crm_data.set_course_states()

    # TODO: [PLANNED] If course is started, put waiting list students to SUBSCRIBED (erdeklodo) state and send mail
