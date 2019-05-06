import unittest

from crmrequestfactory import _
from test.requesthandlermock.expectation import Expectation
from test.requesthandlermock.expextationqueue import ExpectationQueue
from tracing import stacktrace, trace


# TODO find out why some JSON is outputted even if tracing is turned off


class RequestHandlerMock(unittest.TestCase):

    def __init__(self, username, api_key):
        self.expectation_queue = ExpectationQueue()
        self._username = username
        self._api_key = api_key

    def check_is_satisfied(self):
        next_expectation = self.expectation_queue.get_next_element()
        if next_expectation is not None:
            self.assertIsNone(next_expectation,
                              "Not all expectations were fulfilled when test ended. First unsatisfied expectation: [{}]".
                              format(next_expectation.request.get_slogan()))

    @stacktrace
    def fetch(self, command):
        print("COMMAND SENT TO ---MOCK--- API: {}".format(command.get_slogan()))
        response = self.match_expectation(command)
        formatted_output = response["response"]
        trace("ANSWER RECEIVED:")
        return formatted_output

    @stacktrace
    def expect_request(self, expected_request, response):
        self.expectation_queue.push(Expectation(expected_request, response))

    @stacktrace
    def match_expectation(self, request):
        next_expectation = self.expectation_queue.pop()

        self.assertIsNotNone(
            next_expectation,
            "No more commands were expected, but got [{}]".format(request.get_slogan())
        )

        if not self._compare_requests(request, next_expectation.request):
            raise AssertionError("Unexpected command: [{}]. Expected: [{}]".
                                 format(request.get_slogan(), next_expectation.request.get_slogan()))

        return next_expectation.response

    @stacktrace
    def _compare_requests(self, got_request, expected_request):
        if expected_request.get_payload() == _:
            return got_request.get_url() == expected_request.get_url() and \
                   got_request.get_method() == expected_request.get_method()
        else:
            return got_request.get_url() == expected_request.get_url() and \
                   got_request.get_method() == expected_request.get_method() and \
                   got_request.get_slogan() == expected_request.get_slogan() and \
                   got_request.get_payload() == expected_request.get_payload()
