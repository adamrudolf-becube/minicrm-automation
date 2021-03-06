__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import unittest

from expectation import Expectation
from expectationqueue import ExpectationQueue
from minicrm.commonfunctions import commaseparated_list_is_subset_of,\
    all_element_of_commaseparated_list_is_expluded_from
from minicrm.crmrequestfactory import _, CONTAINS, EXCLUDES
from minicrm.tracing import stacktrace, trace, pretty_print


class RequestHandlerMock(unittest.TestCase):

    def __init__(self, username, api_key):
        """
        This class is the test substitute of the minicrm.RequestHandler class.

        From the usage point of view, it works exactly the same way as the ReqestHandler, but it doesn't maintain real
        connection to any server, instead it returns predefined responses to API requests.

        The logic of this class is inspired by Google Test's Google Mock framework
        (https://github.com/google/googletest). That is, you can set a series
        of expectations before the action itself. In this case you have to "tell the exoected story" with a series of
        expect_request calls, and then call the function under test. Any deviation from the previously defined series of
        requests will end up in an exception.

        Note: the class is not a real mock in the Python sense, it is actually a unittest.TestCase. It is mock according
        to it's intention. (I.e. it is used instead of a real class, and you can set expectations against it's usage and
        it keeps track of them.)

        :param username: username (system ID) for the API
        :type username: str

        :param api_key: API key
        :type api_key: str
        """

        self.expectation_queue = ExpectationQueue()
        self._username = username
        self._api_key = api_key

    def check_is_satisfied(self):
        """
        Raises an error if there is an unsatisfied expectation.

        This class can detect any incoming unexpected API requests, but it doesn't know whether the test ended or not.
        It means that if the test ends too early, unsatisfied expectations remain in the queue without causing visible
        problems.  Call this function at the end of test.

        It is practical to call this function in the TearDown of test suites to make sure every test ends without
        unsatisfied expectations.

        :raises: AssertionError with the error message beginning with "Not all expectations were fulfilled when test
                 ended."

        :return: None
        """

        next_expectation = self.expectation_queue.get_next_element()
        if next_expectation is not None:
            self.assertIsNone(
                next_expectation,
                "Not all expectations were fulfilled when test ended. First unsatisfied expectation: [{}]".
                    format(next_expectation.request.get_slogan())
            )

    @stacktrace
    def fetch(self, request):
        """
        Gets an API request, and returns the formatted JSON array in the for of a Python dict.

        The returned dictionary is what has been set by the expect_request if the request matches the next expectation.

        Also pops the next element from the expectation queue.

        Normally URL, request method type, payload and slogan has to be equal when matching expectations, but if
        payload is equal to minicrm.crmrequestfactory._, payload and slogan is not contributing and only URL and
        method type has to be equal to be considered matching.

        Note: this function only adds printing to the match_expectation.

        :raises: AssertionError if expectation queue is empty or if the next element doesn't match the given request.

        :param request: the encapsulated API request
        :type request: ApiRequest

        :return: the JSON answer as Python dictionary, if the request matches the next expectation.
        :rtype: dict
        """

        print("COMMAND SENT TO ---MOCK--- API: {}".format(request.get_slogan()))
        formatted_output = self.match_expectation(request)
        trace("ANSWER RECEIVED:")
        pretty_print(formatted_output)
        return formatted_output

    @stacktrace
    def expect_request(self, expected_request, response):
        """
        Appends the given request to the end of the expectation queue, together with the predefined response.

        With this function you can "tell the story" of what you expect to happen before calling the action of the test.
        Calling this function multiple times after each other builds up an expected series of API requests and also
        defines what the testing machinery has to return as a response for each.

        As opposed to most of the testing frameworks, you have to define the expectations before doing the action. This
        logic is inspired by Google Test's Google Mock framework
        (https://github.com/google/googletest/blob/master/googlemock/docs/ForDummies.md). When the action happens,
        RequestHandlerMock will pop the expectation queue for every API request and match the got request against the
        next expectation. If any deviation happens, AssertionError will be raised.

        You can use special values in the payload of expected request to let more freedom than direct equality. For
        those, see documentation of method "match_expectation" of this class.

        Expectations can be combined with post-action assertions.

        Example usage:

        .. code-block:: python

                wanted_course_code = "2019-1-Q"
                wanted_course_id = 1164

                self.request_handler.expect_request(
                    crmrequestfactory.get_course_list_by_course_code(wanted_course_code),
                    responses_courselists.COURSE_LIST_FOR_COURSE_CODE
                )

                self.request_handler.expect_request(
                    crmrequestfactory.get_course(wanted_course_id),
                    responses_courses.COURSE_2019_1_Q
                )
                course_info = self.crm_facade.get_course_by_course_code(wanted_course_code)
                self.assertEqual(course_info["TanfolyamBetujele"], wanted_course_code)

        Normally URL, request method type and payload have to be equal when matching expectations, but if
        payload is equal to minicrm.crmrequestfactory._, payload is not contributing and only URL and
        method type has to be equal to be considered matching. Slogan doesn't take part in comparison, because
        URL and payload defines the expectation, and different slogans can be generated for the same payloads, since
        order in dictionary is not defined. This could cause false negatives.

        Also, if a field of the payload is a commaseparated list, and you would like to test whether a set of elements
        are included or excluded, you can wrap that field into minicrm.crmrequestfactory.CONTAIN or
        minicrm.crmrequestfactory.EXCLUDE fields. These can be combined.

        In this below example test will pass if 'u"exact_match": u"exact_element"' is exaclty part of the real request,
        'alpha' and 'beta' are included, and 'epsilon', 'phi', and 'khi' are not indclided in field
        "commaseparated_list", which is a commaseparated list.

        .. code-block:: python

            self.request_handler.expect_request(
                crmrequestfactory.set_project_data(
                    ARBITRARY_STUDENT_ID,
                    {
                        u"exact_match": u"exact_element",
                        crmrequestfactory.CONTAINS: {
                            u"commaseparated_list": u"alpha, beta"
                        },
                        crmrequestfactory.EXCLUDES: {
                            u"commaseparated_list": u"epsilon, phi, khi"
                        }
                    }
                ),
                {u"fake": u"fake"}
            )

        :param expected_request: an ApiRequest instance we expect in this place of the sequence.
        :type expected_request: ApiRequest

        :param response: A python dictionary mimicking the JSON array the system would send as a response to the
                         API request given in expected_request
        :type response: dict

        :return: None
        """

        self.expectation_queue.push(Expectation(expected_request, response))

    @stacktrace
    def match_expectation(self, request):
        """
        Gets an API request, and returns the formatted JSON array in the for of a Python dict.

        The returned dictionary is what has been set by the expect_request if the request matches the next expectation.

        Also pops the next element from the expectation queue.

        Note: this function is the same as fetch without printing.

        :raises: AssertionError if expectation queue is empty or if the next element doesn't match the given request.

        :param request: the encapsulated API request
        :type request: ApiRequest

        :return: the JSON answer as Python dictionary, if the request matches the next expectation.
        :rtype: dict
        """

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

        url_is_same = got_request.get_url() == expected_request.get_url()
        method_is_same = got_request.get_method() == expected_request.get_method()

        if expected_request.get_payload() == _:
            payload_is_accepted = True

        else:
            payload_is_accepted = True

            for key in expected_request.get_payload():

                if key == CONTAINS:
                    for key in expected_request.get_payload()[CONTAINS]:
                        if not commaseparated_list_is_subset_of(
                                got_request.get_payload()[key],
                                expected_request.get_payload()[CONTAINS][key]
                        ):
                            payload_is_accepted = False

                elif key == EXCLUDES:
                    for key in expected_request.get_payload()[EXCLUDES]:
                        if not all_element_of_commaseparated_list_is_expluded_from(
                                got_request.get_payload()[key],
                                expected_request.get_payload()[EXCLUDES][key]
                        ):
                            payload_is_accepted = False

                else:
                    if expected_request.get_payload()[key] != got_request.get_payload()[key]:
                        payload_is_accepted = False

        return url_is_same and method_is_same and payload_is_accepted
