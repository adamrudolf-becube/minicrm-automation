# -*- coding: utf-8 -*-
from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import minicrmcommandfactory
from functionalities.registernewapplicants import register_new_applicants
import test.minicrm_api_mock.api_outputs as apioutputs
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.students as apioutputs_students



class TestRegisterNewApplicants(MiniCrmTestBase):
    def test_no_new_applicant_do_nothing(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2741),
            apioutputs.API_OUTPUTS["empty_new_applicant_list"]
        )
        register_new_applicants(self.crm_data)

    def test_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2741),
            apioutputs.API_OUTPUTS["one_new_applicant_list"])
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs_students.FAKE_STUDENT_ZERO_MAILS)

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_one_place_free']
        )

        self.command_handler.expect_command(
            self.crm_command_factory.get_location_list_by_location_name(u"Pannon Kincstár"),
            apioutputs.API_OUTPUTS['location_list_for_location_name']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_location(19),
            apioutputs.API_OUTPUTS['pannon_kincstar_data']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2601, minicrmcommandfactory._),
            apioutputs_general.XPUT_RESPONSE
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {u"StatusId": u"2781", u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l"}
            ),
            apioutputs_general.XPUT_RESPONSE
        )
        register_new_applicants(self.crm_data)

    def test_advanced_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2741),
            apioutputs.API_OUTPUTS["one_new_applicant_list"])
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs.API_OUTPUTS['fake_student_advanced_zero_mails'])

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_advanced_one_place_free'])

        self.command_handler.expect_command(
            self.crm_command_factory.get_location_list_by_location_name(u"Pannon Kincstár"),
            apioutputs.API_OUTPUTS['location_list_for_location_name']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_location(19),
            apioutputs.API_OUTPUTS['pannon_kincstar_data']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2601, minicrmcommandfactory._),
            apioutputs_general.XPUT_RESPONSE
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {u"StatusId": u"2781", u"Levelkuldesek": u"Halad\u00f3 INFO lev\u00e9l"}
            ),
            apioutputs_general.XPUT_RESPONSE
        )
        register_new_applicants(self.crm_data)

    def test_student_is_applied_course_doesnt_exist_raise_task_with_errormessage(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2741),
            apioutputs.API_OUTPUTS["one_new_applicant_list"])
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs.API_OUTPUTS['project_2601_fake_student_nonexistent_course']
        )

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("NONEXISTENT"),
            apioutputs.API_OUTPUTS['course_list_for_nonexistent_course_code']
        )

        self.command_handler.expect_command(
            self.crm_command_factory.raise_task(
                minicrmcommandfactory._,
                minicrmcommandfactory._,
                minicrmcommandfactory._),
            apioutputs_general.XPUT_RESPONSE
        )

        register_new_applicants(self.crm_data)

    def test_student_is_applied_headcount_is_not_less_than_the_limit_put_student_to_waiting_list_and_send_mail(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2741),
            apioutputs.API_OUTPUTS["one_new_applicant_list"])
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs_students.FAKE_STUDENT)

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_full'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_location_list_by_location_name(u"Pannon Kincstár"),
            apioutputs.API_OUTPUTS['location_list_for_location_name']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_location(19),
            apioutputs.API_OUTPUTS['pannon_kincstar_data']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2601, minicrmcommandfactory._),
            apioutputs_general.XPUT_RESPONSE
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {u"StatusId": u"2750", u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, V\u00e1r\u00f3lista"}
            ),
            apioutputs_general.XPUT_RESPONSE
        )
        register_new_applicants(self.crm_data)
