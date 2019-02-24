import unittest
from becube_crm_library import *
from minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"



class TestHandleWaitingList(unittest.TestCase):
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

    def test_there_is_one_student_on_waiting_list_but_there_are_no_free_places_do_nothing(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2750"',
            'waiting_list_one_student_status_2750')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2790"',
            'project_2601_fake_student')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_full'
        )
        self.set_participant_number_expectations()
        self.crm_data.handle_waiting_list()

    def test_there_are_multiple_students_on_waiting_list_but_there_are_no_free_places_do_nothing(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2750"',
            'waiting_list_two_students_status_2750')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2790"',
            'project_2601_fake_student')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2796"',
            'project_later_fake_student')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_full'
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_full'
        )
        self.set_participant_number_expectations()
        self.crm_data.handle_waiting_list()

    def test_there_is_one_student_on_waiting_list_and_there_is_one_free_place_put_student_to_info_sent(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2750"',
            'waiting_list_one_student_status_2750')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2790"',
            'project_2601_fake_student')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_one_place_free')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"StatusId":"2781","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"}\'',
            'xput_response')
        self.set_participant_number_expectations()
        self.crm_data.handle_waiting_list()

    def test_there_are_multiple_students_on_waiting_list_and_there_is_one_free_place_put_earlier_student_to_info_sent(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2750"',
            'waiting_list_two_students_status_2750')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2790"',
            'project_2601_fake_student')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2796"',
            'project_later_fake_student')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_one_place_free')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"StatusId":"2781","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"}\'',
            'xput_response')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_full'
        )
        self.set_participant_number_expectations()
        self.crm_data.handle_waiting_list()

    def test_there_are_multiple_students_on_waiting_list_and_there_are_two_free_places_put_both_students_to_info_sent(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2750"',
            'waiting_list_two_students_status_2750')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2790"',
            'project_2601_fake_student')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2796"',
            'project_later_fake_student')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_one_place_free')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"StatusId":"2781","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"}\'',
            'xput_response')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_one_place_free'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2602" -d \'{"StatusId":"2781","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"}\'',
            'xput_response')
        self.set_participant_number_expectations()
        self.crm_data.handle_waiting_list()

    def test_there_are_5_students_on_the_waiting_list_and_there_are_two_free_places_put_the_earliest_two_to_info_sent(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2750"',
            'waiting_list_five_students_status_2750')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2798"',
            'project_2601_fake_student')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2790"',
            'project_later_fake_student')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2799"',
            'project_later_fake_student')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2796"',
            'project_fourth_fake_student')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2797"',
            'project_fifth_fake_student')

        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_one_place_free')
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2601" -d \'{"StatusId":"2781","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"}\'',
            'xput_response')
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_one_place_free'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2602" -d \'{"StatusId":"2781","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"}\'',
            'xput_response')

        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_full'
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_full'
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q_full'
        )

        self.set_participant_number_expectations()
        self.crm_data.handle_waiting_list()

if __name__ == '__main__':
    unittest.main()