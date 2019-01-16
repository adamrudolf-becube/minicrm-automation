from tracing import stacktrace, trace


class CommandHandlerMock:

    def __init__(self):
        self.commands_got_in_parameters = []

    @stacktrace
    def get_json_array_for_command(self, command):
        trace("COMMAND SENT TO ---MOCK--- API: {}".format(command))
        self.commands_got_in_parameters.append()