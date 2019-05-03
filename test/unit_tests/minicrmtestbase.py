import unittest
from crmdata import CrmData
from minicrmcommandfactory import MinicrmCommandFactory
from commonfunctions import load_api_info
import datetime
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.courselists as apioutputs_courselists
import test.minicrm_api_mock.apioutputs.courses as apioutputs_courses
import test.minicrm_api_mock.apioutputs.studentlists as apioutputs_studentlists


API_INFO_JSON_FILE = "api_info_fake.json"


class MiniCrmTestBase(unittest.TestCase, object):
    def setUp(self):
        system_id, api_key = load_api_info(API_INFO_JSON_FILE)
        self.command_handler = CommandHandlerMock(system_id, api_key)
        self.crm_command_factory = MinicrmCommandFactory()

        self.expect_crmdata_constructor()
        self.crm_data = CrmData(self.command_handler, datetime.datetime(2019, 1, 25, 7, 30))

    def tearDown(self):
        self.command_handler.check_is_satisfied()

    def expect_crmdata_constructor(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_modul_dictionary(),
            apioutputs_general.MODULE_LIST)
        self.command_handler.expect_command(
            self.crm_command_factory.get_schema_for_module_number(20),
            apioutputs_general.SCHEMA_PROJECT_20_STUDENTS)
        self.command_handler.expect_command(
            self.crm_command_factory.get_schema_for_module_number(21),
            apioutputs_general.SCHEMA_PRPJECT_21_COURSES)

    def set_participant_number_expectations(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_project(2037),
            apioutputs_courses.COURSE_2019_1_Q
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs_studentlists.COURSE_CODE_IS_2019_1_Q
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {u"AktualisLetszam":6}),
            apioutputs_general.XPUT_RESPONSE
        )
