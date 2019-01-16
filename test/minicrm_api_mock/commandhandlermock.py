import json
import shlex
import subprocess

from tracing import stacktrace, trace, pretty_print


class CommandHandlerMock:

    @stacktrace
    def get_json_array_for_command(command):
        trace("COMMAND SENT TO ---MOCK--- API: {}".format(command))
        split_command = shlex.split(command)
        process = subprocess.Popen(split_command, stdout=subprocess.PIPE)
        output = process.stdout.readline()
        trace("RAW RECEIVED: {}".format(output))
        formatted_output = json.loads(output)
        trace("ANSWER RECEIVED:")
        pretty_print(formatted_output)
        return formatted_output