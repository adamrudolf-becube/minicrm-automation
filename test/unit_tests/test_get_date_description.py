import crmrequestfactory
import test.minicrm_api_mock.apioutputs.courses as apioutputs_courses
from minicrmtestbase import MiniCrmTestBase


class TestGetDateDescription(MiniCrmTestBase):

    def set_course(self, api_response):
        self.command_handler.expect_command(
            crmrequestfactory.get_student(42),
            api_response
        )
        self.course_data = self.command_handler.fetch(
            crmrequestfactory.get_student(42)
        )

    def test_date_description_returns_correct_string(self):
        self.set_course(apioutputs_courses.COURSE_2019_1_Q_3_BREAKS)
        expected_string = u'   - 2019-01-28\n   - 2019-02-04\n   - 2019-02-11\n   - 2019-02-18\n   - 2019-02-25\n   - 2019-03-04\n   - 2019-03-11 - sz\xfcnet\n   - 2019-03-18\n   - 2019-03-21 - sz\xfcnet\n   - 2019-03-25\n   - 2019-03-31 - sz\xfcnet\n   - 2019-04-01\n   - 2019-04-08'
        self.assertEqual(self.crm_data._get_date_description(self.course_data), expected_string)
