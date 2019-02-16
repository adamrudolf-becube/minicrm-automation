import unittest
from becube_crm_library import *
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "../api_info_fake.json"



class TestInfoSent(unittest.TestCase):
    def setUp(self):
        self.command_handler = CommandHandlerMock()
        system_id, api_key = load_api_info(API_INFO_JSON_FILE)

        self.expect_crmdata_constructor()

        self.crm_data = CrmData(system_id, api_key, self.command_handler, datetime.datetime(2019, 1, 21, 7, 30))

    def expect_crmdata_constructor(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Category"',
            'api_outputs/category_01.json')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/20"',
            'api_outputs/project_20_01.json')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?CategoryId=20"',
            'api_outputs/category_id_20.json')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/21"',
            'api_outputs/schema_project_21.json')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?CategoryId=21"',
            'api_outputs/category_id_21.json')

    def set_participant_number_expectations(self):
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"', 'api_outputs/status_id_2753_one_course_open.json')

        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2037"', 'api_outputs/project_2037.json')
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja=2019-1-Q"', 'api_outputs/tanfolyam_kodja_2019_1_Q.json')
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"AktualisLetszam":6}\'', 'api_outputs/xput_2037.json')

    def test_student_did_not_finalize_deadline_has_not_spent_but_within_24_hours_send_reminder(self):
        """
        Given:
        When:
        Then:
        """

        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2781"', 'api_outputs/status_id_2781_one_student_info_sent.json')
        self.set_participant_number_expectations()
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2601"', "api_outputs/project_2601_fake_student.json")
        self.set_participant_number_expectations()

        self.crm_data.clean_info_level_kiment()

    #def test_student_did_not_finalize_deadline_has_not_spent_but_within_24_hours_send_reminder(self):
    #    pass

    #def test_student_did_not_finalize_deadline_has_spent_but_not_more_than_24_hours_ago_send_reminder_raise_task(self):
    #    pass

    #def test_student_did_not_finalize_deadline_has_spent_more_than_24_hours_ago_delete(self):
    #    pass

    def test_student_did_not_finalize_and_deadline_is_more_than_1_day_away_do_nothing(self):

        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2781"', 'api_outputs/status_id_2781_one_student_info_sent.json')
        self.set_participant_number_expectations()
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2601"', "api_outputs/project_2601_fake_student.json")
        self.set_participant_number_expectations()

        self.crm_data.clean_info_level_kiment()


if __name__ == '__main__':
    unittest.main()