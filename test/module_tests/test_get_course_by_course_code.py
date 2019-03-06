import unittest
from becube_crm_library import *
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"



class TestGetCourseByCourseCode(unittest.TestCase):
    def setUp(self):
        self.command_handler = CommandHandlerMock()
        system_id, api_key = load_api_info(API_INFO_JSON_FILE)

        self.expect_crmdata_constructor()

        self.crm_data = CrmData(system_id, api_key, self.command_handler, datetime.datetime(2019, 1, 21, 7, 30))

    def tearDown(self):
        self.command_handler.check_is_satisfied()

    def expect_crmdata_constructor(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Category"',
            'category_01')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/20"',
            'project_20_01')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?CategoryId=20"',
            'category_id_20')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/21"',
            'schema_project_21')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?CategoryId=21"',
            'category_id_21')

    def test_get_course_by_course_code_returns_correct_course(self):
        wanted_course_code = "2019-1-Q"
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q'
        )
        course_info = self.crm_data.tanfolymok.get_course_by_course_code(wanted_course_code)
        self.assertEqual(course_info["TanfolyamBetujele"], wanted_course_code)
