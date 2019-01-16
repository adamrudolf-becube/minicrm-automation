# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function
import sys
import json
import datetime

from command_handler import CommandHandler
from tracing import stacktrace, trace, pretty_print

API_INFO_JSON_FILE = "api_info.json"


system_id = None
api_key = None

reload(sys)
sys.setdefaultencoding('utf8')


def load_api_info():
    global system_id
    global api_key

    with open(API_INFO_JSON_FILE) as api_info_file:
        api_info = json.load(api_info_file)

    system_id = api_info[0]["username"]
    api_key = api_info[0]["api_key"]


def get_key_from_value(dictionary, dictionary_value):
    """
    Gets a python dictionary value and returns the corresponding index
    """
    keys = dictionary.keys()
    values = dictionary.values()
    return keys[values.index(dictionary_value)]

def truncate_comma_separated_string_list(input_string):
    if input_string[:2] == ', ':
        return input_string[2:]
    else:
        return input_string

def add_element_to_commasep_list(input_list, element):
    if (not element in input_list):
        out_list = truncate_comma_separated_string_list(input_list + ", " + element)
    else:
        out_list = input_list
    return out_list


class Module:
    """
    Represents a CRM module.

    Stores a collection of projects, and other module-level data, for example status codes
    """
    @stacktrace
    def __init__(self, module_id, system_id, api_key):
        self.module_id = module_id
        self.api_key = api_key
        self.system_id = system_id
        self.available_values = self.query_available_values()
        self.project_list = self.query_project_list()

    @stacktrace
    def query_available_values(self):
        return get_json_array_for_command(
                 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Schema/Project/{}"'.
                 format(self.system_id, self.api_key, self.module_id))

    @stacktrace
    def query_project_list(self):
        return get_json_array_for_command(
                 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?CategoryId={}"'.
                 format(self.system_id, self.api_key, self.module_id))

    @stacktrace
    def query_project_list_with_status(self, status):
        trace(self.get_status_number_by_name(status))
        return get_json_array_for_command(
                 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?StatusId={}"'.
                 format(self.system_id, self.api_key, self.get_status_number_by_name(status)))

    @stacktrace
    def get_status_number_by_name(self, status_name):
        status_dictionary = self.available_values["StatusId"]
        return_value = get_key_from_value(status_dictionary, unicode(status_name, "utf-8"))
        trace("STATUS CODE FOR [{}] IS [{}]".format(status_name, return_value))
        return get_key_from_value(status_dictionary, unicode(status_name, "utf-8"))



class CustomerList(Module):
    @stacktrace
    def update_new_students(self):
        self.new_students = self.query_project_list_with_status("Jelentkezett")

    @stacktrace
    def update_info_sent_out_students(self):
        self.info_sent_out = self.query_project_list_with_status("INFO levél kiment")

    @stacktrace
    def update_waitin_list_students(self):
        self.waiting_list_students = self.query_project_list_with_status("Várólistán van")

    @stacktrace
    def update_active_students(self):
        self.active_students = self.query_project_list_with_status("Kurzus folyamatban")

    @stacktrace
    def update_spectators(self):
        self.spectators = self.query_project_list_with_status("Megfigyelő")

    @stacktrace
    def get_checkbox_number_for_letter(self, letter_name):
        status_dictionary = self.available_values["Levelkuldesek"]
        return_value = get_key_from_value(status_dictionary, unicode(status_name, "utf-8"))
        trace("CHECKBOX CODE FOR [{}] IS [{}]".format(status_name, return_value))
        return get_key_from_value(status_dictionary, unicode(status_name, "utf-8"))


class CourseList(Module):
    @stacktrace
    def get_course_by_course_code(self, course_code):
        pretty_print(self.project_list)
        for course in self.project_list["Results"]:
            course_info = get_json_array_for_command(
                 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project/{}"'.
                 format(self.system_id, self.api_key, course))
            if course_info["TanfolyamBetujele"] == course_code:
                return course_info
        trace("COURSE NOT FOUND: [{}]".format(course_code))


class LocationList(Module):
    @stacktrace
    def get_location_by_name(self, location_name):
        for location in self.project_list["Results"]:
            location_info = get_json_array_for_command(
                 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project/{}"'.
                 format(self.system_id, self.api_key, location))
            trace("NAME CHECKED: "+location_info["Name"])
            if location_info["Name"] == location_name:
                return location_info
        trace("LOCATION NOT FOUND: ["+location_name+"]")


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
    def __init__(self, system_id, api_key, command_handler):
        """
        Sets the login data required by the API, collects information about existing modules, and even initializes some fo them
        """
        self.api_key = api_key
        self.system_id = system_id
        self.command_handler = command_handler
        self.set_modules_dictionary()
        self.jelentkezok = CustomerList(self.get_module_number_by_name("Jelentkezés"), self.system_id, self.api_key)
        self.tanfolymok = CourseList(self.get_module_number_by_name("Tanfolyamok"), self.system_id, self.api_key)

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
                    (datetime.datetime.now() + datetime.timedelta(days=3)).__str__(),
                    #crm_data.get_userid_by_name("Rudolf Dániel")
                    )

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

            trace("STUDENT ["+student+"](["+student_data["Name"]+"]) HAS NOT FINALIZED")

            deadline = datetime.datetime.strptime(student_data["VeglegesitesiHatarido"], "%Y-%m-%d %H:%M:%S")
            today = datetime.datetime.now()

            trace("TODAY: {}, DEADLINE: {}".format(today, deadline))

            if today >= deadline + datetime.timedelta(days=-1):
                trace("In first if")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Egy napod van jelentkezni")

            if today >= deadline:
                trace("In second if")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Ma kell jelentkezni")

            if today >= deadline + datetime.timedelta(days=+1):
                trace("In third if")
                levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Toroltunk")
                update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("Nem jelzett vissza")

            if levelkuldesek != levelkuldesek_old:
                trace("CHANGE IN LEVELKULDESEK")
                update_data["Levelkuldesek"] = levelkuldesek
            else:
                trace("NO CHANGE IN LEVELKULDESEK")

            if update_data:
                get_json_array_for_command(
                    'curl -s --user {}:{} -XPUT "https://r3.minicrm.hu/Api/R3/Project/{}" -d '.format(self.system_id, self.api_key, student)
                    +"'{}'".format(json.dumps(update_data, separators=(',',':'))))

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

                update_data["Levelkuldesek"] = truncate_comma_separated_string_list(
                                                   student_data["Levelkuldesek"] + ", Kezdő INFO levél, Felszabadult egy hely")
                update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("INFO levél kiment")

                trace("DATA TO UPDATE:")
                pretty_print(update_data)

                get_json_array_for_command(
                    'curl -s --user {}:{} -XPUT "https://r3.minicrm.hu/Api/R3/Project/{}" -d '.format(self.system_id, self.api_key, student_data["Id"])
                    +"'{}'".format(json.dumps(update_data, separators=(',',':'))))

        self.update_headcounts()

    @stacktrace
    def set_course_states(self):
        """
        Loops through the courses and sets their statuses according to first and last date
        """
        open_course_list = self.tanfolymok.query_project_list_with_status("Jelentkezés nyitva")["Results"]
        ongoing_course_list = self.tanfolymok.query_project_list_with_status("Folyamatban")["Results"]
        freshly_finished = self.tanfolymok.query_project_list_with_status("Frissen végzett")["Results"]

        course_list = dict(dict(open_course_list), **dict(ongoing_course_list))
        course_list = dict(dict(course_list), **dict(freshly_finished))

        for course in course_list:
            course_data = self.get_project(course)

            pretty_print(course_data)

            today = datetime.datetime.now()

            update_data = {}

            try:
                if today >= datetime.datetime.strptime(course_data["ElsoAlkalom"], "%Y-%m-%d %H:%M:%S"):
                    trace("Set: ElsoAlkalom")
                    update_data["StatusId"] = self.tanfolymok.get_status_number_by_name("Folyamatban")
                if today >= datetime.datetime.strptime(course_data["N10Alkalom"], "%Y-%m-%d %H:%M:%S"):
                    trace("Set: N10Alkalom")
                    update_data["StatusId"] = self.tanfolymok.get_status_number_by_name("Frissen végzett")
                if today >= datetime.datetime.strptime(course_data["N10Alkalom"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=35):
                    trace("Set: N10Alkalom + 35 nap")
                    update_data["StatusId"] = self.tanfolymok.get_status_number_by_name("Befejezett")
            except:
                trace("Missing date")

            if update_data:
                pretty_print(update_data)
                get_json_array_for_command(
                    'curl -s --user {}:{} -XPUT "https://r3.minicrm.hu/Api/R3/Project/{}" -d '.format(self.system_id, self.api_key, course)
                    +"'{}'".format(json.dumps(update_data, separators=(',',':'))))
            else:
                trace("NO DATA TO UPDATE")


    @stacktrace
    def send_scheduled_emails(self):
        """
        Loops through active students and spectators and sends them scheduled letters based on the dates and other conditions. Sets done students to "Elvégezte"
        """
        self.jelentkezok.update_active_students()
        trace("ACTIVE STUDENTS")
        pretty_print(self.jelentkezok.active_students["Results"])

        self.jelentkezok.update_spectators()
        trace("SPECTATORS: ")
        pretty_print(self.jelentkezok.spectators["Results"])

        student_list = dict(dict(self.jelentkezok.active_students["Results"]), **dict(self.jelentkezok.spectators["Results"]))

        trace("STUDENT LIST: ")
        pretty_print(student_list)

        today = datetime.datetime.now()

        for student in student_list:
            student_data = self.get_project(student)

            update_data = {}

            levelkuldesek = student_data["Levelkuldesek"]
            levelkuldesek_old = levelkuldesek
            today = datetime.datetime.now()

            if today >= datetime.datetime.strptime(student_data["N1Alkalom"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N1Alkalom, NOW: {}")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "1. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "1. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N2Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N2Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "2. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "2. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N3Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N3Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "3. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "3. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N4Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N4Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "4. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "4. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N5Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N5Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "5. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "5. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N6Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N6Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "6. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "6. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N7Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N7Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "7. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "7. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N8Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N8Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "8. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "8. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N9Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N9Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "9. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "9. alkalom - haladó")

            if today >= datetime.datetime.strptime(student_data["N10Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-3):
                trace("Set: N10Alkalom2")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "10. alkalom - kezdő")
                elif (student_data["TanfolyamTipusa2"] == "Haladó programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "10. alkalom - haladó")



            if today >= datetime.datetime.strptime(student_data["N10Alkalom2"], "%Y-%m-%d %H:%M:%S"):
                trace("Set: N10Alkalom2 + 1 nap")
                if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Útravaló")
                elif (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Útravaló - haladó")


            if today >= datetime.datetime.strptime(student_data["N10Alkalom2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1):
                trace("Set: N10Alkalom2 + 2 nap")
                update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("Elvégezte")
                if self.ok_for_certification(student_data):
                    trace("Set: Certified also")
                    if (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                        levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Oklevél - kezdő")
                    elif (student_data["TanfolyamTipusa2"] == "Kezdő programozó tanfolyam"):
                        levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Oklevél - haladó")

            if student_data["N2SzunetOpcionalis2"] != "":
                if today >= datetime.datetime.strptime(student_data["N2SzunetOpcionalis2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-2):
                    trace("Set: N2SzunetOpcionalis2")
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "1. szünet")
            if student_data["N2SzunetOpcionalis3"] != "":
                if today >= datetime.datetime.strptime(student_data["N2SzunetOpcionalis3"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-2):
                    trace("Set: N2SzunetOpcionalis3")
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "2. szünet")
            if student_data["N3SzunetOpcionalis2"] != "":
                if today >= datetime.datetime.strptime(student_data["N3SzunetOpcionalis2"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-2):
                    trace("Set: N3SzunetOpcionalis2")
                    levelkuldesek = add_element_to_commasep_list(levelkuldesek, "3. szünet")

            if levelkuldesek != levelkuldesek_old:
                trace("CHANGE IN LEVELKULDESEK")
                update_data["Levelkuldesek"] = levelkuldesek
            else:
                trace("NO CHANGE IN LEVELKULDESEK")

            if update_data:
                get_json_array_for_command(
                    'curl -s --user {}:{} -XPUT "https://r3.minicrm.hu/Api/R3/Project/{}" -d '.format(self.system_id, self.api_key, student)
                    +"'{}'".format(json.dumps(update_data, separators=(',',':'))))

    @stacktrace
    def generate_reports(self):
        #6. MUVELET: riportok elkeszitese
        #
        #Vegigmenni az osszes tanfolyamon (?)
        #
        #    minden honapra tanarok kulccsal dict
        #        ha stimmel, a datumot bepusholjuk
        #        
        #    ertesitest gereralni a reporttal
        pass

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

            update_data["Levelkuldesek"] = truncate_comma_separated_string_list(
                                               student_data["Levelkuldesek"] + ", Várólista")

            update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("Várólistán van")

        else:

            trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO COURSE.".
                format(course_data["AktualisLetszam"], course_data["MaximalisLetszam"]))

            trace("TYPE OF COURSE IS: [{}] ".format(course_data["TanfolyamTipusa"]))

            if (course_data["TanfolyamTipusa"] == "Kezdő programozó tanfolyam"):
                trace("IN KEZDO IF")
                update_data["Levelkuldesek"] = truncate_comma_separated_string_list(
                                                   student_data["Levelkuldesek"] + ", Kezdő INFO levél")

            elif (course_data["TanfolyamTipusa"] == "Haladó programozó tanfolyam"):
                trace("IN HALADO IF")
                update_data["Levelkuldesek"] = truncate_comma_separated_string_list(
                                                   student_data["Levelkuldesek"] + ", Haladó INFO levél")

            update_data["StatusId"] = self.jelentkezok.get_status_number_by_name("INFO levél kiment")


        trace("DATA TO UPDATE:")
        pretty_print(update_data)

        get_json_array_for_command(
            'curl -s --user {}:{} -XPUT "https://r3.minicrm.hu/Api/R3/Project/{}" -d '.format(self.system_id, self.api_key, student_data["Id"])
            +"'{}'".format(json.dumps(update_data, separators=(',',':'))))


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

            if course_data["StatusId"] == unicode("Jelentkezés nyitva", "utf-8"):
                trace("APPLICATION IS OPEN, CALCULATING HEADCOUNT")

                student_list = get_json_array_for_command(
                                 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja={}"'.
                                 format(self.system_id, self.api_key, course_code))["Results"]

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

                get_json_array_for_command(
                    'curl -s --user {}:{} -XPUT "https://r3.minicrm.hu/Api/R3/Project/{}" -d '.
                    format(self.system_id, self.api_key, course)
                    +"'{}'".format(json.dumps({"AktualisLetszam": count}, separators=(',',':'))))
            else:
                trace("APPLICATION IS NOT OPEN, DISCARD")

    @stacktrace
    def set_modules_dictionary(self):
        self.module_dict = get_json_array_for_command(
                             'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Category"'.
                             format(self.system_id, self.api_key))

    @stacktrace
    def get_project(self, id):
        return get_json_array_for_command(
                             'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project/{}"'.
                             format(self.system_id, self.api_key, id))

    @stacktrace
    def get_userid_by_name(self, user_name):
        user_dict = self.jelentkezok.available_values["UserId"]
        return user_dict.keys()[user_dict.values().index(unicode(user_name, "utf-8"))]

    @stacktrace
    def get_modules_dictionary(self):
        return self.module_dict

    @stacktrace
    def get_module_number_by_name(self, module_name):
        return self.module_dict.keys()[self.module_dict.values().index(unicode(module_name, "utf-8"))]

    @stacktrace
    def get_detailed_description(self, location):
        location_list = LocationList(self.get_module_number_by_name("Helyszínek"), self.system_id, self.api_key)

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
        today = datetime.datetime.now()
        free_spots = course_data["MaximalisLetszam"] - course_data["AktualisLetszam"]
        all_spots = course_data["MaximalisLetszam"]
        if all_spots == 0:
            all_spots = 1

        if starting_day - today < datetime.timedelta(days = 7) or ((1.0*free_spots) / (1.0*all_spots)) < 0.3:
            days_left_to_apply = 3

        if starting_day - today < datetime.timedelta(days = 3) and free_spots <= 3:
            days_left_to_apply = 1

        deadline = today + datetime.timedelta(days=days_left_to_apply)

        if deadline > starting_day:
            deadline = starting_day + datetime.timedelta(days=-1)

        if deadline < today:
            deadline = today + datetime.timedelta(days=1)

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

        task_data = {
            "ProjectId":project_id,
            "Status":"Open",
            "Comment":comment,
            "Deadline":deadline,
            "UserId":userid
        }

        get_json_array_for_command(
            "curl -XPUT https://{}:{}@r3.minicrm.hu/Api/R3/ToDo/ -d '{}'".
            format(self.system_id, self.api_key, json.dumps(task_data, separators=(',',':'))))

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

        get_json_array_for_command(
            'curl -s --user {}:{} -XPUT "https://r3.minicrm.hu/Api/R3/Project/{}" -d '.format(self.system_id, self.api_key, student_data["Id"])
            +"'{}'".format(json.dumps(data_to_update, separators=(',',':'))))


def quick_script():
    global system_id
    global api_key

    command_handler = CommandHandler()
    crm_data = CrmData(system_id, api_key, command_handler)
    crm_data.clean_info_level_kiment()
    crm_data.handle_waiting_list()
    crm_data.register_new_applicants()
    trace("QUICK SCRIPT EXITED")

def daily_script():
    global system_id
    global api_key

    command_handler = CommandHandler()
    crm_data = CrmData(system_id, api_key, command_handler)
    crm_data.send_scheduled_emails()
    crm_data.set_course_states()
    trace("DAILY SCRIPT EXITED")

def monthly_script():
    pass

def test_script():
    global system_id
    global api_key

    command_handler = CommandHandler()
    crm_data = CrmData(system_id, api_key, command_handler)
    crm_data.send_scheduled_emails()

if __name__ == "__main__":
    load_api_info()
    quick_script()
    #daily_script()
    #monthly_script()
    #test_script()