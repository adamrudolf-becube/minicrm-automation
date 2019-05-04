from minicrmtestbase import MiniCrmTestBase
import minicrmcommandfactory
import test.minicrm_api_mock.apioutputs.studentlists as apioutputs_studentlists


class TestQueryProjectListWithStatus(MiniCrmTestBase):
    def test_query_project_list_with_status_returns_all_projects_even_if_thereare_more_pages(self):
        self.command_handler.expect_command(
            minicrmcommandfactory.get_project_list_for_status(2749),
            apioutputs_studentlists.STUDENT_LIST_105_ACTIVE_PAGE_0
        )

        self.command_handler.expect_command(
            minicrmcommandfactory.get_project_list_for_status_page1(2749),
            apioutputs_studentlists.STUDENT_LIST_105_ACTIVE_PAGE_1
        )
        results = self.crm_data.get_student_list_with_status("Kurzus folyamatban")
        self.assertEqual(len(results), 105)