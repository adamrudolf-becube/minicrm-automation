# -*- coding: utf-8 -*-
import datetime

from minicrm import crmrequestfactory
import quickscript
import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.locationlists as responses_locationlists
import requesthandlermock.responses.locations as responses_locations
import requesthandlermock.responses.studentlists as responses_studentlists
import requesthandlermock.responses.students as responses_students
from test.unit_tests.minicrmtestbase import MiniCrmTestBase


class TestQuickScript(MiniCrmTestBase):
    def test_quick_script_calls_correct_functions(self):
        self.expect_clean_info_sent()
        self.expect_handle_waiting_list()
        self.expect_register_new_applicants()

        quickscript.run(self.crm_facade)

    def expect_clean_info_sent(self):
        self.crm_facade.set_today(datetime.datetime(2019, 1, 22, 12, 0))

        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2781),
            responses_studentlists.INFO_SENT_ONE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2941),
            responses_students.FAKE_STUDENT)

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2941,
                {u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Egy napod van jelentkezni"}
            ),
            responses_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()

    def expect_handle_waiting_list(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2750),
            responses_studentlists.WAITING_LIST_ONE_STUDENT)
        self.request_handler.expect_request(
            crmrequestfactory.get_student(2790),
            responses_students.FAKE_STUDENT)
        self.set_participant_number_expectations()
        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_FULL
        )
        self.set_participant_number_expectations()

    def expect_register_new_applicants(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_project_list_for_status(2741),
            responses_studentlists.NEW_APPLICANTS_ONE_STUDENT)
        self.set_participant_number_expectations()

        self.request_handler.expect_request(
            crmrequestfactory.get_student(2941),
            responses_students.FAKE_STUDENT)

        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code("2019-1-Q"),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )
        self.request_handler.expect_request(
            crmrequestfactory.get_course(1164),
            responses_courses.COURSE_2019_1_Q_ONE_PLACE_FREE)

        self.request_handler.expect_request(
            crmrequestfactory.get_location_list_by_location_name("Pannon Kincstár"),
            responses_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_location(19),
            responses_locations.PANNON_KINCSTAR
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(2601, crmrequestfactory._),
            responses_general.XPUT_RESPONSE
        )
        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                2601,
                {u"StatusId": u"2781", u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l"}
            ),
            responses_general.XPUT_RESPONSE
        )
