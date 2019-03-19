from test.unit_tests.minicrmtestbase import MiniCrmTestBase


class TestRegisterNewApplicants(MiniCrmTestBase):
    def test_no_new_applicant_do_nothing(self):
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2741"', "empty_new_applicant_list")
        self.crm_data.register_new_applicants()

    def test_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2741"',
            "one_new_applicant_list")
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2941"',
            'project_2601_fake_student')

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_one_place_free')

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/22"',
            'places_schema'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?CategoryId=22"',
            'places_list'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/19"',
            'pannon_kincstar_data'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d',
            'xput_response')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"StatusId":"2781","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l"}\'',
            'xput_response'
        )
        self.crm_data.register_new_applicants()

    def test_advanced_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2741"',
            "one_new_applicant_list")
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2941"',
            'fake_student_advanced')

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_advanced_one_place_free')

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/22"',
            'places_schema'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?CategoryId=22"',
            'places_list'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/19"',
            'pannon_kincstar_data'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d',
            'xput_response')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"StatusId":"2781","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Halad\u00f3 INFO lev\u00e9l"}\'',
            'xput_response'
        )
        self.crm_data.register_new_applicants()

    def test_student_is_applied_course_doesnt_exist_raise_task_with_errormessage(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2741"',
            "one_new_applicant_list")
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2941"',
            'project_2601_fake_student_nonexistent_course')

        for i in range(1, 76):
            self.command_handler.expect_command(
                "curl -s --user FakeUserName:FakeApiKey \"https://r3.minicrm.hu/Api/R3/Project/",
                'project_2037_2019-1_Q_one_place_free')

        self.command_handler.expect_command(
            'curl -XPUT https://FakeUserName:FakeApiKey@r3.minicrm.hu/Api/R3/ToDo/ -d ',
            'xput_response')

        self.crm_data.register_new_applicants()

    def test_student_is_applied_headcount_is_not_less_than_the_limit_put_student_to_waiting_list_and_send_mail(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2741"',
            "one_new_applicant_list")
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2941"',
            'project_2601_fake_student')

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_full')

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/22"',
            'places_schema'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?CategoryId=22"',
            'places_list'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/19"',
            'pannon_kincstar_data'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d',
            'xput_response')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"StatusId":"2750","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, V\u00e1r\u00f3lista"}\'',
            'xput_response'
        )
        self.crm_data.register_new_applicants()