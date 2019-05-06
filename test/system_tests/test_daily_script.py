from minicrm import crmrequestfactory
import dailyscript
import test.requesthandlermock.responses.courselists as responses_courselists
import test.requesthandlermock.responses.courses as responses_courses
import test.requesthandlermock.responses.general as responses_general
import test.requesthandlermock.responses.studentlists as responses_studentlists
import test.requesthandlermock.responses.students as responses_students
from test.unit_tests.minicrmtestbase import MiniCrmTestBase


class TestDailyScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):
        self.expect_send_scheduled_mails()
        self.expect_set_course_states()

        dailyscript.run(self.crm_facade)

    def expect_send_scheduled_mails(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2749),
            responses_studentlists.ACTIVE_ONE_STUDENT
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2784),
            responses_general.EMPTY_LIST
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2941),
            responses_students.FAKE_STUDENT
        )

    def expect_set_course_states(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2758),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2797),
            responses_general.EMPTY_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_course(2037),
            responses_courses.COURSE_2019_1_Q)
