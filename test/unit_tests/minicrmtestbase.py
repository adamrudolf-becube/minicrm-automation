import datetime
import unittest

import crmrequestfactory
import test.requesthandlermock.responses.courselists as responses_courselists
import test.requesthandlermock.responses.courses as responses_courses
import test.requesthandlermock.responses.general as responses_general
import test.requesthandlermock.responses.studentlists as responses_studentlists
from commonfunctions import load_api_info
from crmfacade import CrmFacade
from test.requesthandlermock.requesthandlermock import RequestHandlerMock

API_INFO_JSON_FILE = "api_info_fake.json"


class MiniCrmTestBase(unittest.TestCase, object):
    def setUp(self):
        system_id, api_key = load_api_info(API_INFO_JSON_FILE)
        self.request_handler = RequestHandlerMock(system_id, api_key)

        self.expect_crmfacade_constructor()
        self.crm_facade = CrmFacade(self.request_handler, datetime.datetime(2019, 1, 25, 7, 30))

    def tearDown(self):
        self.request_handler.check_is_satisfied()

    def expect_crmfacade_constructor(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_modul_dictionary(),
            responses_general.MODULE_LIST)
        self.request_handler.expect_request(
            crmrequestfactory.get_schema_for_module_number(20),
            responses_general.SCHEMA_PROJECT_20_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_schema_for_module_number(21),
            responses_general.SCHEMA_PROJECT_21_COURSES)

    def set_participant_number_expectations(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2753),
            responses_courselists.LIST_OF_OPEN_COURSES_2753_ONE_COURSE_OPEN
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_project(2037),
            responses_courses.COURSE_2019_1_Q
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code("2019-1-Q"),
            responses_studentlists.COURSE_CODE_IS_2019_1_Q
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2037, {u"AktualisLetszam":6}),
            responses_general.XPUT_RESPONSE
        )
