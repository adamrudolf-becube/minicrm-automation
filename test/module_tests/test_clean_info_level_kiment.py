from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import datetime
from functionalities.clean_info_sent import clean_info_level_kiment


class TestInfoSent(MiniCrmTestBase):
    # TODO find a nice structure fr responses which are easy to read, like ["Schemas"]["Course (21)"], or ["Course lists"]["Open courses (2753)"]["One course open"] or similar
    def setUp(self):
        super(TestInfoSent, self).setUp()
        self.crm_data.set_today(datetime.datetime(2019, 1, 21, 7, 30))

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

        clean_info_level_kiment(self.crm_data)

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

        clean_info_level_kiment(self.crm_data)

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

        clean_info_level_kiment(self.crm_data)

    def test_student_did_not_finalize_and_deadline_is_more_than_1_day_away_do_nothing(self):

        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2781"', 'status_id_2781_one_student_info_sent')
        self.set_participant_number_expectations()
        self.command_handler.expect_command('curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2601"', "project_2601_fake_student")
        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_data)