from minicrmtestbase import MiniCrmTestBase


class TestQueryProjectListWithStatus(MiniCrmTestBase):
    def test_query_project_list_with_status_returns_all_projects_even_if_thereare_more_pages(self):
        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2749"',
            'student_list_105_active_page0'
        )

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project?StatusId=2749&Page=1"',
            'student_list_105_active_page1'
        )
        results = self.crm_data.get_student_list_with_status("Kurzus folyamatban")
        self.assertEqual(len(results), 105)