# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school
import datetime

import crmrequestfactory
from commonfunctions import get_key_from_value, merge_dicts
from tracing import stacktrace, trace, pretty_print

STUDENTS_MODULE_NAME = "Jelentkezés"
COURSES_MODULE_NAME = "Tanfolyamok"
APPLICATION_OPEN_STATE = "Jelentkezés nyitva"
INFO_SENT_STATE = "INFO levél kiment"
COURSE_IN_PROGRESS_STATE = "Kurzus folyamatban"
RESULTS_FIELD = "Results"
STATUS_ID_FIELD = "StatusId"
COUSE_CODE_FIELD = "TanfolyamBetujele"
CURRENT_HEADCOUNT_FIELD = "AktualisLetszam"
MAX_HEADCOUNT_FIELD = "MaximalisLetszam"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DETAILED_LOCATION_DESCRIPTION_FIELD = "ReszletesHelyszinleiras"
COUNT_FIELD = "Count"

COURSE_FIRST_OCCASION_DATE_FIELD = "ElsoAlkalom"
COURSE_SECOND_OCCASION_DATE_FIELD = "N2Alkalom"
COURSE_THIRD_OCCASION_DATE_FIELD = "N3Alkalom"
COURSE_FOURTH_OCCASION_DATE_FIELD = "N4Alkalom"
COURSE_FIFTH_OCCASION_DATE_FIELD = "N5Alkalom"
COURSE_SIXTH_OCCASION_DATE_FIELD = "N6Alkalom"
COURSE_SEVENTH_OCCASION_DATE_FIELD = "N7Alkalom"
COURSE_EIGTH_OCCASION_DATE_FIELD = "N8Alkalom"
COURSE_NINTH_OCCASION_DATE_FIELD = "N9Alkalom"
COURSE_TENTH_OCCASION_DATE_FIELD = "N10Alkalom"

COURSE_FISRST_DAYOFF_FIELD = "N1SzunetOpcionalis"
COURSE_SECOND_DAYOFF_FIELD = "N2SzunetOpcionalis"
COURSE_THIRD_DAYOFF_FIELD = "N3SzunetOpcionalis"


class CrmFacade:
    """
    Acts as a facade to the MiniCRM. This class implements human understandable methods to fetch from and write to the
    MiniCRM system, caches data if needed and handles the connection. Business code needs to use an instance of this
    class to have an API to the MiniCRM system.
    """

    @stacktrace
    def __init__(self, request_handler, today=datetime.datetime.now()):
        """
        Sets the login data required by the API, collects information about existing modules, and even initializes some fo them
        """
        self._request_handler = request_handler
        self._module_dict = None
        self._set_modules_dictionary()
        self._student_schema = self._get_schema_for_module(self._get_module_number_by_name(STUDENTS_MODULE_NAME))
        self._course_schema = self._get_schema_for_module(self._get_module_number_by_name(COURSES_MODULE_NAME))
        self._today = today

    @stacktrace
    def get_today(self):
        return self._today

    def set_today(self, today):
        """
        Only for testing purposes. If different tests need different "_today" dates, constructor can be called in setup
        then _today can be set differently in separate tests.
        :param today: should be datetime.datetime object
        :return: None
        """
        self._today = today

    @stacktrace
    def get_student(self, student):
        """
        Fetches a student with the given ID from the MiniCRM system and returns it's data as a dictionary.
        :param student: integer, ID of the student
        :return: dictionary, complying with the schema of the student module
        """
        return self._get_project(student)

    @stacktrace
    def get_student_list_with_status(self, status):
        return self._query_project_list_with_status_id(self.get_student_status_number_by_name(status))

    @stacktrace
    def get_student_status_number_by_name(self, status_name):
        status_dictionary = self._student_schema[STATUS_ID_FIELD]
        return_value = get_key_from_value(status_dictionary, status_name)
        trace("STATUS CODE FOR [{}] IS [{}]".format(status_name, return_value))
        return return_value

    @stacktrace
    def set_student_data(self, student, data):
        self._set_project_data(student, data)

    @stacktrace
    def get_course(self, course):
        return self._get_project(course)

    @stacktrace
    def get_course_list_with_status(self, status):
        return self._query_project_list_with_status_id(self.get_course_status_number_by_name(status))

    @stacktrace
    def get_course_status_number_by_name(self, status_name):
        status_dictionary = self._course_schema[STATUS_ID_FIELD]
        return_value = get_key_from_value(status_dictionary, status_name)
        trace("STATUS CODE FOR [{}] IS [{}]".format(status_name, return_value))
        return return_value

    @stacktrace
    def get_course_by_course_code(self, course_code):

        course_list = self._request_handler.fetch(
            crmrequestfactory.get_course_list_by_course_code(course_code)
        )

        pretty_print(course_list)
        for course in course_list[RESULTS_FIELD]:
            return self._request_handler.fetch(
                crmrequestfactory.get_course(course))

        trace("COURSE NOT FOUND: [{}]".format(course_code))
        return None

    @stacktrace
    def set_course_data(self, course, data):
        self._set_project_data(course, data)

    @stacktrace
    def get_location_by_name(self, location_name):

        location_list = self._request_handler.fetch(
            crmrequestfactory.get_location_list_by_location_name(location_name)
        )

        pretty_print(location_list)
        for location in location_list[RESULTS_FIELD]:
            return self._request_handler.fetch(
                crmrequestfactory.get_location(location))

        trace("COURSE NOT FOUND: [{}]".format(location_name))
        return None

    @stacktrace
    def update_headcounts(self):
        """
        Loops through all open ("Jelentkezés nyitva") courses, and calculates how many applicants are there.
        It writes the result to the CRM page of the course.
        """
        course_list = self.get_course_list_with_status(APPLICATION_OPEN_STATE)
        pretty_print(course_list)

        for course in course_list:

            course_data = self._get_project(course)
            course_code = course_data[COUSE_CODE_FIELD]

            trace("CALCULATE HEADCOUNT OF COURSE [" + course + "], code: [" + course_code + "]")

            trace("APPLICATION IS OPEN, CALCULATING HEADCOUNT")

            student_list = self._request_handler.fetch(
                crmrequestfactory.get_student_list_by_course_code(course_code))[RESULTS_FIELD]

            acceptable_statuses = [
                int(self.get_student_status_number_by_name(INFO_SENT_STATE)),
                int(self.get_student_status_number_by_name(COURSE_IN_PROGRESS_STATE))
            ]

            trace("ACCEPTABLE STATUSES: [{}]".format(acceptable_statuses))

            count = 0
            for student in student_list:
                if student_list[student][STATUS_ID_FIELD] in acceptable_statuses:
                    count += 1
                    trace("STUDENT [{}] has status [{}], ACCEPTABLE, CURRENT HEADCOUNT: [{}]".
                          format(student, student_list[student][STATUS_ID_FIELD], count))
                else:
                    trace("STUDENT [{}] has status [{}], NOT ACCEPTABLE, CURRENT HEADCOUNT: [{}]".
                          format(student, student_list[student][STATUS_ID_FIELD], count))

            trace("END OF STUDENT LIST, UPDATING HEADCOUNT TO [{}]".format(count))

            self._request_handler.fetch(
                crmrequestfactory.set_project_data(course, {CURRENT_HEADCOUNT_FIELD: count}))

    @stacktrace
    def raise_task(
            self,
            project_id,
            comment,
            deadline,
            userid=""):
        """
        Creates a new task in teh CRM ssytem with the given details
        """

        self._request_handler.fetch(
            crmrequestfactory.raise_task(project_id, comment, deadline, userid))

    @stacktrace
    def fill_student_data(self, student_data, course_data):
        data_to_update = {
            "TanfolyamKodja": student_data["MelyikTanfolyamErdekli"],
            "TanfolyamTipusa2": course_data["TanfolyamTipusa"],
            "Helyszin2": course_data["Helyszin"],
            "HelyszinReszletesLeiras": self._get_detailed_description_of_location(course_data["Helyszin"]),
            "OrakIdopontja2": course_data["OrakIdopontja"],
            "N1Alkalom": course_data["ElsoAlkalom"],
            "N2Alkalom2": course_data["N2Alkalom"],
            "N3Alkalom2": course_data["N3Alkalom"],
            "N4Alkalom2": course_data["N4Alkalom"],
            "N5Alkalom2": course_data["N5Alkalom"],
            "N6Alkalom2": course_data["N6Alkalom"],
            "N7Alkalom2": course_data["N7Alkalom"],
            "N8Alkalom2": course_data["N8Alkalom"],
            "N9Alkalom2": course_data["N9Alkalom"],
            "N10Alkalom2": course_data["N10Alkalom"],
            "N2SzunetOpcionalis2": course_data["N1SzunetOpcionalis"],
            "N2SzunetOpcionalis3": course_data["N2SzunetOpcionalis"],
            "N3SzunetOpcionalis2": course_data["N3SzunetOpcionalis"],
            "VeglegesitesiHatarido": self._get_application_deadline(course_data),
            "Datumleirasok": self._get_date_description(course_data)
        }

        trace("DATA TO BE REPLACED:")
        pretty_print(data_to_update)

        self._request_handler.fetch(crmrequestfactory.set_project_data(student_data["Id"], data_to_update))

    # Private methods --------------------------------------------------------------------------------------------------

    @stacktrace
    def _set_project_data(self, student, data):
        self._request_handler.fetch(
            crmrequestfactory.set_project_data(student, data))

    @stacktrace
    def _query_project_list_with_status_id(self, status_id):
        trace(status_id)
        response = self._request_handler.fetch(
            crmrequestfactory.get_project_list_for_status(status_id))
        if response[COUNT_FIELD] > 100:
            response_second_page = self._request_handler.fetch(
                crmrequestfactory.get_project_list_for_status_page1(status_id))
            response[RESULTS_FIELD] = merge_dicts(response[RESULTS_FIELD], response_second_page[RESULTS_FIELD])

        return response[RESULTS_FIELD]

    def _get_schema_for_module(self, module):
        return self._request_handler.fetch(
            crmrequestfactory.get_schema_for_module_number(module))

    @stacktrace
    def _set_modules_dictionary(self):
        self._module_dict = self._request_handler.fetch(crmrequestfactory.get_modul_dictionary())

    @stacktrace
    def _get_project(self, id):
        return self._request_handler.fetch(crmrequestfactory.get_project(id))

    @stacktrace
    def _get_module_number_by_name(self, module_name):
        return self._module_dict.keys()[self._module_dict.values().index(module_name)]

    @stacktrace
    def _get_detailed_description_of_location(self, location_name):
        location_data = self.get_location_by_name(location_name)
        pretty_print(location_data)
        return location_data[DETAILED_LOCATION_DESCRIPTION_FIELD]

    @stacktrace
    def _get_application_deadline(self, course_data):
        """
        Returns a serialized datetime, which is the the deadline for the student to finalize his/her application.

        Algorithm:
        1. by default, it is 5 days
        2. If the course starts in less than 7 days, or less than 30% of places is free, it is set to 3 days
        3. If the course starts in less than 3 days, and there is no more than 3 places, it will be 1 day
        4. If the starting day is earlier than the calculated deadline, it will be the starting day - 1 day
        5. If the deadline is earlier than now, it is now + 1 day
        """
        days_left_to_apply = 5
        starting_day = datetime.datetime.strptime(course_data[COURSE_FIRST_OCCASION_DATE_FIELD], DATE_FORMAT)
        free_spots = course_data[MAX_HEADCOUNT_FIELD] - course_data[CURRENT_HEADCOUNT_FIELD]
        all_spots = course_data[MAX_HEADCOUNT_FIELD]
        if all_spots == 0:
            all_spots = 1

        if starting_day - self.get_today() < datetime.timedelta(days=7) or (
                (1.0 * free_spots) / (1.0 * all_spots)) < 0.3:
            days_left_to_apply = 3

        if starting_day - self.get_today() < datetime.timedelta(days=3) and free_spots <= 3:
            days_left_to_apply = 1

        deadline = self.get_today() + datetime.timedelta(days=days_left_to_apply)

        if deadline > starting_day:
            deadline = starting_day + datetime.timedelta(days=-1)

        if deadline < self.get_today():
            deadline = self.get_today() + datetime.timedelta(days=1)

        return deadline.__str__()

    @stacktrace
    def _get_date_description(self, course_data):
        date_list = []
        date_list.append(course_data[COURSE_FIRST_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_SECOND_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_THIRD_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_FOURTH_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_FIFTH_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_SIXTH_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_SEVENTH_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_EIGTH_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_NINTH_OCCASION_DATE_FIELD][:10])
        date_list.append(course_data[COURSE_TENTH_OCCASION_DATE_FIELD][:10])
        if course_data[COURSE_FISRST_DAYOFF_FIELD] != "":
            date_list.append("{} - {}".format(course_data[COURSE_FISRST_DAYOFF_FIELD][:10], "szünet"))
        if course_data[COURSE_SECOND_DAYOFF_FIELD] != "":
            date_list.append("{} - {}".format(course_data[COURSE_SECOND_DAYOFF_FIELD][:10], "szünet"))
        if course_data[COURSE_THIRD_DAYOFF_FIELD] != "":
            date_list.append("{} - {}".format(course_data[COURSE_THIRD_DAYOFF_FIELD][:10], "szünet"))

        date_list.sort()

        return_string = "   - " + "\n   - ".join(date_list)

        trace("JOINED STRING:\n{}".format(return_string))

        return return_string
