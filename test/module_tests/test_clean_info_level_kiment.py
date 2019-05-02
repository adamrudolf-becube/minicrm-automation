from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import datetime
from functionalities.clean_info_sent import clean_info_level_kiment
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.studentlists as apioutputs_studentlists
import test.minicrm_api_mock.apioutputs.students as apioutputs_students


class TestInfoSent(MiniCrmTestBase):
    # TODO find a nice structure fr responses which are easy to read, like ["Schemas"]["Course (21)"], or ["Course lists"]["Open courses (2753)"]["One course open"] or similar
    def setUp(self):
        super(TestInfoSent, self).setUp()
        self.crm_data.set_today(datetime.datetime(2019, 1, 21, 7, 30))

    def test_student_did_not_finalize_deadline_has_not_spent_but_within_24_hours_send_reminder(self):

        self.crm_data.set_today(datetime.datetime(2019, 1, 22, 12, 0))

        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2781),
            apioutputs_studentlists.ONE_STUDENT_IN_INFO_SENT_STATE)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2601),
            apioutputs_students.FAKE_STUDENT)

        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2601, {"Levelkuldesek":u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni"}),
            apioutputs_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_data)

    def test_student_did_not_finalize_deadline_has_spent_but_not_more_than_24_hours_ago_send_reminder_raise_task(self):

        self.crm_data.set_today(datetime.datetime(2019, 1, 23, 12, 0))

        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2781),
            apioutputs_studentlists.ONE_STUDENT_IN_INFO_SENT_STATE)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2601),
            apioutputs_students.FAKE_STUDENT)

        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {u"Levelkuldesek":u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni, Ma kell jelentkezni"}
            ),
            apioutputs_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_data)

    def test_student_did_not_finalize_deadline_has_spent_more_than_24_hours_ago_delete(self):

        self.crm_data.set_today(datetime.datetime(2019, 1, 24, 12, 0))

        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2781),
            apioutputs_studentlists.ONE_STUDENT_IN_INFO_SENT_STATE)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2601),
            apioutputs_students.FAKE_STUDENT)

        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(2601, {u"StatusId":u"2782",u"Levelkuldesek":u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni, Ma kell jelentkezni, Toroltunk"}),
            apioutputs_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_data)

    def test_student_did_not_finalize_and_deadline_is_more_than_1_day_away_do_nothing(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2781),
            apioutputs_studentlists.ONE_STUDENT_IN_INFO_SENT_STATE
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2601),
            apioutputs_students.FAKE_STUDENT
        )
        self.set_participant_number_expectations()

        clean_info_level_kiment(self.crm_data)