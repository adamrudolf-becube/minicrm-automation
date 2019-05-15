import datetime

import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.studentlists as responses_studentlists
import requesthandlermock.responses.students as responses_students
from functionalities.sendscheduledmails import ok_for_certification
from functionalities.sendscheduledmails import send_scheduled_emails
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase

ACTIVE_STATUS_NUMBER = 2749
SPECTATOR_STATUS = 2784
FAKE_STUDENT_ID_NUMBER = 2941


class TestSendScheduledMails(MiniCrmTestBase):

    def setUp(self):
        super(TestSendScheduledMails, self).setUp()

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(ACTIVE_STATUS_NUMBER),
            responses_studentlists.ACTIVE_ONE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(SPECTATOR_STATUS),
            responses_general.EMPTY_LIST
        )

    def test_beginner_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_date_is_after_1st_occasion_send_first_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_if_no_change_in_sent_mails_dont_send_update(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_1ST_MAIL_ALREADY_SENT
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        self.crm_facade.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_if_second_break_is_coming_send_second_break_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 1. sz\u00fcnet, 2. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_if_third_break_is_coming_send_third_break_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 1. sz\u00fcnet, 2. sz\u00fcnet, 3. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_send_final_mail_1_day_after_last_occasion(self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, \u00datraval\u00f3, 1. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_GOOD_FOR_CERTIFICATION
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"StatusId": u"2743",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, \u00datraval\u00f3, Oklev\u00e9l - kezd\u0151, 1. sz\u00fcnet"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"StatusId": u"2743",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, \u00datraval\u00f3, 1. sz\u00fcnet"
                }

            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_ID_NUMBER, {
                u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3"}),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_date_is_after_1st_occasion_send_first_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_ID_NUMBER, {
                u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3"}),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_if_no_change_in_sent_mails_dont_send_update(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_1ST_MAIL_ALREADY_SENT_ADVANCED
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        self.crm_facade.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_ID_NUMBER, {
                u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3"}),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_if_second_break_is_coming_send_second_break_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_ID_NUMBER, {
                u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 1. sz\u00fcnet, 2. sz\u00fcnet"}),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_if_third_break_is_coming_send_third_break_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 1. sz\u00fcnet, 2. sz\u00fcnet, 3. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_send_final_mail_1_day_after_last_occasion(self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, 1. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_GOOD_FOR_CERTIFICATION_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"StatusId": u"2743",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, Oklev\u00e9l - halad\u00f3, 1. sz\u00fcnet"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(
            self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"StatusId": u"2743",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, 1. sz\u00fcnet"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_date_is_after_1st_occasion_send_first_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_if_no_change_in_sent_mails_dont_send_update(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_1ST_MAIL_ALREADY_SENT_COMPANY_BEGINNER
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        self.crm_facade.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_dont_send_final_mail_1_day_after_last_occasion(self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, 1. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_dont_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(
            self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_GOOD_FOR_CERTIFICATION_COMPANY_BEGINNER
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"StatusId": u"2743",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, 1. sz\u00fcnet"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(
            self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"StatusId": u"2743",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151, 5. alkalom - kezd\u0151, 6. alkalom - kezd\u0151, 7. alkalom - kezd\u0151, 8. alkalom - kezd\u0151, 9. alkalom - kezd\u0151, 10. alkalom - kezd\u0151, 1. sz\u00fcnet"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_comppany_advanced_date_is_after_1st_occasion_send_first_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_if_no_change_in_sent_mails_dont_send_update(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_1ST_MAIL_ALREADY_SENT_COMPANY_ADVANCED
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        self.crm_facade.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_if_second_break_is_coming_send_second_break_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 1. sz\u00fcnet, 2. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_if_third_break_is_coming_send_third_break_email(self):
        self.crm_facade.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 1. sz\u00fcnet, 2. sz\u00fcnet, 3. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_send_final_mail_1_day_after_last_occasion(self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, 1. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(
            self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_GOOD_FOR_CERTIFICATION_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"StatusId": u"2743",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, Oklev\u00e9l - halad\u00f3, 1. sz\u00fcnet"
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(self):
        self.crm_facade.set_today(datetime.datetime(2019, 4, 10, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    u"StatusId": u"2743",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, 1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3, 5. alkalom - halad\u00f3, 6. alkalom - halad\u00f3, 7. alkalom - halad\u00f3, 8. alkalom - halad\u00f3, 9. alkalom - halad\u00f3, 10. alkalom - halad\u00f3, \u00datraval\u00f3 - halad\u00f3, Oklev\u00e9l - halad\u00f3, 1. sz\u00fcnet"}
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)


class TestOkForCertification(MiniCrmTestBase):

    def test_no_attendance_no_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)
        self.assertFalse(ok_for_certification(self.student_data))

    def test_full_attendance_full_homework_returns_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_GOOD_FOR_CERTIFICATION)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_full_attendance_no_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_FULL_ATTENDANCE_NO_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_no_attendance_full_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_NO_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_full_attendance_one_missing_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_FULL_ATTENDANCE_ALMOST_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_9_attendance_full_homework_returns_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_9_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_8_attendance_full_homework_returns_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_8_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_7_attendance_full_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_7_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertFalse(ok_for_certification(self.student_data))
