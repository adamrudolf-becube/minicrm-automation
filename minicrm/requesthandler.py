import json

import requests

from apirequest import GET_METHOD, PUT_METHOD
from tracing import stacktrace, trace, pretty_print


class RequestHandler:

    def __init__(self, username, api_key):
        self._username = username
        self._api_key = api_key

    @stacktrace
    def fetch(self, request):
        """
        Sends the API request to the CRM system, and returns the formatted JSON array.
        """
        trace("COMMAND SENT TO API: {}, URL: {}".format(request.get_slogan(), request.get_url()))

        if request.get_method() == GET_METHOD:
            response = requests.get(request.get_url(), auth=(self._username, self._api_key))
        elif request.get_method() == PUT_METHOD:
            response = requests.put(
                request.get_url(),
                auth=(self._username, self._api_key),
                data=json.dumps(request.get_payload()))
        else:
            ValueError("Unsupported method type: [{}]".format(request.get_method()))

        trace("RAW RECEIVED: {}".format(response))
        formatted_output = response.json
        trace("ANSWER RECEIVED:")
        pretty_print(formatted_output)
        return formatted_output
