from minicrmtestbase import MiniCrmTestBase


class TestGetDateDescription(MiniCrmTestBase):

    def set_course(self, api_response):
        self.command_handler.expect_command('ASDF', api_response)
        self.course_data = self.command_handler.get_json_array_for_command("ASDF")

    def test_date_description_returns_correct_string(self):
        self.set_course('project_2037_2019-1_Q_3_breaks')
        expected_string = u'   - 2019-01-28\n   - 2019-02-04\n   - 2019-02-11\n   - 2019-02-18\n   - 2019-02-25\n   - 2019-03-04\n   - 2019-03-11 - sz\xfcnet\n   - 2019-03-18\n   - 2019-03-21 - sz\xfcnet\n   - 2019-03-25\n   - 2019-03-31 - sz\xfcnet\n   - 2019-04-01\n   - 2019-04-08'
        self.assertEqual(self.crm_data._get_date_description(self.course_data), expected_string)