from minicrmtestbase import MiniCrmTestBase


class TestOkForCertification(MiniCrmTestBase):

    def test_no_attendance_no_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'project_2601_fake_student')
        self.student_data = self.crm_data.get_project(42)
        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))

    def test_full_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'project_2601_fake_student_good_for_certification')
        self.student_data = self.crm_data.get_project(42)

        self.assertTrue(self.crm_data.ok_for_certification(self.student_data))

    def test_full_attendance_no_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_full_attendance_no_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))

    def test_no_attendance_full_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_no_attendance_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))

    def test_full_attendance_one_missing_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_full_attendance_almost_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))

    def test_9_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_9_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertTrue(self.crm_data.ok_for_certification(self.student_data))

    def test_8_attendance_full_homework_returns_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_8_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertTrue(self.crm_data.ok_for_certification(self.student_data))

    def test_7_attendance_full_homework_returns_not_ok(self):

        self.command_handler.expect_command(
            'curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Project/42"',
            'partial_student_7_of_10_attendance_full_homework')
        self.student_data = self.crm_data.get_project(42)

        self.assertFalse(self.crm_data.ok_for_certification(self.student_data))