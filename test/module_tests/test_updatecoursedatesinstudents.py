# -*- coding: utf-8 -*-
"""
This module contains all of the tests and requirements for the subfunctionality called updatecoursedatesinstudetns.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2019"

import requesthandlermock.responses.courselists as responses_courselists
import requesthandlermock.responses.courses as responses_courses
import requesthandlermock.responses.general as responses_general
import requesthandlermock.responses.studentlists as responses_studentlists
from functionalities.subfunctionalities.updatecoursedatesinstudents import \
    update_course_dates_for_all_students_for_that_course
from minicrm import crmrequestfactory
from test.unit_tests.minicrmtestbase import MiniCrmTestBase


class TestUpdateCourseDatesInStudents(MiniCrmTestBase):

    def test_correct_list_of_students_is_updated_with_correct_data(self):
        """
        Correct list is updated by update_course_dates_for_all_students_for_that_course with correct data.

        Given:
            - 2 students applied to given course (regardless of their states)
        When:
            - update_course_dates_for_all_students_for_that_course is called
        Then:
            - both students are updated with the correct data (dates, dayoffs and date descriptions)
        """
        course_code = "2019-1-Q"
        course_id = 1164
        first_student_id = 2790
        second_student_id = 2796

        expected_data_to_update = {
            "N1Alkalom": "2019-01-28 23:59:59",
            "N2Alkalom2": "2019-02-04 23:59:59",
            "N3Alkalom2": "2019-02-11 23:59:59",
            "N4Alkalom2": "2019-02-18 23:59:59",
            "N5Alkalom2": "2019-02-25 23:59:59",
            "N6Alkalom2": "2019-03-04 23:59:59",
            "N7Alkalom2": "2019-03-18 23:59:59",
            "N8Alkalom2": "2019-03-25 23:59:59",
            "N9Alkalom2": "2019-04-01 23:59:59",
            "N10Alkalom2": "2019-04-08 23:59:59",
            "N2SzunetOpcionalis2": "2019-03-11 23:59:59",
            "N2SzunetOpcionalis3": "",
            "N3SzunetOpcionalis2": "",
            "Datumleirasok": "   - 2019-01-28\n   - 2019-02-04\n   - 2019-02-11\n   - 2019-02-18\n   - 2019-02-25\n   - 2019-03-04\n   - 2019-03-11 - szünet\n   - 2019-03-18\n   - 2019-03-25\n   - 2019-04-01\n   - 2019-04-08",
        }

        self.request_handler.expect_request(
            crmrequestfactory.get_course_list_by_course_code(course_code),
            responses_courselists.COURSE_LIST_FOR_COURSE_CODE
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_course(course_id),
            responses_courses.COURSE_2019_1_Q
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_student_list_by_course_code(course_code),
            responses_studentlists.WAITING_LIST_TWO_STUDENTS
        )

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                first_student_id,
                expected_data_to_update
            ),
            responses_general.XPUT_RESPONSE
        )

        self.request_handler.expect_request(
            crmrequestfactory.set_project_data(
                second_student_id,
                expected_data_to_update
            ),
            responses_general.XPUT_RESPONSE
        )

        update_course_dates_for_all_students_for_that_course(self.crm_facade, course_code)
