import unittest
from becube_crm_library import *
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"

class TestInfoSent(unittest.TestCase):
    # TODO find a nice structure fr responses which are easy to read, like ["Schemas"]["Course (21)"], or ["Course lists"]["Open courses (2753)"]["One course open"] or similar
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

    def set_participant_number_expectations(self):
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"', 'status_id_2753_one_course_open')

        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"', 'project_2037_2019-1_Q')
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja=2019-1-Q"', 'tanfolyam_kodja_2019_1_Q')
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"AktualisLetszam":6}\'', 'xput_response')

    def test_student_did_not_finalize_deadline_has_not_spent_but_within_24_hours_send_reminder(self):

        self.crm_data.set_today(datetime.datetime(2019, 1, 22, 12, 0))

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2781"',
            'status_id_2781_one_student_info_sent')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2601"',
            "project_2601_fake_student")

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni"}\'',
            'xput_response')

        self.set_participant_number_expectations()

        self.crm_data.clean_info_level_kiment()

    def test_student_did_not_finalize_deadline_has_spent_but_not_more_than_24_hours_ago_send_reminder_raise_task(self):

        self.crm_data.set_today(datetime.datetime(2019, 1, 23, 12, 0))

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2781"',
            'status_id_2781_one_student_info_sent')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2601"',
            "project_2601_fake_student")

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni, Ma kell jelentkezni"}\'',
            'xput_response')

        self.set_participant_number_expectations()

        self.crm_data.clean_info_level_kiment()

    def test_student_did_not_finalize_deadline_has_spent_more_than_24_hours_ago_delete(self):

        self.crm_data.set_today(datetime.datetime(2019, 1, 24, 12, 0))

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2781"',
            'status_id_2781_one_student_info_sent')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2601"',
            "project_2601_fake_student")

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"StatusId":"2782","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni, Ma kell jelentkezni, Toroltunk"}\'',
            'xput_response')

        self.set_participant_number_expectations()

        self.crm_data.clean_info_level_kiment()

    def test_student_did_not_finalize_and_deadline_is_more_than_1_day_away_do_nothing(self):

        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2781"', 'status_id_2781_one_student_info_sent')
        self.set_participant_number_expectations()
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2601"', "project_2601_fake_student")
        self.set_participant_number_expectations()

        self.crm_data.clean_info_level_kiment()


if __name__ == '__main__':
    unittest.main()