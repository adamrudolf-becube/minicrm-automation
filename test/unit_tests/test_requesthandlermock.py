"""
This module contains requirements for RequestHandlerMock.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import unittest

from minicrm import crmrequestfactory
from requesthandlermock.requesthandlermock import RequestHandlerMock

ARBITRARY_STUDENT_ID = 42
ARBITRARY_STUDENT_ID_2 = 43
ARBITRARY_STUDENT_ID_3 = 44
RESPONSE_1 = 'b'
RESPONSE_2 = 'd'
RESPONSE_3 = 'f'


class TestRequestHandlerMock(unittest.TestCase):
    def setUp(self):
        """Initializes self.request_handler to the RequestHandlerMock with fake API info to be the SUT."""
        self.request_handler = RequestHandlerMock("FakeApi", "FakeApi")

    def test_check_if_satisfied_does_not_raise_when_there_is_no_expectation(self):
        """
        Given:
            - no expectations were made
        When:
            - request_handler.check_is_satisfied() is called
        Then:
            - no error is raised
        """

        self.request_handler.check_is_satisfied()

    def test_check_if_satisfied_raises_when_there_is_expectation(self):
        """
        Given:
            - one expectation is not fulfilled
        When:
            - request_handler.check_is_satisfied() is called
        Then:
            - AssertionError is raised starting with "Not all expectations were fulfilled when test ended."
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(ARBITRARY_STUDENT_ID),
            {u"fake": u"fake"}
        )
        with self.assertRaisesRegexp(AssertionError, "Not all expectations were fulfilled when test ended.") as cm:
            self.request_handler.check_is_satisfied()

    def test_match_expectation_raises_if_there_is_no_expectation(self):
        """
        Given:
            - there are no expectations in the queue
        When:
            - request_handler.match_expectation() is called
        Then:
            - AssertionError is raised, with the starting "No more commands were expected, but got"
        """

        with self.assertRaisesRegexp(AssertionError, "No more commands were expected, but got") as cm:
            self.request_handler.match_expectation(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID))

    def test_match_expectation_raises_when_other_command_comes(self):
        """
        Given:
            - next expected command in expectation queue is to get student X
        When:
            - request_handler.match_expectation() is called with getting student Y, where X is not equal to T
        Then:
            - AssertionError is raised, with the text starting by "Unexpected command"
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(ARBITRARY_STUDENT_ID),
            {u"fake": u"fake"}
        )
        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.request_handler.match_expectation(crmrequestfactory.get_student(137))

    def test_match_expectation_does_not_raise_when_correct_command_comes_exact_match(self):
        """
        Given:
            - there is an expectation
        When:
            - request_handler.match_expectation() is called with the next expected command in the queue
        Then:
            - no error is raised
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(ARBITRARY_STUDENT_ID),
            {u"fake": u"fake"}
        )
        self.request_handler.match_expectation(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID))

    def test_match_expectation_does_not_raise_when_correct_command_comes_contains(self):
        """
        test_match_expectation_does_not_raise_when_correct_command_comes_contains

        Given:
            - there is an expectation with crmrequestfactory.CONTAINS
        When:
            - request_handler.match_expectation() is called with the next expected command in the queue
        Then:
            - no error is raised
        """

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                ARBITRARY_STUDENT_ID,
                {
                    crmrequestfactory.CONTAINS: {
                        u"commaseparated_list": u"alpha, gamma"
                    }
                }
            ),
            {u"fake": u"fake"}
        )

        self.request_handler.match_expectation(
            crmrequestfactory.set_project_data(
                ARBITRARY_STUDENT_ID,
                {
                    u"commaseparated_list": u"alpha, beta, gamma, delta"
                }
            )
        )

    def test_match_expectation_raises_when_incorrect_command_comes_contains(self):
        """
        test_match_expectation_raises_when_incorrect_command_comes_contains

        Given:
            - there is an expectation with crmrequestfactory.OONTAINS
        When:
            - request_handler.match_expectation() is called with the next expected command in the queue, which doesn't
            contain all required elements
        Then:
            - AssertionError is raised
        """

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                ARBITRARY_STUDENT_ID,
                {
                    crmrequestfactory.CONTAINS: {
                        u"commaseparated_list": u"alpha, gamma, epsilon"
                    }
                }
            ),
            {u"fake": u"fake"}
        )

        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.request_handler.match_expectation(
                crmrequestfactory.set_project_data(
                    ARBITRARY_STUDENT_ID,
                    {
                        u"commaseparated_list": u"alpha, beta, gamma, delta"
                    }
                )
            )

    def test_match_expectation_does_not_raise_when_correct_command_comes_excludes(self):
        """
        test_match_expectation_does_not_raise_when_correct_command_comes_excludes

        Given:
            - there is an expectation with crmrequestfactory.EXCLUDES
        When:
            - request_handler.match_expectation() is called with the next expected command in the queue
        Then:
            - no error is raised
        """

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                ARBITRARY_STUDENT_ID,
                {
                    crmrequestfactory.EXCLUDES: {
                        u"commaseparated_list": u"epsilon, phi, khi"
                    }
                }
            ),
            {u"fake": u"fake"}
        )

        self.request_handler.match_expectation(
            crmrequestfactory.set_project_data(
                ARBITRARY_STUDENT_ID,
                {
                    u"commaseparated_list": u"alpha, beta, gamma, delta"
                }
            )
        )

    def test_match_expectation_raises_when_incorrect_command_comes_excludes(self):
        """
        test_match_expectation_raises_when_incorrect_command_comes_excludes

        Given:
            - there is an expectation with crmrequestfactory.EXCLUDES
        When:
            - request_handler.match_expectation() is called with the next expected command in the queue, which doesn't
            contxclude all required elements
        Then:
            - AssertionError is raised
        """

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                ARBITRARY_STUDENT_ID,
                {
                    crmrequestfactory.EXCLUDES: {
                        u"commaseparated_list": u"alpha, epsilon, phi, khi"
                    }
                }
            ),
            {u"fake": u"fake"}
        )

        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.request_handler.match_expectation(
                crmrequestfactory.set_project_data(
                    ARBITRARY_STUDENT_ID,
                    {
                        u"commaseparated_list": u"alpha, beta, gamma, delta"
                    }
                )
            )

    def test_match_expectation_does_not_raise_when_correct_command_comes_includes_excludes(self):
        """
        test_match_expectation_does_not_raise_when_correct_command_comes_includes_excludes

        Given:
            - there is an expectation with mixed crmrequestfactory.EXCLUDES, CONTAINS and exact match
        When:
            - request_handler.match_expectation() is called with the next expected command in the queue
        Then:
            - no error is raised
        """

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

        self.request_handler.match_expectation(
            crmrequestfactory.set_project_data(
                ARBITRARY_STUDENT_ID,
                {
                    u"exact_match": u"exact_element",
                    u"commaseparated_list": u"alpha, beta, gamma, delta"
                }
            )
        )

    def test_match_expectation_raises_when_incorrect_command_comes_includes_excludes_wrong_exact_match(self):
        """
        test_match_expectation_raises_when_incorrect_command_comes_contains

        Given:
            - there is an expectation with mixed crmrequestfactory.EXCLUDES, CONTAINS and exact match
        When:
            - request_handler.match_expectation() is called with the next expected command in the queue, with wrong
            exact match
        Then:
            - AssertionError is raised
        """

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

        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.request_handler.match_expectation(
                crmrequestfactory.set_project_data(
                    ARBITRARY_STUDENT_ID,
                    {
                        u"exact_match": u"exact_element_wrong",
                        u"commaseparated_list": u"alpha, beta, gamma, delta"
                    }
                )
            )

    def test_match_expectation_returns_expected_file_path(self):
        """
        Given:
            - there is an expectation
        When:
            - request_handler.match_expectation() is called with the next expected command in the queue
        Then:
            - correct preset response is returned
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_student(ARBITRARY_STUDENT_ID),
            {u"fake": u"fake"}
        )
        self.assertEqual(self.request_handler.match_expectation(
            crmrequestfactory.get_student(ARBITRARY_STUDENT_ID)),
            {u"fake": u"fake"}
        )

    def test_expectations_are_matched_in_correct_order(self):
        """
        Given:
            - series of expectations are set
        When:
            - requests are sent in the same order
            - check_if_ssatisfied is called
        Then:
            - no error is raised
        """

        self.request_handler.expect_request(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID), RESPONSE_1)
        self.request_handler.expect_request(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID_2), RESPONSE_2)
        self.request_handler.expect_request(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID_3), RESPONSE_3)
        self.request_handler.match_expectation(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID))
        self.request_handler.match_expectation(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID_2))
        self.request_handler.match_expectation(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID_3))
        self.request_handler.check_is_satisfied()

    def test_error_is_raised_when_commands_are_matched_in_wrong_order(self):
        """
        Given:
            - series of expectations are set
        When:
            - requests are sent in the wrong order
        Then:
            - AssertionError is raised with "Unexpected command"
        """

        self.request_handler.expect_request(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID), RESPONSE_1)
        self.request_handler.expect_request(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID_2), RESPONSE_2)
        self.request_handler.expect_request(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID_3), RESPONSE_3)
        self.request_handler.match_expectation(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID))
        with self.assertRaisesRegexp(AssertionError, "Unexpected command") as cm:
            self.request_handler.match_expectation(crmrequestfactory.get_student(ARBITRARY_STUDENT_ID_3))
