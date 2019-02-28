import unittest
from becube_crm_library import *
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"


class TestOkForCertification(unittest.TestCase):
    def setUp(self):
        self.command_handler = CommandHandlerMock()
        system_id, api_key = load_api_info(API_INFO_JSON_FILE)

        self.expect_crmdata_constructor()
        self.crm_data = CrmData(system_id, api_key, self.command_handler, datetime.datetime(2019, 1, 25, 7, 30))

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

    def test_no_attendance_no_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'project_2601_fake_student')
        self.student_data = self.crm_data.get_project(42)
        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))

    def test_full_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'project_2601_fake_student_good_for_certification')
        self.student_data = self.crm_data.get_project(42)

        self.assertTrue(self.crm_data.ok_for_certification(self.student_data))

    def test_full_attendance_no_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_full_attendance_no_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))

    def test_no_attendance_full_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_no_attendance_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))

    def test_full_attendance_one_missing_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_full_attendance_almost_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))

    def test_9_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_9_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertTrue(self.crm_data.ok_for_certification(self.student_data))

    def test_8_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_8_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertTrue(self.crm_data.ok_for_certification(self.student_data))

    def test_7_attendance_full_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_7_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))