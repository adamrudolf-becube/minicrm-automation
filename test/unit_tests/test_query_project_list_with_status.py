from minicrm import crmrequestfactory
import test.requesthandlermock.responses.studentlists as responses_studentlists
from minicrmtestbase import MiniCrmTestBase


class TestQueryProjectListWithStatus(MiniCrmTestBase):
    def test_query_project_list_with_status_returns_all_projects_even_if_thereare_more_pages(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2749),
            responses_studentlists.STUDENT_LIST_105_ACTIVE_PAGE_0
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status_page1(2749),
            responses_studentlists.STUDENT_LIST_105_ACTIVE_PAGE_1
        )
        results = self.crm_facade.get_student_list_with_status("Kurzus folyamatban")
        self.assertEqual(len(results), 105)
