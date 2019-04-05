from test.unit_tests.minicrmtestbase import MiniCrmTestBase


class TestGetCourseByCourseCode(MiniCrmTestBase):

    def test_get_course_by_course_code_returns_correct_course(self):
        wanted_course_code = "2019-1-Q"

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?TanfolyamBetujele={}"'. \
                format(wanted_course_code),
            'course_list_for_course_code'
        )

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/1164"',
            'project_2037_2019-1_Q'
        )
        course_info = self.crm_data.get_course_by_course_code(wanted_course_code)
        self.assertEqual(course_info["TanfolyamBetujele"], wanted_course_code)
