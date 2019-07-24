"""
This module contains all of the tests and requirements for the functionality called sendscheduledemails.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

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
        """
        Beginner date is more then delta days less than 1st occasion do nothing

        Given:
            - there is one active beginner student
            - first occasion is more than 3 days away
        When:
            - send_scheduled_emails() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        """
        test_beginner_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email

        Given:
            - there is one active beginner student
            - first occasion os less than 3 days away (but still not spent)
        When:
            - send_scheduled_emails() is called
        Then:
            - first email is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_date_is_after_1st_occasion_send_first_email(self):
        """
        test_beginner_date_is_after_1st_occasion_send_first_email

        Given:
            - there is one active beginner student
            - first occasion is spent
        When:
            - send_scheduled_emails() is called
        Then:
            - first email is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_if_no_change_in_sent_mails_dont_send_update(self):
        """
        test_beginner_if_no_change_in_sent_mails_dont_send_update

        Given:
            - there is one active beginner student
            - all of the needed mails have been already sent
        When:
            - send_scheduled_emails() is called
        Then:
            - don't update student data
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_1ST_MAIL_ALREADY_SENT
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        """
        test_beginner_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails

        Given:
            - there is one active beginner student
            - no mails have been sent
            - more occasions have passed
        When:
            - send_scheduled_emails() is called
        Then:
            - all relevant emails have been sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_if_second_break_is_coming_send_second_break_email(self):
        """
        test_beginner_if_second_break_is_coming_send_second_break_email

        Given:
            - there is one active beginner student
            - it's not less than two days before second dayoff
        When:
            - send_scheduled_emails() is called
        Then:
            - send second dayoff email
        """

        self.crm_facade.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"2. sz\u00fcnet"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_beginner_if_third_break_is_coming_send_third_break_email(self):
        """
        test_beginner_if_third_break_is_coming_send_third_break_email

        Given:
            - there is one active beginner student
            - it's not less than two days before third dayoff
        When:
            - send_scheduled_emails() is called
        Then:
            - send third dayoff email
        """

        self.crm_facade.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"3. sz\u00fcnet"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_send_final_mail_1_day_after_last_occasion(self):
        """
        test_send_final_mail_1_day_after_last_occasion

        Given:
            - there is one active beginner student
            - it's 1 day after last occasion
        When:
            - send_scheduled_emails() is called
        Then:
            - final email is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"\u00datraval\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(self):
        """
        test_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable

        Given:
            - there is one active beginner student
            - it's last occasion plus 2 days
            - student is eligible for certification
        When:
            - send_scheduled_emails() is called
        Then:
            - send certification
            - put state to Finished ("Elvegezte")
        """

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
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"Oklev\u00e9l - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(self):
        """
        test_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable

        Given:
            - there is one active beginner student
            - it's last occasion plus 2 days
            - student is not eligible for certification
        When:
            - send_scheduled_emails() is called
        Then:
            - don't send certification
            - put state to Finished ("Elvegezte")
        """

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
                    crmrequestfactory.EXCLUDES: {
                        u"Levelkuldesek": u"Oklev\u00e9l - kezd\u0151"
                    }
                }

            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        """
        test_advanced_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing

        Given:
            - there is one active advanced student
            - first occasion is more than 3 days away
        When:
            - send_scheduled_emails() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        """
        test_advanced_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email

        Given:
            - there is one active advanced student
            - first occasion os less than 3 days away (but still not spent)
        When:
            - send_scheduled_emails() is called
        Then:
            - first email is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_ID_NUMBER, {
                crmrequestfactory.CONTAINS: {
                    u"Levelkuldesek": u"1. alkalom - halad\u00f3"}
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_date_is_after_1st_occasion_send_first_email(self):
        """
        test_advanced_date_is_after_1st_occasion_send_first_email

        Given:
            - there is one active advanced student
            - first occasion is spent
        When:
            - send_scheduled_emails() is called
        Then:
            - first email is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_ID_NUMBER, {
                crmrequestfactory.CONTAINS: {
                    u"Levelkuldesek": u"1. alkalom - halad\u00f3"}
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_if_no_change_in_sent_mails_dont_send_update(self):
        """
        test_advanced_if_no_change_in_sent_mails_dont_send_update

        Given:
            - there is one active advanced student
            - all scheduled emails have been already spent
        When:
            - send_scheduled_emails() is called
        Then:
            - don't update student data
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_1ST_MAIL_ALREADY_SENT_ADVANCED
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        """
        test_advanced_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails

        Given:
            - there is one active advanced student
            - no emails have been sent out
            - multiple occasions have been spent
        When:
            - send_scheduled_emails() is called
        Then:
            - all relevant mails are sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_ID_NUMBER, {
                crmrequestfactory.CONTAINS: {
                    u"Levelkuldesek": u"1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3"}
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_if_second_break_is_coming_send_second_break_email(self):
        """
        test_advanced_if_second_break_is_coming_send_second_break_email

        Given:
            - there is one active advanced student
            - it's not less than 2 days before the second dayoff
        When:
            - send_scheduled_emails() is called
        Then:
            - second dayoff mail is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_STUDENT_ID_NUMBER, {
                crmrequestfactory.CONTAINS: {
                    u"Levelkuldesek": u"2. sz\u00fcnet"}
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_if_third_break_is_coming_send_third_break_email(self):
        """
        test_advanced_if_third_break_is_coming_send_third_break_email

        Given:
            - there is one active advanced student
            - it's not less than 2 days before the third dayoff
        When:
            - send_scheduled_emails() is called
        Then:
            - third dayoff mail is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"3. sz\u00fcnet"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_send_final_mail_1_day_after_last_occasion(self):
        """
        test_advanced_send_final_mail_1_day_after_last_occasion

        Given:
            - there is one active advanced student
            - it's 1 day after last occasion
        When:
            - send_scheduled_emails() is called
        Then:
            - final mail is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"\u00datraval\u00f3 - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(self):
        """
        test_advanced_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable

        Given:
            - there is one active advanced student
            - it's last occasion plus 2 days
            - student is eligible for certification
        When:
            - send_scheduled_emails() is called
        Then:
            - advanced certification is sent
            - student is put to Finished ("Elvegezte") state
        """

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
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"Oklev\u00e9l - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(
            self):
        """
        test_advanced_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable

        Given:
            - there is one active advanced student
            - it's last occasion plus 2 days
            - student is not eligible for certification
        When:
            - send_scheduled_emails() is called
        Then:
            - advanced certification is not sent
            - student is put to Finished ("Elvegezte") state
        """

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
                    crmrequestfactory.EXCLUDES: {
                        u"Levelkuldesek": u"Oklev\u00e9l - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        """
        test_company_beginner_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing

        Given:
            - there is one active company beginner student
            - first occasion is more than 3 days away
        When:
            - send_scheduled_emails() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        """
        test_company_beginner_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email

        Given:
            - there is one active company beginner student
            - first occasion is less than 3 days away, but not spent
        When:
            - send_scheduled_emails() is called
        Then:
            - send beginner first mail
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_date_is_after_1st_occasion_send_first_email(self):
        """
        test_company_beginner_date_is_after_1st_occasion_send_first_email

        Given:
            - there is one active company beginner student
            - first occasion spent
        When:
            - send_scheduled_emails() is called
        Then:
            - send beginner first mail
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_if_no_change_in_sent_mails_dont_send_update(self):
        """
        test_company_beginner_if_no_change_in_sent_mails_dont_send_update

        Given:
            - there is one active company beginner student
            - first occasion spent
        When:
            - send_scheduled_emails() is called
        Then:
            - send beginner first mail
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_1ST_MAIL_ALREADY_SENT_COMPANY_BEGINNER
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        """
        test_company_beginner_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails

        Given:
            - there is one active company beginner student
            - no mails have been sent
            - multiple occasions have passed
        When:
            - send_scheduled_emails() is called
        Then:
            - all relevant mails are sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - kezd\u0151, 2. alkalom - kezd\u0151, 3. alkalom - kezd\u0151, 4. alkalom - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_dont_send_final_mail_1_day_after_last_occasion(self):
        """
        test_company_beginner_dont_send_final_mail_1_day_after_last_occasion

        Given:
            - there is one active company beginner student
            - it's last occasion plus 1 day
        When:
            - send_scheduled_emails() is called
        Then:
            - last mail is NOT sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_BEGINNER
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.EXCLUDES: {
                        u"Levelkuldesek": u"\u00datraval\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_dont_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(
            self):
        """
        test_company_beginner_dont_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable

        Given:
            - there is one active company beginner student
            - it's 2 days after last occasion
            - student is eligible for certification
        When:
            - send_scheduled_emails() is called
        Then:
            - don't send certification
            - put student to Finished ("Elvegezte") state
        """

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
                    crmrequestfactory.EXCLUDES: {
                        u"Levelkuldesek": u"Oklev\u00e9l - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_beginner_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(
            self):
        """
        test_company_beginner_dont_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable

        Given:
            - there is one active company beginner student
            - it's 2 days after last occasion
            - student is not eligible for certification
        When:
            - send_scheduled_emails() is called
        Then:
            - don't send certification
            - put student to Finished ("Elvegezte") state
        """

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
                    crmrequestfactory.EXCLUDES: {
                        u"Levelkuldesek": u"Oklev\u00e9l - kezd\u0151"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing(self):
        """
        test_company_advanced_date_is_more_than_delta_days_less_than_1st_occasion_do_nothing

        Given:
            - there is one active company advanced student
            - fist day is in more than 3 days
        When:
            - send_scheduled_emails() is called
        Then:
            - do nothing
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email(self):
        """
        test_company_advanced_date_is_before_1st_occasion_but_difference_is_less_than_delta_send_first_email

        Given:
            - there is one active company advanced student
            - fist day is in less than 3 days, but has not spent
        When:
            - send_scheduled_emails() is called
        Then:
            - first email is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_date_is_after_1st_occasion_send_first_email(self):
        """
        test_company_advanced_date_is_after_1st_occasion_send_first_email

        Given:
            - there is one active company advanced student
            - fist day is spent
        When:
            - send_scheduled_emails() is called
        Then:
            - first email is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_if_no_change_in_sent_mails_dont_send_update(self):
        """
        test_company_advanced_if_no_change_in_sent_mails_dont_send_update

        Given:
            - there is one active company advanced student
            - all scheduled mails have been already sent
        When:
            - send_scheduled_emails() is called
        Then:
            - don't update student data
        """

        self.crm_facade.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_1ST_MAIL_ALREADY_SENT_COMPANY_ADVANCED
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails(self):
        """
        test_company_advanced_if_no_mails_have_been_sent_but_more_occasions_passed_send_all_relevant_emails

        Given:
            - there is one active company advanced student
            - no mails have been sent
            - multiple occasions passed
        When:
            - send_scheduled_emails() is called
        Then:
            - all relevant mails are sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 2, 20, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"1. alkalom - halad\u00f3, 2. alkalom - halad\u00f3, 3. alkalom - halad\u00f3, 4. alkalom - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_if_second_break_is_coming_send_second_break_email(self):
        """
        test_company_advanced_if_second_break_is_coming_send_second_break_email

        Given:
            - there is one active company advanced student
            - it't not less than second break minus 2 days
        When:
            - send_scheduled_emails() is called
        Then:
            - second break mail is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 3, 17, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"2. sz\u00fcnet"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_if_third_break_is_coming_send_third_break_email(self):
        """
        test_company_advanced_if_third_break_is_coming_send_third_break_email

        Given:
            - there is one active company advanced student
            - it't not less than third break minus 2 days
        When:
            - send_scheduled_emails() is called
        Then:
            - third break mail is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 3, 27, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED_WITH_3_BREAKS
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"3. sz\u00fcnet"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_send_final_mail_1_day_after_last_occasion(self):
        """
        test_company_advanced_send_final_mail_1_day_after_last_occasion

        Given:
            - there is one active company advanced student
            - it't not less than final occasion minus 1 day
        When:
            - send_scheduled_emails() is called
        Then:
            - final mail is sent
        """

        self.crm_facade.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_COMPANY_ADVANCED
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                FAKE_STUDENT_ID_NUMBER,
                {

                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"\u00datraval\u00f3 - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_company_advanced_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable(
            self):
        """
        test_company_advanced_send_certification_and_set_state_to_finished_2_days_after_last_occasion_if_applicable

        Given:
            - there is one active company advanced student
            - it's not less than last occasion plus 2 days
            - student is eligible for certification
        When:
            - send_scheduled_emails() is called
        Then:
            - send advanced certification
            - put student to Finished ("Elvegezte") state
        """

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
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"Oklev\u00e9l - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)

    def test_advanced_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable(self):
        """
        test_advanced_send_certification_but_set_state_to_finished_2_days_after_last_occasion_if_not_applicable

        Given:
            - there is one active company advanced student
            - it's not less than last occasion plus 2 days
            - student is NOT eligible for certification
        When:
            - send_scheduled_emails() is called
        Then:
            - send advanced certification
            - put student to Finished ("Elvegezte") state
        """

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
                    crmrequestfactory.CONTAINS: {
                        u"Levelkuldesek": u"Oklev\u00e9l - halad\u00f3"
                    }
                }
            ),
            responses_general.XPUT_RESPONSE
        )
        send_scheduled_emails(self.crm_facade)


class TestOkForCertification(MiniCrmTestBase):

    def test_no_attendance_no_homework_returns_not_ok(self):
        """
        test_no_attendance_no_homework_returns_not_ok

        Given:
            - student hasn't filed any homework
        When:
            - ok_for_certification() with given student is called
        Then:
            - False is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)
        self.assertFalse(ok_for_certification(self.student_data))

    def test_full_attendance_full_homework_returns_ok(self):
        """
        test_full_attendance_full_homework_returns_ok

        Given:
            - student filed all homework
            - student attended all occasions
        When:
            - ok_for_certification() with given student is called
        Then:
            - True is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.FAKE_STUDENT_GOOD_FOR_CERTIFICATION)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_full_attendance_no_homework_returns_not_ok(self):
        """
        test_full_attendance_no_homework_returns_not_ok

        Given:
            - student attended all occasions
            - student hasn't filed any homework
        When:
            - ok_for_certification() with given student is called
        Then:
            - False is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_FULL_ATTENDANCE_NO_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_no_attendance_full_homework_returns_not_ok(self):
        """
        test_no_attendance_full_homework_returns_not_ok

        Given:
            - student filed all homework
            - student hasn't attended any courses
        When:
            - ok_for_certification() with given student is called
        Then:
            - False is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_NO_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_full_attendance_one_missing_homework_returns_not_ok(self):
        """
        test_full_attendance_one_missing_homework_returns_not_ok

        Given:
            - one homework is missing
            - student attended all courses
        When:
            - ok_for_certification() with given student is called
        Then:
            - False is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_FULL_ATTENDANCE_ALMOST_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_9_attendance_full_homework_returns_ok(self):
        """
        test_9_attendance_full_homework_returns_ok

        Given:
            - student attended 9 courses
            - student filed all homework
        When:
            - ok_for_certification() with given student is called
        Then:
            - True is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_9_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_8_attendance_full_homework_returns_ok(self):
        """
        test_8_attendance_full_homework_returns_ok

        Given:
            - student attended 8 courses
            - student filed all homework
        When:
            - ok_for_certification() with given student is called
        Then:
            - True is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_8_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_7_attendance_full_homework_returns_not_ok(self):
        """
        test_7_attendance_full_homework_returns_not_ok

        Given:
            - student attended 7 courses
            - student filed all homework
        When:
            - ok_for_certification() with given student is called
        Then:
            - False is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(FAKE_STUDENT_ID_NUMBER),
            responses_students.PARTIAL_STUDENT_7_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(FAKE_STUDENT_ID_NUMBER)

        self.assertFalse(ok_for_certification(self.student_data))
