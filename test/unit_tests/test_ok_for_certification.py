from minicrmtestbase import MiniCrmTestBase
from functionalities.sendscheduledmails import ok_for_certification


class TestOkForCertification(MiniCrmTestBase):

    def test_no_attendance_no_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(42),
            'project_2601_fake_student')
        self.student_data = self.crm_data.get_student(42)
        self.assertFalse(ok_for_certification(self.student_data))

    def test_full_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(42),
            'project_2601_fake_student_good_for_certification')
        self.student_data = self.crm_data.get_student(42)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_full_attendance_no_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(42),
            'partial_student_full_attendance_no_homework')
        self.student_data = self.crm_data.get_student(42)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_no_attendance_full_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(42),
            'partial_student_no_attendance_full_homework')
        self.student_data = self.crm_data.get_student(42)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_full_attendance_one_missing_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(42),
            'partial_student_full_attendance_almost_full_homework')
        self.student_data = self.crm_data.get_student(42)

        self.assertFalse(ok_for_certification(self.student_data))

    def test_9_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(42),
            'partial_student_9_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_student(42)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_8_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(42),
            'partial_student_8_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_student(42)

        self.assertTrue(ok_for_certification(self.student_data))

    def test_7_attendance_full_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            self.crm_command_factory.get_student(42),
            'partial_student_7_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_student(42)

        self.assertFalse(ok_for_certification(self.student_data))
