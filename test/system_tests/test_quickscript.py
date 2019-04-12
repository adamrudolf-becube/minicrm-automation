# -*- coding: utf-8 -*-
from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import datetime
import quick_script


class TestQuickScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):

        self.expect_clean_info_sent()
        self.expect_handle_waiting_list()
        self.expect_register_new_applicants()

        quick_script.run(self.crm_data)

    def expect_clean_info_sent(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 22, 12, 0))

        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2781),
            'status_id_2781_one_student_info_sent')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2601),
            "project_2601_fake_student")

        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni"}
            ),
            'xput_response')

        self.set_participant_number_expectations()

    def expect_handle_waiting_list(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2750),
            'waiting_list_one_student_status_2750')
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2790),
            'project_2601_fake_student')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            'course_list_for_course_code'
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            'project_2037_2019-1_Q_full'
        )
        self.set_participant_number_expectations()

    def expect_register_new_applicants(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2741),
            "one_new_applicant_list")
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            'project_2601_fake_student')

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            'course_list_for_course_code'
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            'project_2037_2019-1_Q_one_place_free')

        self.command_handler.expect_command(
            self.crm_command_factory.get_location_list_by_location_name("Pannon Kincstár"),
            'location_list_for_location_name'
        )

        self.command_handler.expect_command(
            self.crm_command_factory.get_location(19),
            'pannon_kincstar_data'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d',
            'xput_response')
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {u"StatusId": u"2781", u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l"}
            ),
            'xput_response'
        )
