# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function
import sys
import datetime
from commandmapper import CommandMapper
from commonfunctions import *
from modules import CustomerList, CourseList, LocationList

from tracing import stacktrace, trace, pretty_print

reload(sys)
sys.setdefaultencoding('utf8')


class CrmData:
    """
    Representation of high-level CRM data.
    Stores a colelction of modules as module objects.
    Responsible for bookkeeping of module ID-s, creating and deleting modules.
    """

    ###########################################################################
    #                                                                         #
    # Public methods                                                          #
    #                                                                         #
    ###########################################################################
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

    ###########################################################################
    #                                                                         #
    # Private methods                                                         #
    #                                                                         #
    ###########################################################################
    @stacktrace
    def ok_for_certification(self, student_data):
        visited_classes = len(student_data["Jelenlet"].split(", "))
        sent_homeworks = len(student_data["Hazi"].split(", "))
        return visited_classes >= 8 and sent_homeworks >= 8

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

    ###########################################################################
    #                                                                         #
    # Public methods                                                          #
    #                                                                         #
    ###########################################################################

    @stacktrace
    def register_new_applicants(self):
        """
        Lists all of the "Jelentkezett" students, and looks for their courses. Based on the course, it fills
        the needed data in the student's page.
        If the course is not found, it raises a task in CRM. (Not yet)
        Assumes that jelentkezok.new_students is up-to-date
        """
        self.jelentkezok.update_new_students()
        student_list = self.jelentkezok.new_students["Results"]
        trace("LOOPING THROUGH STUDENTS WITH NEW STATUS")

        for student in student_list:
            self.update_headcounts()
            student_data = self.get_project(student)
            trace("COURSE FOR " + student_data["Name"] + " IS " + student_data["MelyikTanfolyamErdekli"])
            course_code = student_data["MelyikTanfolyamErdekli"]

            trace("\nGET COURSE DATA BASED ON COURSE CODE\n")

            course_data = self.tanfolymok.get_course_by_course_code(course_code)
            if course_data:
                self.fill_student_data(student_data, course_data)
                self.send_initial_letter(student_data, course_data)
            else:
                self.raise_task(
                    student,
                    """Érvénytelen kurzuskód: [{}].

                    Nem tartozik nyitott kurzus ehhez a kódhoz, így a tanfolyamspecifikus adatokat nem sikerült kitölteni, és az INFO levelet a rendszer nem tudta kiküldeni. A jelentkező továbbra is "Jelentkezett" státuszban marad. Lehetséges okok:
                    - Az ehhez a kurzuskódhoz tartozó kurzus nem "Jelentkezés nyitva" státuszban van.
                    - A jelentkezési űrlapra hibásan lett beírva a kurzuskód.
                    - A tanfolyam adatlapjára hibásan lett beírva a kurzuskód.
                    - A jelentkezési űrlapon választható értékhez egyáltalán nem is tartozik tanfolyam.

                    TEENDŐ: a hiba okának megfelelően vagy
                    - módosítsd a jelentkezési űrlapot, és ezután manuálisan válaszd ki, "Melyik tanfolyam érdekli", vagy
                    - Hozd létre a hiányzó tanfolyamot, vagy ha létezik,
                    - állítsd "Jelentkezés nyitva" státuszra!
                    és várj, amíg a reendszer elvégzi a többit!

                    FIGYELEM!

                    Az adatok korrigálása után a rendszer automatiksuan megteszi a szokásos lépéseket, így ne küldj manuálisan INFO levelet, és ne változtasd meg a jelentkező státásuzát, mert az elronthatja a folyamatot!
                    """.format(student_data["MelyikTanfolyamErdekli"]),
                    (self.today + datetime.timedelta(days=3)).__str__())

    @stacktrace
    def clean_info_level_kiment(self):
        """
        Checks all students in "INFO levöl kiment" status, and
        - NOT DONE BY SCRIPT If billing info is filled, student gets to "Kurzus folyamatban" NOT DONE BY SCRIPT, autmated in MiniCRTM
        - If finalizing deadline -1 day is over, it sends a reminder
        - If finalizing deadline is over, it sends a reminder, raises a task for the responsible
        - If finalizing deadline + 1 ady is over, it sets student to "Nem valaszolt", and notifies responsible
        """

        self.jelentkezok.update_info_sent_out_students()
        student_list = self.jelentkezok.info_sent_out["Results"]
        trace("LOOPING THROUGH STUDENTS WITH INFO SENT OUT STATUS")

        for student in student_list:
            self.update_headcounts()
            trace("HEADCOUNT UPDATE DONE")
            student_data = self.get_project(student)
            trace("COURSE FOR " + student_data["Name"] + " IS " + student_data["MelyikTanfolyamErdekli"])

            update_data = {}

            levelkuldesek = student_data["Levelkuldesek"]
            levelkuldesek_old = levelkuldesek

            trace("STUDENT [" + student + "]([" + student_data["Name"] + "]) HAS NOT FINALIZED")

            deadline = datetime.datetime.strptime(student_data["VeglegesitesiHatarido"], "%Y-%m-%d %H:%M:%S")

            trace("TODAY: {}, DEADLINE: {}".format(self.today, deadline))

            if self.today >= deadline + datetime.timedelta(days=-1):
                trace("In first if")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Egy napod van jelentkezni")

            if self.today >= deadline:
                trace("In second if")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Ma kell jelentkezni")

            if self.today >= deadline + datetime.timedelta(days=+1):
                trace("In third if")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Toroltunk")
                update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("Nem jelzett vissza")

            if levelkuldesek != levelkuldesek_old:
                trace("CHANGE IN LEVELKULDESEK")
                update_data["Levelkuldesek"] = levelkuldesek
            else:
                trace("NO CHANGE IN LEVELKULDESEK")

            if update_data:
                self.command_handler.get_json_array_for_command(
                    self.command_mapper.set_project_data(student, update_data))

        self.update_headcounts()

    @stacktrace
    def handle_waiting_list(self):
        """
        Loops through all of the students in the waiting list and if there is
        free space in their course, it sends them the INFO letter and chenges their
        status. Also updates the headcounts of courses.
        """
        self.jelentkezok.update_waitin_list_students()
        student_list = self.jelentkezok.waiting_list_students["Results"]
        trace("LOOPING THROUGH STUDENTS ON WAITING LIST")

        student_ordered_list = []

        for student in student_list:
            trace("GETTING DETAILED DATA FOR SORTING")
            student_data = self.get_project(student)
            student_ordered_list.append(student_data)

        student_ordered_list.sort(key=lambda student_instance: student_instance["CreatedAt"])

        trace("ORDERED LIST IS")
        pretty_print(student_ordered_list)

        for student_data in student_ordered_list:
            trace("LOOPING THROUGH OERDERED LIST OF WAITING STUDENTS, CURRENTLY PROCESSING [{}]([{}])".
                  format(student_data["Id"], student_data["Name"]))
            self.update_headcounts()
            trace("COURSE FOR " + student_data["Name"] + " IS " + student_data["MelyikTanfolyamErdekli"])
            course_code = student_data["MelyikTanfolyamErdekli"]
            course_data = self.tanfolymok.get_course_by_course_code(course_code)

            is_there_free_spot = (course_data["MaximalisLetszam"] - course_data["AktualisLetszam"]) > 0

            if is_there_free_spot:
                update_data = {}

                trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO COURSE.".
                      format(course_data["AktualisLetszam"], course_data["MaximalisLetszam"]))

                update_data["Levelkuldesek"] = student_data[
                                                   "Levelkuldesek"] + ", Kezdő INFO levél, Felszabadult egy hely"
                update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("INFO levél kiment")

                trace("DATA TO UPDATE:")
                pretty_print(update_data)

                self.command_handler.get_json_array_for_command(
                    self.command_mapper.set_project_data(student_data["Id"], update_data))

        self.update_headcounts()

@stacktrace
def set_course_states(crm_data):
    """
    Loops through the courses and sets their statuses according to first and last date
    """
    open_course_list = crm_data.tanfolymok.query_project_list_with_status("Jelentkezés nyitva")["Results"]
    ongoing_course_list = crm_data.tanfolymok.query_project_list_with_status("Folyamatban")["Results"]
    freshly_finished = crm_data.tanfolymok.query_project_list_with_status("Frissen végzett")["Results"]

    course_list = dict(dict(open_course_list), **dict(ongoing_course_list))
    course_list = dict(dict(course_list), **dict(freshly_finished))

    for course in course_list:
        course_data = crm_data.get_project(course)

        pretty_print(course_data)

        update_data = {}

        try:
            if crm_data.today >= datetime.datetime.strptime(course_data["ElsoAlkalom"], "%Y-%m-%d %H:%M:%S"):
                trace("Set: ElsoAlkalom")
                update_data["StatusId"] = crm_data.tanfolymok.get_status_number_by_name("Folyamatban")
            if crm_data.today >= datetime.datetime.strptime(course_data["N10Alkalom"], "%Y-%m-%d %H:%M:%S"):
                trace("Set: N10Alkalom")
                update_data["StatusId"] = crm_data.tanfolymok.get_status_number_by_name("Frissen végzett")
            if crm_data.today >= datetime.datetime.strptime(course_data["N10Alkalom"],
                                                        "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=35):
                trace("Set: N10Alkalom + 35 nap")
                update_data["StatusId"] = crm_data.tanfolymok.get_status_number_by_name("Befejezett")
        except:
            trace("Missing date")

        if update_data:
            pretty_print(update_data)

            crm_data.command_handler.get_json_array_for_command(
                crm_data.command_mapper.set_project_data(course, update_data))
        else:
            trace("NO DATA TO UPDATE")

@stacktrace
def send_scheduled_emails(crm_data):
    """
    Loops through active students and spectators and sends them scheduled letters based on the dates and other conditions. Sets done students to "Elvégezte"
    """
    crm_data.jelentkezok.update_active_students()
    trace("ACTIVE STUDENTS")
    pretty_print(crm_data.jelentkezok.active_students["Results"])

    crm_data.jelentkezok.update_spectators()
    trace("SPECTATORS: ")
    pretty_print(crm_data.jelentkezok.spectators["Results"])

    student_list = dict(dict(crm_data.jelentkezok.active_students["Results"]),
                        **dict(crm_data.jelentkezok.spectators["Results"]))

    trace("STUDENT LIST: ")
    pretty_print(student_list)

    for student in student_list:
        student_data = crm_data.get_project(student)

        update_data = {}

        levelkuldesek = student_data["Levelkuldesek"]
        levelkuldesek_old = levelkuldesek

        if crm_data.today >= datetime.datetime.strptime(student_data["N1Alkalom"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N1Alkalom, NOW: {}")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "1. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "1. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N2Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N2Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "2. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "2. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N3Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N3Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "3. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "3. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N4Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N4Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "4. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "4. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N5Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N5Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "5. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "5. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N6Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N6Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "6. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "6. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N7Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N7Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "7. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "7. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N8Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N8Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "8. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "8. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N9Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N9Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "9. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "9. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N10Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
            trace("Set: N10Alkalom2")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges kezdő"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "10. alkalom - kezdő")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "10. alkalom - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N10Alkalom2"], "%Y-%m-%d %H:%M:%S"):
            trace("Set: N10Alkalom2 + 1 nap")
            if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Útravaló")
            elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam") or \
                    (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Útravaló - haladó")

        if crm_data.today >= datetime.datetime.strptime(student_data["N10Alkalom2"],
                                                    "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1):
            trace("Set: N10Alkalom2 + 2 nap")
            update_data["StatusId"] = crm_data.jelentkezok.get_status_number_by_name("Elvégezte")
            if (student_data["TanfolyamTipusa2"] == "Céges haladó"):
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Oklevél - haladó")
            if crm_data.ok_for_certification(student_data):
                trace("Set: Certified also")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Oklevél - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Oklevél - haladó")

        if student_data["N2SzunetOpcionalis2"] != "":
            if crm_data.today >= datetime.datetime.strptime(student_data["N2SzunetOpcionalis2"],
                                                        "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-2):
                trace("Set: N2SzunetOpcionalis2")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "1. szünet")
        if student_data["N2SzunetOpcionalis3"] != "":
            if crm_data.today >= datetime.datetime.strptime(student_data["N2SzunetOpcionalis3"],
                                                        "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-2):
                trace("Set: N2SzunetOpcionalis3")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "2. szünet")
        if student_data["N3SzunetOpcionalis2"] != "":
            if crm_data.today >= datetime.datetime.strptime(student_data["N3SzunetOpcionalis2"],
                                                        "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-2):
                trace("Set: N3SzunetOpcionalis2")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "3. szünet")

        if levelkuldesek != levelkuldesek_old:
            trace("CHANGE IN LEVELKULDESEK")
            update_data["Levelkuldesek"] = levelkuldesek
        else:
            trace("NO CHANGE IN LEVELKULDESEK")

        if update_data:
            crm_data.command_handler.get_json_array_for_command(
                crm_data.command_mapper.set_project_data(student, update_data))
