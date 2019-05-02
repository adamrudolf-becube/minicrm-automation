# -*- coding: utf-8 -*-
from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import minicrmcommandfactory
from functionalities.registernewapplicants import register_new_applicants
import test.minicrm_api_mock.api_outputs as apioutputs
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.courses as apioutputs_courses
import test.minicrm_api_mock.apioutputs.courselists as apioutputs_courselists
import test.minicrm_api_mock.apioutputs.students as apioutputs_students
import test.minicrm_api_mock.apioutputs.studentlists as apioutputs_studentlists
import test.minicrm_api_mock.apioutputs.locations as apioutputs_locations
import test.minicrm_api_mock.apioutputs.locationlists as apioutputs_locationlists




class TestRegisterNewApplicants(MiniCrmTestBase):
    def test_no_new_applicant_do_nothing(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2741),
            apioutputs_general.EMPTY_LIST
        )
        register_new_applicants(self.crm_data)

    def test_student_is_applied_headcount_is_less_than_the_limit_put_student_to_infosent_update_headcounts_copy_course_data(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2741),
            apioutputs_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs_students.FAKE_STUDENT_ZERO_MAILS)

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs_courses.COURSE_2019_1_Q_ONE_PLACE_FREE
        )

        self.command_handler.expect_command(
            self.crm_command_factory.get_location_list_by_location_name(u"Pannon Kincstár"),
            apioutputs_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_location(19),
            apioutputs_locations.PANNON_KINCSTAR
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
            apioutputs_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs_students.FAKE_STUDENT_ADVANCED_ZERO_MAILS)

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs_courses.COURSE_2019_1_Q_ADVANCED_ONE_PLACE_FREE)

        self.command_handler.expect_command(
            self.crm_command_factory.get_location_list_by_location_name(u"Pannon Kincstár"),
            apioutputs_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_location(19),
			apioutputs_locations.PANNON_KINCSTAR
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
            apioutputs_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs_students.FAKE_STUDENT_NONEXISTENT_COURSE
        )

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("NONEXISTENT"),
            apioutputs_general.EMPTY_LIST
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
            apioutputs_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2941),
            apioutputs_students.FAKE_STUDENT)

        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs_courses.COURSE_2019_1_Q_FULL)
        self.command_handler.expect_command(
            self.crm_command_factory.get_location_list_by_location_name(u"Pannon Kincstár"),
            apioutputs_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_location(19),
			apioutputs_locations.PANNON_KINCSTAR
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
