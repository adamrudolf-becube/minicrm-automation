import json
from apirequest import GET_METHOD, PUT_METHOD
import requests

from tracing import stacktrace, trace, pretty_print


class CommandHandler:

    def __init__(self, username, api_key):
        self._username = username
        self._api_key = api_key

    @stacktrace
    def get_json_array_for_command(self, command):
        """
        Sends the API command to the CRM system, and returns the formatted JSON array.
        """
        trace("COMMAND SENT TO API: {}".format(command.get_slogan()))

        if command.get_method == GET_METHOD:
            response = requests.get(command.get_url(), auth=(self._username, self._api_key))
        elif command.get_method == PUT_METHOD:
            response = requests.put(
                command.get_url(),
                auth=(self._username, self._api_key),
                data=json.dumps(command.get_payload()))

        trace("RAW RECEIVED: {}".format(response))
        formatted_output = response.json
        trace("ANSWER RECEIVED:")
        pretty_print(formatted_output)
        return formatted_output