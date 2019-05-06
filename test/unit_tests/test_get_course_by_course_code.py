import crmrequestfactory

from test.unit_tests.minicrmtestbase import MiniCrmTestBase
import test.minicrm_api_mock.apioutputs.courselists as apioutputs_courselists
import test.minicrm_api_mock.apioutputs.courses as apioutputs_courses


class TestGetCourseByCourseCode(MiniCrmTestBase):

    def test_get_course_by_course_code_returns_correct_course(self):
        wanted_course_code = "2019-1-Q"

        self.command_handler.expect_command(
            crmrequestfactory.get_course_list_by_course_code(wanted_course_code),
            apioutputs_courselists.COURSE_LIST_FOR_COURSE_CODE
        )

        self.command_handler.expect_command(
            crmrequestfactory.get_course(1164),
            apioutputs_courses.COURSE_2019_1_Q
        )
        course_info = self.crm_data.get_course_by_course_code(wanted_course_code)
        self.assertEqual(course_info["TanfolyamBetujele"], wanted_course_code)
