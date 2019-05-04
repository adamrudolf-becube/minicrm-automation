# -*- coding: utf-8 -*-
from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import crmrequestfactory
import datetime
import quickscript
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.courses as apioutputs_courses
import test.minicrm_api_mock.apioutputs.courselists as apioutputs_courselists
import test.minicrm_api_mock.apioutputs.studentlists as apioutputs_studentlists
import test.minicrm_api_mock.apioutputs.students as apioutputs_students
import test.minicrm_api_mock.apioutputs.locations as apioutputs_locations
import test.minicrm_api_mock.apioutputs.locationlists as apioutputs_locationlists


class TestQuickScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):

        self.expect_clean_info_sent()
        self.expect_handle_waiting_list()
        self.expect_register_new_applicants()

        quickscript.run(self.crm_data)

    def expect_clean_info_sent(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 22, 12, 0))

        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2781),
            apioutputs_studentlists.ONE_STUDENT_IN_INFO_SENT_STATE)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            crmrequestfactory.get_student(2601),
            apioutputs_students.FAKE_STUDENT)

        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(
                2601,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni"}
            ),
            apioutputs_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

    def expect_handle_waiting_list(self):
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2750),
            apioutputs_studentlists.WAITING_LIST_ONE_STUDENT)
        self.command_handler.expect_command(
            crmrequestfactory.get_student(2790),
            apioutputs_students.FAKE_STUDENT)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.command_handler.expect_command(
            crmrequestfactory.get_course(1164),
            apioutputs_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()

    def expect_register_new_applicants(self):
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2741),
            apioutputs_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.command_handler.expect_command(
            crmrequestfactory.get_student(2941),
            apioutputs_students.FAKE_STUDENT)

        self.command_handler.expect_command(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.command_handler.expect_command(
            crmrequestfactory.get_course(1164),
            apioutputs_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)

        self.command_handler.expect_command(
            crmrequestfactory.get_location_list_by_location_name("Pannon Kincstár"),
            apioutputs_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )

        self.command_handler.expect_command(
            crmrequestfactory.get_location(19),
			apioutputs_locations.PANNON_KINCSTAR
        )
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(2601, crmrequestfactory._),
            apioutputs_general.XPUT_RESPONSE
        )
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(
                2601,
                {u"StatusId": u"2781", u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l"}
            ),
            apioutputs_general.XPUT_RESPONSE
        )
