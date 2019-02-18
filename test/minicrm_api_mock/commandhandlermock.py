from tracing import stacktrace, trace, pretty_print
from test.expextationqueue import ExpectationQueue
from test.expectation import Expectation
import unittest
import json


class CommandHandlerMock(unittest.TestCase):

    def __init__(self):
        self.expectation_queue = ExpectationQueue()

    def check_is_satisfied(self):
        next_expectation = self.expectation_queue.get_next_element()
        if next_expectation is not None:
            self.assertIsNone(next_expectation,
                              "Not all expectations were fulfilled when test ended. First unsatisfied expectation: [{}]".
                              format(next_expectation.command_pattern))

    @stacktrace
    def get_json_array_for_command(self, command):
        print("COMMAND SENT TO ---MOCK--- API: {}".format(command))
        response_location = self.match_expectation(command)
        output = self.read_file(response_location)
        formatted_output = json.loads(output)
        #trace("ANSWER RECEIVED:")
        #pretty_print(formatted_output)
        return formatted_output

    @stacktrace
    def expect_command(self, command_pattern, response_file, repeatedly = False):
        self.expectation_queue.push(Expectation(command_pattern, response_file, repeatedly))

    @stacktrace
    def match_expectation(self, command):
        next_expectation = self.expectation_queue.pop()

        self.assertIsNotNone(next_expectation, "No more commands were expected, but got [{}]".format(command))

        if not next_expectation.command_pattern == command:
            raise AssertionError("Unexpected command: [{}]. Expected: [{}]".
                                 format(command, next_expectation.command_pattern))

        return next_expectation.response_file

    @stacktrace
    def read_file(self, filename):
        trace("Trying to read {}".format(filename))
        with open(filename, 'r') as inputfile:
            contents = inputfile.read()
        return contents