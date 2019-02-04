from tracing import stacktrace, trace, pretty_print
from test.expextationqueue import ExpectationQueue
from test.expectation import Expectation
import json


class CommandHandlerMock:

    def __init__(self):
        self.expectation_queue = ExpectationQueue()

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
        next_expectation = self.expectation_queue.get_next_element()

        if next_expectation.command_pattern == command:
            trace("Command matches next expectation")
            if not next_expectation.repeatedly:
                trace("Command is not expected repeatedly, removing expectation from the list")
                return self.expectation_queue.pop().response_file
        else:
            trace("Command does not match next expectation")
            if next_expectation.repeatedly:
                trace("Command was expected repeatedly. Removing expectation from the list and checking next expectation")
                self.expectation_queue.pop()
                self.match_expectation(command)
            else:
                trace("Command was not expected repeatedly, raising error")
                # TODO make unittest fail
                raise AssertionError("Unexpected command: {}".format(command))

    @stacktrace
    def read_file(self, filename):
        trace("Trying to read {}".format(filename))
        with open(filename, 'r') as inputfile:
            contents = inputfile.read()
        return contents