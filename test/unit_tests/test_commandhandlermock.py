import unittest

import crmrequestfactory
from test.requesthandlermock.requesthandlermock import RequestHandlerMock


class TestCommandHandlerMock(unittest.TestCase):
    def setUp(self):
        self.command_handler = RequestHandlerMock("FakeApi", "FakeApi")

    def test_check_if_satisfied_does_not_raise_when_there_is_no_expectation(self):
        self.command_handler.check_is_satisfied()

    def test_check_if_satisfied_raises_when_there_is_expectation(self):
        self.command_handler.expect_request(
            crmrequestfactory.get_student(42),
            {u"fake": u"fake"}
        )
        with self.assertRaisesRegexp(AssertionError, "Not all expectations were fulfilled when test ended.") as cm:
            self.command_handler.check_is_satisfied()

    def test_match_expectation_raises_if_there_is_no_expectation(self):
        with self.assertRaisesRegexp(AssertionError, "No more commands were expected, but got") as cm:
            self.command_handler.match_expectation(crmrequestfactory.get_student(42))

    def test_match_expectation_raises_when_other_command_comes(self):
        self.command_handler.expect_request(
            crmrequestfactory.get_student(42),
            {u"fake": u"fake"}
        )
        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.command_handler.match_expectation(crmrequestfactory.get_student(137))

    def test_match_expectation_does_not_raise_when_correct_command_comes(self):
        self.command_handler.expect_request(
            crmrequestfactory.get_student(42),
            {u"fake": u"fake"}
        )
        self.command_handler.match_expectation(crmrequestfactory.get_student(42))

    def test_match_expectation_returns_expected_file_path(self):
        self.command_handler.expect_request(
            crmrequestfactory.get_student(42),
            {u"fake": u"fake"}
        )
        self.assertEqual(self.command_handler.match_expectation(
            crmrequestfactory.get_student(42)),
            {u"fake": u"fake"}
        )

    def test_expectations_are_matched_in_correct_order(self):
        self.command_handler.expect_request(crmrequestfactory.get_student(42), 'b')
        self.command_handler.expect_request(crmrequestfactory.get_student(43), 'd')
        self.command_handler.expect_request(crmrequestfactory.get_student(44), 'f')
        self.command_handler.match_expectation(crmrequestfactory.get_student(42))
        self.command_handler.match_expectation(crmrequestfactory.get_student(43))
        self.command_handler.match_expectation(crmrequestfactory.get_student(44))
        self.command_handler.check_is_satisfied()

    def test_error_is_raised_when_commands_are_matched_in_wrong_order(self):
        self.command_handler.expect_request(crmrequestfactory.get_student(42), 'b')
        self.command_handler.expect_request(crmrequestfactory.get_student(43), 'd')
        self.command_handler.expect_request(crmrequestfactory.get_student(44), 'f')
        self.command_handler.match_expectation(crmrequestfactory.get_student(42))
        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.command_handler.match_expectation(crmrequestfactory.get_student(44))
