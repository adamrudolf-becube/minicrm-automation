from minicrmtestbase import MiniCrmTestBase
import test.minicrm_api_mock.api_outputs as apioutputs


class TestQueryProjectListWithStatus(MiniCrmTestBase):
    def test_query_project_list_with_status_returns_all_projects_even_if_thereare_more_pages(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2749),
            apioutputs.API_OUTPUTS['student_list_105_active_page0']
        )

        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status_page1(2749),
            apioutputs.API_OUTPUTS['student_list_105_active_page1']
        )
        results = self.crm_data.get_student_list_with_status("Kurzus folyamatban")
        self.assertEqual(len(results), 105)