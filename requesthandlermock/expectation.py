__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"


class Expectation:
    def __init__(self, expected_request, response):
        """
        Encapsulates an expectation in the test. The expectation contains the expected ApiRequest and a response to that
        request as a Python dictionary.

        :param expected_request: API request expected by the testcase
        :type: ApiRequest

        :param response: if the expected request is sent to a CommandHandlerMock instance, this is returned as a
                         response.
        :type response: dict
        """

        self.request = expected_request
        self.response = response
