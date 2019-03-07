import unittest
from becube_crm_library import *
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"


class TestSendScheduledMails(unittest.TestCase):
    def setUp(self):
        self.command_handler = CommandHandlerMock()
        system_id, api_key = load_api_info(API_INFO_JSON_FILE)

        self.expect_crmdata_constructor()

        self.crm_data = CrmData(system_id, api_key, self.command_handler, datetime.datetime(2019, 1, 25, 7, 30))

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2749"',
            'list_of_active_studetns_only_one_student'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2784"',
            'empty_student_list'
        )

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

    def test_beginner_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student'
        )
        self.crm_data.send_scheduled_emails()

    def test_beginner_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_beginner_date_is_after_1st_occasion_send_first_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_beginner_if_no_change_in_sent_mails_dont_send_update(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student_1st_mail_already_sent'
        )
        self.crm_data.send_scheduled_emails()

    def test_beginner_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        self.crm_data.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_beginner_if_second_break_is_coming_send_second_break_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student_3_breaks'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 1. sz\u00fcnet, 2. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_beginner_if_third_break_is_coming_send_third_break_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student_3_breaks'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 1. sz\u00fcnet, 2. sz\u00fcnet, 3. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_send_final_mail_1_day_after_last_occasion(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, \u00datraval\u00f3, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student_good_for_certification'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"StatusId":"2743","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, \u00datraval\u00f3, Oklev\u00e9l - kezd\u0151, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"StatusId":"2743","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, \u00datraval\u00f3, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_advanced'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_date_is_after_1st_occasion_send_first_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_if_no_change_in_sent_mails_dont_send_update(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_1st_mail_already_sent_advanced'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        self.crm_data.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_if_second_break_is_coming_send_second_break_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_advanced_3_breaks'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 1. sz\u00fcnet, 2. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_if_third_break_is_coming_send_third_break_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_advanced_3_breaks'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 1. sz\u00fcnet, 2. sz\u00fcnet, 3. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_send_final_mail_1_day_after_last_occasion(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_good_for_certification_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"StatusId":"2743","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, Oklev\u00e9l - halad\u00f3, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"StatusId":"2743","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_beginner_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_beginner'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_beginner_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_beginner'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_beginner_date_is_after_1st_occasion_send_first_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_beginner'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_beginner_if_no_change_in_sent_mails_dont_send_update(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student_1st_mail_already_sent_company_beginner'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_beginner_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        self.crm_data.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'project_2601_fake_student'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_beginner_dont_send_final_mail_1_day_after_last_occasion(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_beginner'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_beginner_dont_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_good_for_certification_company_beginner'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"StatusId":"2743","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_beginner_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_beginner'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"StatusId":"2743","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_advanced_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_advanced'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_advanced_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_comppany_advanced_date_is_after_1st_occasion_send_first_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_advanced_if_no_change_in_sent_mails_dont_send_update(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_1st_mail_already_sent_company_advanced'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_advanced_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        self.crm_data.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_advanced_if_second_break_is_coming_send_second_break_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_advanced_3_breaks'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 1. sz\u00fcnet, 2. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_advanced_if_third_break_is_coming_send_third_break_email(self):
        self.crm_data.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_advanced_3_breaks'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 1. sz\u00fcnet, 2. sz\u00fcnet, 3. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_advanced_send_final_mail_1_day_after_last_occasion(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_company_advanced_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_good_for_certification_company_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"StatusId":"2743","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, Oklev\u00e9l - halad\u00f3, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()

    def test_advanced_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/2126"',
            'fake_student_company_advanced'
        )
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey -XPUT "https://r3.minicrm.hu/Api/R3/Project/2126" -d \'{"StatusId":"2743","Levelkuldesek":"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, Oklev\u00e9l - halad\u00f3, 1. sz\u00fcnet"}\'',
            'xput_response'
        )
        self.crm_data.send_scheduled_emails()