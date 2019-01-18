from tracing import stacktrace, trace


class CommandHandlerMock:

    def __init__(self):
        self.commands_got_in_parameters = []
        self.return_values = {}

    @stacktrace
    def get_json_array_for_command(self, command):
        print("COMMAND SENT TO ---MOCK--- API: {}".format(command))
        self.commands_got_in_parameters.append(command)
        return self.read_file(self.return_values[command])

    @stacktrace
    def set_return_value(self, command, filename):
        self.return_values[command] = filename

    @stacktrace
    def read_file(self, filename):
        with open(filename, 'r') as inputfile:
            contents = inputfile.read()
        return contents