# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function
import sys
import datetime
from commonfunctions import *

from tracing import stacktrace, trace, pretty_print

reload(sys)
sys.setdefaultencoding('utf8')


@stacktrace
def register_new_applicants(crm_data):
    """
    Lists all of the "Jelentkezett" students, and looks for their courses. Based on the course, it fills
    the needed data in the student's page.
    If the course is not found, it raises a task in CRM. (Not yet)
    Assumes that jelentkezok.new_students is up-to-date
    """
    crm_data.jelentkezok.update_new_students()
    student_list = crm_data.jelentkezok.new_students["Results"]
    trace("LOOPING THROUGH STUDENTS WITH NEW STATUS")

    for student in student_list:
        crm_data.update_headcounts()
        student_data = crm_data.get_project(student)
        trace("COURSE FOR " + student_data["Name"] + " IS " + student_data["MelyikTanfolyamErdekli"])
        course_code = student_data["MelyikTanfolyamErdekli"]

        trace("\nGET COURSE DATA BASED ON COURSE CODE\n")

        course_data = crm_data.tanfolymok.get_course_by_course_code(course_code)
        if course_data:
            crm_data.fill_student_data(student_data, course_data)
            crm_data.send_initial_letter(student_data, course_data)
        else:
            crm_data.raise_task(
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
                (crm_data.today + datetime.timedelta(days=3)).__str__())

@stacktrace
def clean_info_level_kiment(crm_data):
    """
    Checks all students in "INFO levöl kiment" status, and
    - NOT DONE BY SCRIPT If billing info is filled, student gets to "Kurzus folyamatban" NOT DONE BY SCRIPT, autmated in MiniCRTM
    - If finalizing deadline -1 day is over, it sends a reminder
    - If finalizing deadline is over, it sends a reminder, raises a task for the responsible
    - If finalizing deadline + 1 ady is over, it sets student to "Nem valaszolt", and notifies responsible
    """

    crm_data.jelentkezok.update_info_sent_out_students()
    student_list = crm_data.jelentkezok.info_sent_out["Results"]
    trace("LOOPING THROUGH STUDENTS WITH INFO SENT OUT STATUS")

    for student in student_list:
        crm_data.update_headcounts()
        trace("HEADCOUNT UPDATE DONE")
        student_data = crm_data.get_project(student)
        trace("COURSE FOR " + student_data["Name"] + " IS " + student_data["MelyikTanfolyamErdekli"])

        update_data = {}

        levelkuldesek = student_data["Levelkuldesek"]
        levelkuldesek_old = levelkuldesek

        trace("STUDENT [" + student + "]([" + student_data["Name"] + "]) HAS NOT FINALIZED")

        deadline = datetime.datetime.strptime(student_data["VeglegesitesiHatarido"], "%Y-%m-%d %H:%M:%S")

        trace("TODAY: {}, DEADLINE: {}".format(crm_data.today, deadline))

        if crm_data.today >= deadline + datetime.timedelta(days=-1):
            trace("In first if")
            levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Egy napod van jelentkezni")

        if crm_data.today >= deadline:
            trace("In second if")
            levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Ma kell jelentkezni")

        if crm_data.today >= deadline + datetime.timedelta(days=+1):
            trace("In third if")
            levelkuldesek = add_element_to_commasep_list(levelkuldesek, "Toroltunk")
            update_data["StatusId"] = crm_data.jelentkezok.get_status_number_by_name("Nem jelzett vissza")

        if levelkuldesek != levelkuldesek_old:
            trace("CHANGE IN LEVELKULDESEK")
            update_data["Levelkuldesek"] = levelkuldesek
        else:
            trace("NO CHANGE IN LEVELKULDESEK")

        if update_data:
            crm_data.command_handler.get_json_array_for_command(
                crm_data.command_mapper.set_project_data(student, update_data))

    crm_data.update_headcounts()

@stacktrace
def handle_waiting_list(crm_data):
    """
    Loops through all of the students in the waiting list and if there is
    free space in their course, it sends them the INFO letter and chenges their
    status. Also updates the headcounts of courses.
    """
    crm_data.jelentkezok.update_waitin_list_students()
    student_list = crm_data.jelentkezok.waiting_list_students["Results"]
    trace("LOOPING THROUGH STUDENTS ON WAITING LIST")

    student_ordered_list = []

    for student in student_list:
        trace("GETTING DETAILED DATA FOR SORTING")
        student_data = crm_data.get_project(student)
        student_ordered_list.append(student_data)

    student_ordered_list.sort(key=lambda student_instance: student_instance["CreatedAt"])

    trace("ORDERED LIST IS")
    pretty_print(student_ordered_list)

    for student_data in student_ordered_list:
        trace("LOOPING THROUGH OERDERED LIST OF WAITING STUDENTS, CURRENTLY PROCESSING [{}]([{}])".
              format(student_data["Id"], student_data["Name"]))
        crm_data.update_headcounts()
        trace("COURSE FOR " + student_data["Name"] + " IS " + student_data["MelyikTanfolyamErdekli"])
        course_code = student_data["MelyikTanfolyamErdekli"]
        course_data = crm_data.tanfolymok.get_course_by_course_code(course_code)

        is_there_free_spot = (course_data["MaximalisLetszam"] - course_data["AktualisLetszam"]) > 0

        if is_there_free_spot:
            update_data = {}

            trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO COURSE.".
                  format(course_data["AktualisLetszam"], course_data["MaximalisLetszam"]))

            update_data["Levelkuldesek"] = student_data[
                                               "Levelkuldesek"] + ", Kezdő INFO levél, Felszabadult egy hely"
            update_data["StatusId"] = crm_data.jelentkezok.get_status_number_by_name("INFO levél kiment")

            trace("DATA TO UPDATE:")
            pretty_print(update_data)

            crm_data.command_handler.get_json_array_for_command(
                crm_data.command_mapper.set_project_data(student_data["Id"], update_data))

    crm_data.update_headcounts()

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
