# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from tracing import stacktrace, trace, pretty_print
import datetime
from commandmapper import CommandMapper
from modules import CustomerList, CourseList, LocationList
from commonfunctions import add_element_to_commasep_list


class CrmData:
    """
    Representation of high-level CRM data.
    Stores a colelction of modules as module objects.
    Responsible for bookkeeping of module ID-s, creating and deleting modules.
    """

    @stacktrace
    def __init__(self, system_id, api_key, command_handler, today=datetime.datetime.now()):
        """
        Sets the login data required by the API, collects information about existing modules, and even initializes some fo them
        """
        self.api_key = api_key
        self.system_id = system_id
        self.command_mapper = CommandMapper(system_id, api_key)
        self.command_handler = command_handler
        self.set_modules_dictionary()
        # TODO are these lists really used?
        self.jelentkezok = CustomerList(
            self.get_module_number_by_name("Jelentkezés"),
            self.system_id,
            self.api_key,
            command_handler)
        self.tanfolymok = CourseList(
            self.get_module_number_by_name("Tanfolyamok"),
            self.system_id,
            self.api_key,
            command_handler)
        self.today = today

    def set_today(self, today):
        """
        Only for testing purposes. If different tests need different "today" dates, constructor can be called in setup
        then today can be set differently in separate tests.
        :param today: should be datetime.datetime object
        :return: None
        """
        self.today = today

    @stacktrace
    def get_student_list_with_status(self, status):
        return self.jelentkezok.query_project_list_with_status(status)["Results"]

    @stacktrace
    def get_student(self, student):
        return self.get_project(student)

    @stacktrace
    def get_today(self):
        return self.today

    @stacktrace
    def get_student_status_number_by_name(self, statusname):
        return self.jelentkezok.get_status_number_by_name(statusname)

    @stacktrace
    def set_student_data(self, student, data):
        self.command_handler.get_json_array_for_command(
            self.command_mapper.set_project_data(student, data))

    @stacktrace
    def get_course_by_course_code(self, course_code):
        return self.tanfolymok.get_course_by_course_code(course_code)

    # Private methods --------------------------------------------------------------------------------------------------

    @stacktrace
    def send_initial_letter(self, student_data, course_data):
        """
        Based on the given student, and course, the system sends
        an INFO or a waitinglist letter, and sets the status of
        the student accordingly.
        """
        update_data = {}

        if course_data["AktualisLetszam"] >= course_data["MaximalisLetszam"]:

            trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO WAITING LIST.".
                format(course_data["AktualisLetszam"], course_data["MaximalisLetszam"]))

            update_data["Levelkuldesek"] = student_data["Levelkuldesek"] + ", Várólista"

            update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("Várólistán van")

        else:

            trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO COURSE.".
                format(course_data["AktualisLetszam"], course_data["MaximalisLetszam"]))

            trace("TYPE OF COURSE IS: [{}] ".format(course_data["TanfolyamTipusa"]))

            if (course_data["TanfolyamTipusa"] == "Kezdő programozó tanfolyam"):
                trace("IN KEZDO IF")
                update_data["Levelkuldesek"] = add_element_to_commasep_list(student_data["Levelkuldesek"], "Kezdő INFO levél")

            elif (course_data["TanfolyamTipusa"] == "Haladó programozó tanfolyam"):
                trace("IN HALADO IF")
                update_data["Levelkuldesek"] = add_element_to_commasep_list(student_data["Levelkuldesek"], "Haladó INFO levél")

            update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("INFO levél kiment")


        trace("DATA TO UPDATE:")
        pretty_print(update_data)

        self.command_handler.get_json_array_for_command(
            self.command_mapper.set_project_data(student_data["Id"], update_data))

    @stacktrace
    def update_headcounts(self):
        """
        Loops through all open ("Jelentkezés nyitva") courses, and calculates how many applicants are there. It writes the result to the CRM page of the course.
        """
        course_list = self.tanfolymok.query_project_list_with_status("Jelentkezés nyitva")["Results"]
        pretty_print(course_list)

        for course in course_list:

            course_data = self.get_project(course)
            course_code = course_data["TanfolyamBetujele"]

            trace("CALCULATE HEADCOUNT OF COURSE ["+course+"], code: ["+course_code+"]")

            trace("APPLICATION IS OPEN, CALCULATING HEADCOUNT")

            student_list = self.command_handler.get_json_array_for_command(
                             self.command_mapper.get_course_by_course_code(course_code))["Results"]

            acceptable_statuses = [
                int(self.jelentkezok.get_status_number_by_name("INFO levél kiment")),
                int(self.jelentkezok.get_status_number_by_name("Kurzus folyamatban"))
            ]

            trace("ACCEPTABLE STATUSES: [{}]".format(acceptable_statuses))

            count = 0
            for student in student_list:
                if student_list[student]["StatusId"] in acceptable_statuses:
                    count += 1
                    trace("STUDENT [{}] has status [{}], ACCEPTABLE, CURRENT HEADCOUNT: [{}]".
                        format(student, student_list[student]["StatusId"], count))
                else:
                    trace("STUDENT [{}] has status [{}], NOT ACCEPTABLE, CURRENT HEADCOUNT: [{}]".
                        format(student, student_list[student]["StatusId"], count))

            trace("END OF STUDENT LIST, UPDATING HEADCOUNT TO [{}]".format(count))

            self.command_handler.get_json_array_for_command(
                self.command_mapper.set_project_data(course, {"AktualisLetszam": count}))

    @stacktrace
    def set_modules_dictionary(self):
        self.module_dict = self.command_handler.get_json_array_for_command(self.command_mapper.get_modul_dictionary())

    @stacktrace
    def get_project(self, id):
        return self.command_handler.get_json_array_for_command(self.command_mapper.get_project(id))

    @stacktrace
    def get_module_number_by_name(self, module_name):
        return self.module_dict.keys()[self.module_dict.values().index(unicode(module_name, "utf-8"))]

    @stacktrace
    def get_detailed_description(self, location):
        location_list = LocationList(self.get_module_number_by_name("Helyszínek"),
                                     self.system_id,
                                     self.api_key,
                                     self.command_handler)

        location_data = location_list.get_location_by_name(location)
        pretty_print(location_data)
        return location_data["ReszletesHelyszinleiras"]

    @stacktrace
    def get_application_deadline(self, course_data):
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
        starting_day = datetime.datetime.strptime(course_data["ElsoAlkalom"], "%Y-%m-%d %H:%M:%S")
        free_spots = course_data["MaximalisLetszam"] - course_data["AktualisLetszam"]
        all_spots = course_data["MaximalisLetszam"]
        if all_spots == 0:
            all_spots = 1

        if starting_day - self.today < datetime.timedelta(days = 7) or ((1.0*free_spots) / (1.0*all_spots)) < 0.3:
            days_left_to_apply = 3

        if starting_day - self.today < datetime.timedelta(days = 3) and free_spots <= 3:
            days_left_to_apply = 1

        deadline = self.today + datetime.timedelta(days=days_left_to_apply)

        if deadline > starting_day:
            deadline = starting_day + datetime.timedelta(days=-1)

        if deadline < self.today:
            deadline = self.today + datetime.timedelta(days=1)

        return deadline.__str__()

    @stacktrace
    def get_date_description(self, course_data):
        date_list = []
        date_list.append(course_data["ElsoAlkalom"][:10])
        date_list.append(course_data["N2Alkalom"][:10])
        date_list.append(course_data["N3Alkalom"][:10])
        date_list.append(course_data["N4Alkalom"][:10])
        date_list.append(course_data["N5Alkalom"][:10])
        date_list.append(course_data["N6Alkalom"][:10])
        date_list.append(course_data["N7Alkalom"][:10])
        date_list.append(course_data["N8Alkalom"][:10])
        date_list.append(course_data["N9Alkalom"][:10])
        date_list.append(course_data["N10Alkalom"][:10])
        if course_data["N1SzunetOpcionalis"] != "":
            date_list.append("{} - {}".format(course_data["N1SzunetOpcionalis"][:10], "szünet"))
        if course_data["N2SzunetOpcionalis"] != "":
            date_list.append("{} - {}".format(course_data["N2SzunetOpcionalis"][:10], "szünet"))
        if course_data["N3SzunetOpcionalis"] != "":
            date_list.append("{} - {}".format(course_data["N3SzunetOpcionalis"][:10], "szünet"))

        date_list.sort()

        return_string = "   - " + "\n   - ".join(date_list)

        trace("JOINED STRING:\n{}".format(return_string))

        return return_string

    @stacktrace
    def raise_task(
            self,
            project_id,
            comment,
            deadline,
            userid = ""):
        """
        Creates a new task in teh CRM ssytem with the given details
        """

        self.command_handler.get_json_array_for_command(
            self.command_mapper.raise_task(project_id, comment, deadline, userid))

    @stacktrace
    def fill_student_data(self, student_data, course_data):
        data_to_update = {
                  "TanfolyamKodja": student_data["MelyikTanfolyamErdekli"],
                  "TanfolyamTipusa2": course_data["TanfolyamTipusa"],
                  "Helyszin2": course_data["Helyszin"],
                  "HelyszinReszletesLeiras": self.get_detailed_description(course_data["Helyszin"]),
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
                  "VeglegesitesiHatarido": self.get_application_deadline(course_data),
                  "Datumleirasok": self.get_date_description(course_data)
            }

        trace("DATA TO BE REPLACED:")
        pretty_print(data_to_update)

        self.command_handler.get_json_array_for_command(
            self.command_mapper.set_project_data(student_data["Id"], data_to_update))
