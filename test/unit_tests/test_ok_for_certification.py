import crmrequestfactory
import test.requesthandlermock.responses.students as responses_students
from functionalities.sendscheduledmails import ok_for_certification
from minicrmtestbase import MiniCrmTestBase


class TestOkForCertification(MiniCrmTestBase):

    def test_no_attendance_no_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(42),
            responses_students.FAKE_STUDENT)
        self.student_data = self.crm_facade.get_student(42)
        self.assertFalse(ok_for_certification(self.student_data))

    def test_full_attendance_full_homework_returns_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(42),
            responses_students.FAKE_STUDENT_GOOD_FOR_CERTIFICATION)
        self.student_data = self.crm_facade.get_student(42)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_full_attendance_no_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(42),
            responses_students.PARTIAL_STUDENT_FULL_ATTENDANCE_NO_HOMEWORK)
        self.student_data = self.crm_facade.get_student(42)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_no_attendance_full_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(42),
            responses_students.PARTIAL_STUDENT_NO_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(42)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_full_attendance_one_missing_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(42),
            responses_students.PARTIAL_STUDENT_FULL_ATTENDANCE_ALMOST_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(42)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_9_attendance_full_homework_returns_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(42),
            responses_students.PARTIAL_STUDENT_9_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(42)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_8_attendance_full_homework_returns_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(42),
            responses_students.PARTIAL_STUDENT_8_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(42)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_7_attendance_full_homework_returns_not_ok(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_student(42),
            responses_students.PARTIAL_STUDENT_7_OF_10_ATTENDANCE_FULL_HOMEWORK)
        self.student_data = self.crm_facade.get_student(42)

        self.assertFalse(ok_for_certification(self.student_data))
