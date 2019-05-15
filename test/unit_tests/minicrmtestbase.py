import datetime
import unittest

from minicrm import crmrequestfactory
import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.studentlists as responses_studentlists
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
            crmrequestfactory.get_schema_for_module_number(STUDENTS_MODULE_ID_NUMBER),
            responses_general.SCHEMA_PROJECT_20_STUDENTS)
        self.request_handler.expect_request(
            crmrequestfactory.get_schema_for_module_number(COURSES_MODULE_ID_NUMBER),
            responses_general.SCHEMA_PROJECT_21_COURSES)

    def set_participant_number_expectations(self):
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
            crmrequestfactory.set_project_data(FAKE_COURSE_ID_NUMBER, {u"AktualisLetszam":6}),
            responses_general.XPUT_RESPONSE
        )
