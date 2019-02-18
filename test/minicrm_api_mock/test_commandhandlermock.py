import unittest
from commandhandlermock import CommandHandlerMock


class TestCommandHandlerMock(unittest.TestCase):
    def setUp(self):
        self.command_handler = CommandHandlerMock()

    def test_check_if_satisfied_does_not_raise_when_there_is_no_expectation(self):
        self.command_handler.check_is_satisfied()

    def test_check_if_satisfied_raises_when_there_is_expectation(self):
        self.command_handler.expect_command('A', 'b')
        with self.assertRaisesRegexp(AssertionError, "Not all expectations were fulfilled when test ended.") as cm:
            self.command_handler.check_is_satisfied()

    def test_match_expectation_raises_if_there_is_no_expectation(self):
        with self.assertRaisesRegexp(AssertionError, "No more commands were expected, but got") as cm:
            self.command_handler.match_expectation('C')

    def test_match_expectation_raises_when_other_command_comes(self):
        self.command_handler.expect_command('A', 'b')
        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.command_handler.match_expectation('C')

    def test_match_expectation_does_not_raise_when_correct_command_comes(self):
        self.command_handler.expect_command('A', 'b')
        self.command_handler.match_expectation('A')

    def test_match_expectation_returns_expected_file_path(self):
        self.command_handler.expect_command('A', 'b')
        self.assertEqual(self.command_handler.match_expectation('A'), 'b')

    def test_expectations_are_matched_in_correct_order(self):
        self.command_handler.expect_command('A', 'b')
        self.command_handler.expect_command('C', 'd')
        self.command_handler.expect_command('E', 'f')
        self.command_handler.match_expectation('A')
        self.command_handler.match_expectation('C')
        self.command_handler.match_expectation('E')
        self.command_handler.check_is_satisfied()

    def test_error_is_raised_when_commands_are_matched_in_wrong_order(self):
        self.command_handler.expect_command('A', 'b')
        self.command_handler.expect_command('C', 'd')
        self.command_handler.expect_command('E', 'f')
        self.command_handler.match_expectation('A')
        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.command_handler.match_expectation('E')

    def test_get_json_array_for_command_returns_and_parses_given_file(self):
        self.command_handler.expect_command('A', 'dummy_response_file.json')
        return_value = self.command_handler.get_json_array_for_command('A')
        self.assertEqual(return_value['dummyKey'], "dummyResponse")
