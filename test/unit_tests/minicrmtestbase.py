import unittest
from crmdata import CrmData
from minicrmcommandfactory import MinicrmCommandFactory
from commonfunctions import load_api_info
import datetime
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock
import test.minicrm_api_mock.api_outputs as apioutputs
import test.minicrm_api_mock.apioutputs.general as apioutputs_general


API_INFO_JSON_FILE = "api_info_fake.json"


class MiniCrmTestBase(unittest.TestCase, object):
    def setUp(self):
        self.command_handler = CommandHandlerMock()
        system_id, api_key = load_api_info(API_INFO_JSON_FILE)
        self.crm_command_factory = MinicrmCommandFactory(system_id, api_key)

        self.expect_crmdata_constructor()
        self.crm_data = CrmData(system_id, api_key, self.command_handler, datetime.datetime(2019, 1, 25, 7, 30))

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
            apioutputs.API_OUTPUTS['status_id_2753_one_course_open']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_project(2037),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['tanfolyam_kodja_2019_1_Q']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {"AktualisLetszam":6}),
            apioutputs.API_OUTPUTS['xput_response']
        )
