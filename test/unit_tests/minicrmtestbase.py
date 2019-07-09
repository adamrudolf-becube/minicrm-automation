"""
Contains a class to serve as the common abstract base class for all of the test cases.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import datetime
import unittest

import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.studentlists as responses_studentlists
from minicrm import crmrequestfactory
from minicrm.commonfunctions import load_api_info
from minicrm.crmfacade import CrmFacade
from requesthandlermock.requesthandlermock import RequestHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"
STUDENTS_MODULE_ID_NUMBER = 20
COURSES_MODULE_ID_NUMBER = 21
COURSE_OPEN_STATUS_NUMBER = 2753
FAKE_COURSE_ID_NUMBER = 2037
FAKE_COURSE_COURSE_CODE = "2019-1-Q"


class MiniCrmTestBase(unittest.TestCase, object):
    """
    Contains common functionality for MiniCRM tests.

    MiniCrmTestBase contains the common parts of test setUp and tearDown, which use the RequestHandlerMock and CrmFacade
    classes. This class also provides commonly used helper functions and creates the needed datamembers.
    """

    def setUp(self):
        """
        Creates a RequestHandlerMock with the fake API login info, and creates the CrmFacaade with the mock.

        Also sets and satisfies expectations for creating CrmFacade.

        Tests derived from MiniCrmTestBase can define their own setups if needed, but they have to call this setUp
        explicitly in the very beginning of their setUps.
        """

        system_id, api_key = load_api_info(API_INFO_JSON_FILE)
        self.request_handler = RequestHandlerMock(system_id, api_key)

        self.expect_crmfacade_constructor()
        self.crm_facade = CrmFacade(self.request_handler, datetime.datetime(2019, 1, 25, 7, 30))

    def tearDown(self):
        """
        Checks whether all expectations of the RequestHandlerMock have been satisfied, so it guarantees that no
        unsatisfied expectations are left in any tests.
        """

        self.request_handler.check_is_satisfied()

    def expect_crmfacade_constructor(self):
        """
        Sets all expectations for creating the CrmFacade instance.

        If you need to create a CrmFacade instance, this method provides an easy way to prepare for the API requests
        sent by the constructor. You just call this method, instantiate the CrmFacade instance and you can have a fresh
        start without errors and with an empty expectation queue.

        Example code:

        .. code-block:: python

            system_id, api_key = load_api_info(API_INFO_JSON_FILE)
            self.request_handler = RequestHandlerMock(system_id, api_key)

            self.expect_crmfacade_constructor()
            self.crm_facade = CrmFacade(self.request_handler, datetime.datetime(2019, 1, 25, 7, 30))

        """

        self.request_handler.expect_request(
            crmrequestfactory.get_modul_dictionary(),
            responses_general.MODULE_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_schema_for_module_number(STUDENTS_MODULE_ID_NUMBER),
            responses_general.SCHEMA_PROJECT_20_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_schema_for_module_number(COURSES_MODULE_ID_NUMBER),
            responses_general.SCHEMA_PROJECT_21_COURSES)

    def set_participant_number_expectations(self):
        """
        Sets expectations for the update_headcounts() method of CrmFacade.

        CrmFacade's update_headcounts() is a commonly used method, which creates a typical pattern of API requests. This
        pattern has to be expected again and again in every test which uses the update_headcounts() method, maybe
        multiple times in a use case. This method provides a single line to set those expectations, and also logically
        group these expectations, and make the code easier to read.
        """

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(COURSE_OPEN_STATUS_NUMBER),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_project(FAKE_COURSE_ID_NUMBER),
            responses_courses.COURSE_2019_1_Q
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(FAKE_COURSE_COURSE_CODE),
            responses_studentlists.COURSE_CODE_IS_2019_1_Q
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam": 6}),
            responses_general.XPUT_RESPONSE
        )
