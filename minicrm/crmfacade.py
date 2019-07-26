# -*- coding: utf-8 -*-
"""
Contains a class to provide a facade for the MiniCRM system.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

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
    Acts as a facade to the MiniCRM system.

    This class implements human understandable methods to fetch from and write to the
    MiniCRM system, caches data if needed and handles the connection. Client code needs to use an instance of this
    class to have an API to the MiniCRM system.

    This class handles the connection, and knows the request types the system uses so the user doesn't have to handle
    these.
    """

    @stacktrace
    def __init__(self, request_handler, today=datetime.datetime.now()):
        """
        Constructor:

        Sets the login data required by the API, collects information about existing modules, and even initializes some
        of them.

        :param request_handler:
        :type request_handler: RequestHandler

        :param today: a date object the CrmFacade object will know as "today". Defaults to current date.
        :type today: datetime.datetime
        """
        self._request_handler = request_handler
        self._module_dict = None
        self._set_modules_dictionary()
        self._student_schema = self._get_schema_for_module(self._get_module_number_by_name(STUDENTS_MODULE_NAME))
        self._course_schema = self._get_schema_for_module(self._get_module_number_by_name(COURSES_MODULE_NAME))
        self._today = today

    @stacktrace
    def get_today(self):
        """
        Gets the the date stored in the instance as today.

        :return: the date stored in the instance as today's date. Is in format of datetime.datetime.
        :rtype: datetime.datetime
        """

        return self._today

    def set_today(self, today):
        """
        Sets the the date stored in the instance as today.

        Only for testing purposes. If different tests need different "_today" dates, constructor can be called in setup
        then _today can be set differently in separate tests.

        :param today: should be datetime.datetime object
        :type today: datetime.datetime

        :return: None
        """

        self._today = today

    @stacktrace
    def get_student(self, student_number):
        """
        Fetches a student with the given ID from the MiniCRM system and returns it's data as a dictionary.

        :param student_number: integer, ID of the student
        :type student: int

        :return: dictionary, complying with the schema of the student module
        :rtype: dict
        """

        return self._get_project(student_number)

    @stacktrace
    def get_student_list_with_status(self, status):
        """
        Returns all students with the given status.

        :param status: specifies a desired status.
        :type status: str

        :return: the students with the given status. Key is the ID number.
        :rtype: dict
        """

        return self._query_project_list_with_status_id(self.get_student_status_number_by_name(status))

    @stacktrace
    def get_student_status_number_by_name(self, status_name):
        """
        Returns the ID number of the given status.

        MiniCRM system works with status numbers. The number is what usually the API requests require, but often it's
        easier for the clients to handle the human readable status names. This function is used to provide the status
        number if only the status name is known.

        :raises ValueError: if nonexistent status_name is given

        :param status_name: string, name of a status
        :type status_name: stt

        :return: integer, the status number of the given status
        :rtype: dict
        """

        status_dictionary = self._student_schema[STATUS_ID_FIELD]
        return_value = get_key_from_value(status_dictionary, status_name)
        trace("STATUS CODE FOR [{}] IS [{}]".format(status_name, return_value))
        return return_value

    @stacktrace
    def set_student_data(self, student_number, data):
        """
        Is used to modify data of a student stored in MiniCRM system.

        :param student_number: ID number of the student.
        :type student_number: int

        :param data: Has to have the structure of a student as stored in the MiniCRM system.
        :type data: dict

        :return: None
        """

        self._set_project_data(student_number, data)

    @stacktrace
    def get_course(self, course_number):
        """
        Returns the dictionary of a course.

        :param course_number: ID number of a course
        :type course_number: int

        :return: dictionary, containing all information about the given ourse
        :rtype: dict
        """

        return self._get_project(course_number)

    @stacktrace
    def get_course_list_with_status(self, status):
        """
        Returns all courses with the given status.

        :param status: the desired status.
        :type status: str

        :return: dictionary of the courses with the given status.
        :rtype: dict
        """

        return self._query_project_list_with_status_id(self.get_course_status_number_by_name(status))

    @stacktrace
    def get_course_status_number_by_name(self, status_name):
        """
        Returns the ID number of the given status.

        MiniCRM system works with status numbers. The number is what usually the API requests require, but often it's
        easier for the clients to handle the human readable status names. This function is used to provide the status
        number if only the status name is known.

        :raises ValueError: if nonexistent status_name is given

        :param status_name: name of a status
        :type status_name: str

        :return: the status number of the given status
        :rtype: int
        """

        status_dictionary = self._course_schema[STATUS_ID_FIELD]
        return_value = get_key_from_value(status_dictionary, status_name)
        trace("STATUS CODE FOR [{}] IS [{}]".format(status_name, return_value))
        return return_value

    @stacktrace
    def get_course_by_course_code(self, course_code):
        """
        Returns the dictionary of a course.

        :param course_code: Course code of a course
        :type course_code: int

        :return: containing all information about the given ourse
        :rtype: dict
        """

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
    def set_course_data(self, course_number, data):
        """
        Is used to modify data of a course stored in MiniCRM system.

        :param course_number: ID number of the course.
        :type course_number: int

        :param data: Has to have the structure of a student as stored in the MiniCRM system.
        :type data: dict

        :return: None
        """

        self._set_project_data(course_number, data)

    @stacktrace
    def get_location_by_name(self, location_name):
        """
        Returns the dictionary of a location for a given name.

        - returns one of the locations if name is not unique

        - returns None if name doesn't exist

        :param location_name: Course code of a course
        :type location_name: int

        :return: containing all information about the given location
        :rtype: dict
        """

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
        Loops through all courses in Application Open ("Jelentkezés nyitva") state, and updates their headcount fields.

        It writes the result to the CRM page of the course.

        A student is considered enrolled to a course if their status is either "INFO Sent" ("INFO levél kiment") or
        "Course In Progress" ("Kurzus folyamatban").

        The function loops through all courses in Application Open ("Jelentkezés nyitva") state in a big loop, and for
        each course in the loop, it loops through all of the students who are registered to that course and counts how
        many of them are in any of the above mentioned stated. When it finishes the small loop, it updates the field for
        the current headcount of the currently processed course.

        After calling this method, the user can be sure that all courses are in up-to-date state.

        :return: None
        """
        open_courses = self.get_course_list_with_status(APPLICATION_OPEN_STATE)
        pretty_print(open_courses)

        for course in open_courses:

            course_data = self._get_project(course)
            course_code = course_data[COUSE_CODE_FIELD]

            trace("CALCULATE HEADCOUNT OF COURSE [" + course + "], code: [" + course_code + "]")

            students_in_current_course = self._request_handler.fetch(
                crmrequestfactory.get_student_list_by_course_code(course_code))[RESULTS_FIELD]

            acceptable_statuses = [
                int(self.get_student_status_number_by_name(INFO_SENT_STATE)),
                int(self.get_student_status_number_by_name(COURSE_IN_PROGRESS_STATE))
            ]

            trace("ACCEPTABLE STATUSES: [{}]".format(acceptable_statuses))

            count = 0
            for student in students_in_current_course:
                if students_in_current_course[student][STATUS_ID_FIELD] in acceptable_statuses:
                    count += 1
                    trace("STUDENT [{}] has status [{}], ACCEPTABLE, CURRENT HEADCOUNT: [{}]".
                          format(student, students_in_current_course[student][STATUS_ID_FIELD], count))
                else:
                    trace("STUDENT [{}] has status [{}], NOT ACCEPTABLE, CURRENT HEADCOUNT: [{}]".
                          format(student, students_in_current_course[student][STATUS_ID_FIELD], count))

            trace("END OF STUDENT LIST, UPDATING HEADCOUNT TO [{}]".format(count))

            self._request_handler.fetch(
                crmrequestfactory.set_project_data(course, {CURRENT_HEADCOUNT_FIELD: count}))

    @stacktrace
    def raise_task(
            self,
            project_id,
            comment,
            deadline,
            user_id=""):
        """
        Creates a new task in the MiniCRM system with the given details.

        :param project_id: the task will be raised to the project (student, course, location, etc.) identified by this
                           ID.
        :type project_id: int

        :param comment: the text shown as the contents (description) of the task
        :type comment: str

        :param deadline: date, set as deadline in the MiniCRM system. Has to be in the "%Y-%m-%d %H:%M:%S"" format.
        :type deadline: str

        :param user_id: MiniCRM user who is responsible (assignee) for the task
        :type user_id: int

        :return: None
        """

        self._request_handler.fetch(
            crmrequestfactory.raise_task(project_id, comment, deadline, user_id))

    @stacktrace
    def copy_applied_course_to_course_code(self, student_data):
        """
        Copies the "MelyikTanfolyamErdekli" field to "TanfolyamKodja".

        Code of the course ("TanfolyamKodja") will be equal to the course they applied to ("MelyikTanfolyamErdekli").
        This is because the latter one changes every time the registration form on MiniCRM is updated, but this way
        the course code is saved.

        :param student_data: all of the date about a student as stored in the MiniCRM system.
        :type student_data: dict

        :return: None
        """
        data_to_update = {
            "TanfolyamKodja": student_data["MelyikTanfolyamErdekli"]
        }

        trace("DATA TO BE REPLACED:")
        pretty_print(data_to_update)

        self._request_handler.fetch(crmrequestfactory.set_project_data(student_data["Id"], data_to_update))


    @stacktrace
    def fill_student_data(self, student_data, course_data):
        """
        Updates the following data of the student:

        - Detailed description of the location (fetched from locations)

        The following will be copied from the course data:

        - Type of the course

        - Time of the lectures (during the day)

        - Date of every lecture

        - Date of every dayoffs

        The following will be calculated:

        - Application deadline determined by the following algorithm (applied in this order):

            1. by default, it is 5 days
            2. If the course starts in less than 7 days, or less than 30% of places is free, it is set to 3 days
            3. If the course starts in less than 3 days, and there is no more than 3 places, it will be 1 day
            4. If the starting day is earlier than the calculated deadline, it will be the starting day - 1 day
            5. If the deadline is earlier than now, it is now + 1 day

        - Date descriptions. This is one string containing all of the lectures and vacations, directly insertable to
          emails.

        :param student_data: all of the date about a student as stored in the MiniCRM system.
        :type student_data: dict

        :param course_data: all of the date about a course the student has applied to as stored in the MiniCRM system.
        :type course_data: dict

        :return: None
        """
        data_to_update = {
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
        course_starting_day = datetime.datetime.strptime(course_data[COURSE_FIRST_OCCASION_DATE_FIELD], DATE_FORMAT)
        free_spots = course_data[MAX_HEADCOUNT_FIELD] - course_data[CURRENT_HEADCOUNT_FIELD]
        all_spots = course_data[MAX_HEADCOUNT_FIELD]
        if all_spots == 0:
            all_spots = 1

        if course_starting_day - self.get_today() < datetime.timedelta(days=7) or (
                (1.0 * free_spots) / (1.0 * all_spots)) < 0.3:
            days_left_to_apply = 3

        if course_starting_day - self.get_today() < datetime.timedelta(days=3) and free_spots <= 3:
            days_left_to_apply = 1

        deadline = self.get_today() + datetime.timedelta(days=days_left_to_apply)

        if deadline > course_starting_day:
            deadline = course_starting_day + datetime.timedelta(days=-1)

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
