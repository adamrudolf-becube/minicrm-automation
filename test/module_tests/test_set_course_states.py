from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import crmrequestfactory
import datetime
from functionalities.setcoursestates import set_course_states
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.courselists as apioutputs_courselists
import test.minicrm_api_mock.apioutputs.courses as apioutputs_courses
import test.minicrm_api_mock.apioutputs.studentlists as apioutputs_studentlists


class TestRegisterNewApplicants(MiniCrmTestBase):

    def test_application_is_open_and_first_day_hasnt_spent_do_nothing(self):
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q)
        set_course_states(self.crm_data)

    def test_application_is_open_first_day_spent_but_last_didnt_put_to_in_progress(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q)
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(2037, {u"StatusId": u"2758"}),
            apioutputs_general.XPUT_RESPONSE)
        set_course_states(self.crm_data)

    def test_in_progress_first_day_is_spent_but_last_didnt_set_state_to_in_rpogress(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_IN_PROGRESS)
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(2037, {u"StatusId": u"2758"}),
            apioutputs_general.XPUT_RESPONSE)
        set_course_states(self.crm_data)

    def test_recently_finished_first_day_spent_but_last_didnt_put_to_in_progress(self):
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 7, 30))
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_RECENTLY_FINISHED)
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(2037, {u"StatusId": u"2758"}),
            apioutputs_general.XPUT_RESPONSE)
        set_course_states(self.crm_data)

    def test_in_progress_last_day_has_spent_but_not_35_more_days_put_to_recently_finished(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_IN_PROGRESS)
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(2037, {u"StatusId": u"2797"}),
            apioutputs_general.XPUT_RESPONSE)
        set_course_states(self.crm_data)

    def test_recently_finished_last_day_has_spent_but_not_35_more_put_to_recently_finished(self):
        self.crm_data.set_today(datetime.datetime(2019, 4, 9, 7, 30))
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_RECENTLY_FINISHED)
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(2037, {u"StatusId": u"2797"}),
            apioutputs_general.XPUT_RESPONSE)
        set_course_states(self.crm_data)

    def test_recently_finished_and_35_days_passed_put_to_closed(self):
        self.crm_data.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_RECENTLY_FINISHED)
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(2037, {u"StatusId": u"2754"}),
            apioutputs_general.XPUT_RESPONSE)
        set_course_states(self.crm_data)

    def test_first_day_is_missing_no_error_is_raised_state_is_not_changed(self):
        self.crm_data.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_FIRST_DATE_MISSING)
        set_course_states(self.crm_data)

    def test_last_day_is_missing_no_error_is_raised_put_to_in_progress(self):
        self.crm_data.set_today(datetime.datetime(2019, 5, 15, 7, 30))
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2753),
            apioutputs_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2758),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_project_list_for_status(2797),
            apioutputs_general.EMPTY_LIST)
        self.command_handler.expect_command(
            crmrequestfactory.get_course(2037),
            apioutputs_courses.COURSE_2019_1_Q_LAST_DATE_MISSING)
        self.command_handler.expect_command(
            crmrequestfactory.set_project_data(2037, {u"StatusId": u"2758"}),
            apioutputs_general.XPUT_RESPONSE)
        set_course_states(self.crm_data)

    # TODO: [PLANNED] If course is started, put waiting list students to SUBSCRIBED (erdeklodo) state and send mail
