from minicrmtestbase import MiniCrmTestBase
import datetime


class TestGetApplicationDeadline(MiniCrmTestBase):

    def set_course(self, api_response):
        self.command_handler.expect_command('ASDF', api_response)
        self.course_data = self.command_handler.get_json_array_for_command("ASDF")

    def test_if_course_starts_in_not_less_than_7_days_away_and_more_than_places_30_percent_if_free_deadline_is_5_days(self):
        self.set_course('project_2037_2019-1_Q')
        self.crm_data.set_today(datetime.datetime(2019, 1, 10, 9, 8))
        self.assertEqual("2019-01-15 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_course_starts_in_less_than_7_days_away_and_more_than_places_30_percent_if_free_deadline_is_3_days(self):
        self.set_course('project_2037_2019-1_Q')
        self.crm_data.set_today(datetime.datetime(2019, 1, 23, 9, 8))
        self.assertEqual("2019-01-26 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_course_starts_in_not_less_than_7_days_away_and_less_than_places_30_percent_if_free_deadline_is_3_days(self):
        self.set_course('project_2037_2019-1_Q_one_place_free')
        self.crm_data.set_today(datetime.datetime(2019, 1, 10, 9, 8))
        self.assertEqual("2019-01-13 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_course_starts_in_less_than_3_days_and_there_is_no_more_than_3_places_deadline_is_1_day(self):
        self.set_course('project_2037_2019-1_Q_one_place_free')
        self.crm_data.set_today(datetime.datetime(2019, 1, 26, 9, 8))
        self.assertEqual("2019-01-27 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_course_start_is_earlier_than_the_calculated_deadline_deadline_is_course_start_minus_one_day(self):
        self.set_course('project_2037_2019-1_Q')
        self.crm_data.set_today(datetime.datetime(2019, 1, 26, 9, 8))
        self.assertEqual("2019-01-27 23:59:59", self.crm_data.get_application_deadline(self.course_data))

    def test_if_deadline_is_earlier_than_today_deadline_is_today_plus_one_day(self):
        self.set_course('project_2037_2019-1_Q')
        self.crm_data.set_today(datetime.datetime(2019, 1, 29, 9, 8))
        self.assertEqual("2019-01-30 09:08:00", self.crm_data.get_application_deadline(self.course_data))

    def test_if_all_spots_is_zero_function_does_not_raise(self):
        self.set_course('course_max_spots_is_zero')
        self.crm_data.get_application_deadline(self.course_data)
