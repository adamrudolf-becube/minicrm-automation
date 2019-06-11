"""
Contains a class to maintain the connection with the remote server.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import json

import requests

from apirequest import GET_METHOD, PUT_METHOD
from tracing import stacktrace, trace, pretty_print


class RequestHandler:

    def __init__(self, username, api_key):
        """
        This class encapsulates a connection towards the MiniCRM server through it's REST API.

        It is responsible to send the requests and receive and parse the answers.

        :param username: username (system ID) for the API
        :type username: str

        :param api_key: API key
        :type api_key: str
        """

        self._username = username
        self._api_key = api_key

    @stacktrace
    def fetch(self, request):
        """
        Sends the API request to the CRM system, and returns the formatted JSON array in the for of a Python dict.

        :param request: the encapsulated API request
        :type request: ApiRequest

        :return: the JSON answer as Python dictionary.
        :rtype: dict
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
