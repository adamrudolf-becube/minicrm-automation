import unittest
from becube_crm_library import *
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"


class TestGetApplicationDeadline(unittest.TestCase):
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

    def set_course(self, api_response):
        self.command_handler.expect_command('ASDF', api_response)
        self.course_data = self.command_handler.get_json_array_for_command("ASDF")

    def test_if_course_starts_in_not_less_than_7_days_away_and_more_than_places_30_percent_if_free_deadline_is_5_days(self):
        self.set_course('project_2037_2019-1_Q')
        self.crm_data.set_today(datetime.datetime(2019, 1, 10, 9, 8))
        self.assertEqual("2019-01-15 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_course_starts_in_less_than_7_days_away_and_more_than_places_30_percent_if_free_deadline_is_3_days(self):
        self.set_course('project_2037_2019-1_Q')
        self.crm_data.set_today(datetime.datetime(2019, 1, 23, 9, 8))
        self.assertEqual("2019-01-26 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_course_starts_in_not_less_than_7_days_away_and_less_than_places_30_percent_if_free_deadline_is_3_days(self):
        self.set_course('project_2037_2019-1_Q_one_place_free')
        self.crm_data.set_today(datetime.datetime(2019, 1, 10, 9, 8))
        self.assertEqual("2019-01-13 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_course_starts_in_less_than_3_days_and_there_is_no_more_than_3_places_deadline_is_1_day(self):
        self.set_course('project_2037_2019-1_Q_one_place_free')
        self.crm_data.set_today(datetime.datetime(2019, 1, 26, 9, 8))
        self.assertEqual("2019-01-27 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_course_start_is_earlier_than_the_calculated_deadline_deadline_is_course_start_minus_one_day(self):
        self.set_course('project_2037_2019-1_Q')
        self.crm_data.set_today(datetime.datetime(2019, 1, 26, 9, 8))
        self.assertEqual("2019-01-27 23:59:59", self.crm_data.get_application_deadline(self.course_data))

    def test_if_deadline_is_earlier_than_today_deadline_is_today_plus_one_day(self):
        self.set_course('project_2037_2019-1_Q')
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 9, 8))
        self.assertEqual("2019-01-30 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_all_spots_is_zero_function_does_not_raise(self):
        self.set_course('course_max_spots_is_zero')
        self.crm_data.get_application_deadline(self.course_data)
