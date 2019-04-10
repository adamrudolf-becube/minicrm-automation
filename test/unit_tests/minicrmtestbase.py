import unittest
from crmdata import CrmData
from minicrmcommandfactory import MinicrmCommandFactory
from commonfunctions import load_api_info
import datetime
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock


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
            'category_01')
        self.command_handler.expect_command(
            self.crm_command_factory.get_schema_for_module_number(20),
            'project_20_01')
        self.command_handler.expect_command(
            self.crm_command_factory.get_schema_for_module_number(21),
            'schema_project_21')

    def set_participant_number_expectations(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2753),
            'status_id_2753_one_course_open'
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_project(2037),
            'project_2037_2019-1_Q'
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_student_list_by_course_code("2019-1-Q"),
            'tanfolyam_kodja_2019_1_Q'
        )
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2037, {"AktualisLetszam":6}),
            'xput_response'
        )
