"""
Contains a class to encapsulate an API request.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

GET_METHOD = "GET"
"""Defines a constant to denote GET type REST API request."""

PUT_METHOD = "PUT"
"""Defines a constant to denote PUT type REST API request."""


class ApiRequest:
    """
    Encapsulates a REST API request.

    This can be used to send to the request handlers, which can send the request to the REST API, but can be also
    used in the tests to set expectations.
    """

    def __init__(self, url, method, slogan, payload={}):
        """
        Initializes a new ApiRequest instance. Throws ValueError.

        :param url: this is the URL of the request, or the API endpoint in other words

        :param method: request method type. Currently only GET and PUT are supported. If other string is given, a
        ValueError is raised.

        :param slogan: human readable description of the request. Intended to be used in traces and error messages.
        Prefer to include data, for example student ID or payload to make it more understandable, and to help to compare
        requests.

        :param payload: data of the request. Used in PUT requests. Defaults to empty dictionary.
        """

        self._url = url
        if method != GET_METHOD and method != PUT_METHOD:
            raise ValueError("Unsupported method type: {}".format(method))
        else:
            self._method = method
        self._slogan = slogan
        self._payload = payload

    def get_url(self):
        """
        Gets the URL of the request

        :return: URL of the request as a string
        """

        return self._url

    def get_method(self):
        """
        Gets the method type of the request

        :return: the method type as s string. It supports "GET" and "PUT" at the time.
        """

        return self._method

    def get_slogan(self):
        """
        Gets the human readable slogan of the request.

        :return: the human readable slogan of the request as string.
        """

        return self._slogan

    def get_payload(self):
        """
        Gets the payload of the request.

        :return: the payload of the request.
        """

        return self._payload
