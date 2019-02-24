from tracing import stacktrace, trace
from test.minicrm_api_mock.expextationqueue import ExpectationQueue
from test.minicrm_api_mock.expectation import Expectation
import unittest
import json
import os

# TODO find out why some JSON is outputted even if tracing is turned off
# TODO put json outputs to one file to make it faster

API_RESPONSES = None

currentDirectory = os.path.dirname(os.path.realpath(__file__))

api_response_file_path = currentDirectory + "/api_outputs.json"

with open(api_response_file_path) as api_response_file:
    API_RESPONSES = json.load(api_response_file)


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
        response_identifier = self.match_expectation(command)
        formatted_output = API_RESPONSES[response_identifier]["response"]
        #trace("ANSWER RECEIVED:")
        #pretty_print(formatted_output)
        return formatted_output

    @stacktrace
    def expect_command(self, command_pattern, response_identifier, repeatedly = False):
        self.expectation_queue.push(Expectation(command_pattern, response_identifier, repeatedly))

    @stacktrace
    def match_expectation(self, command):
        next_expectation = self.expectation_queue.pop()

        self.assertIsNotNone(next_expectation, "No more commands were expected, but got [{}]".format(command))

        if not next_expectation.command_pattern == command:
            raise AssertionError("Unexpected command: [{}]. Expected: [{}]".
                                 format(command, next_expectation.command_pattern))

        return next_expectation.response_identifier

    @stacktrace
    def read_file(self, filename):
        trace("Trying to read {}".format(filename))
        with open(filename, 'r') as inputfile:
            contents = inputfile.read()
        return contents