import json
import shlex
import subprocess

from tracing import stacktrace, trace, pretty_print


class CommandHandlerMock:

    def __init__(self):
        self.commands_got_in_parameters = []

    @stacktrace
    def get_json_array_for_command(self, command):
        trace("COMMAND SENT TO ---MOCK--- API: {}".format(command))
        split_command = shlex.split(command)
        self.commands_got_in_parameters.append()
        trace("RAW RECEIVED: {}".format(output))
        formatted_output = json.loads(output)
        trace("ANSWER RECEIVED:")
        pretty_print(formatted_output)
        return formatted_output