from tracing import stacktrace, trace, pretty_print
import json

class CommandHandlerMock:

    def __init__(self):
        self.commands_got_in_parameters = []
        self.return_values = {}

    @stacktrace
    def get_json_array_for_command(self, command):
        print("COMMAND SENT TO ---MOCK--- API: {}".format(command))
        self.commands_got_in_parameters.append(command)
        output = self.read_file(self.return_values[command])
        trace("RAW RECEIVED: {}".format(output))
        formatted_output = json.loads(output)
        trace("ANSWER RECEIVED:")
        pretty_print(formatted_output)
        return formatted_output

    @stacktrace
    def set_return_value(self, command, filename):
        self.return_values[command] = filename

    @stacktrace
    def read_file(self, filename):
        with open(filename, 'r') as inputfile:
            contents = inputfile.read()
        return contents