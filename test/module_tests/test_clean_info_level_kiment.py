import datetime

import test.requesthandlermock.responses.general as responses_general
import test.requesthandlermock.responses.studentlists as responses_studentlists
import test.requesthandlermock.responses.students as responses_students
from functionalities.cleaninfosent import clean_info_level_kiment
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase


class TestInfoSent(MiniCrmTestBase):
    # TODO find a nice structure fr responses which are easy to read, like ["Schemas"]["Course (21)"], or ["Course lists"]["Open courses (2753)"]["One course open"] or similar
    def setUp(self):
        super(TestInfoSent, self).setUp()
        self.crm_facade.set_today(datetime.datetime(2019, 1, 21, 7, 30))

    def test_student_did_not_finalize_deadline_has_not_spent_but_within_24_hours_send_reminder(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 22, 12, 0))

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2781),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2941),
            responses_students.FAKE_STUDENT)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2941,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni"}
            ),
            responses_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_facade)

    def test_student_did_not_finalize_deadline_has_spent_but_not_more_than_24_hours_ago_send_reminder_raise_task(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 23, 12, 0))

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2781),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2941),
            responses_students.FAKE_STUDENT)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2941,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni, Ma kell jelentkezni"}
            ),
            responses_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_facade)

    def test_student_did_not_finalize_deadline_has_spent_more_than_24_hours_ago_delete(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 24, 12, 0))

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2781),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2941),
            responses_students.FAKE_STUDENT)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2941,
                {
                    u"StatusId": u"2782",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni, Ma kell jelentkezni, Toroltunk"
                }
            ),
            responses_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_facade)

    def test_student_did_not_finalize_and_deadline_is_more_than_1_day_away_do_nothing(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2781),
            responses_studentlists.INFO_SENT_ONE_STUDENT
        )
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2941),
            responses_students.FAKE_STUDENT
        )
        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_facade)
