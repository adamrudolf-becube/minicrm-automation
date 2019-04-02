# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function
import datetime
from commonfunctions import *
from tracing import stacktrace, trace, pretty_print


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
            if ok_for_certification(student_data):
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

@stacktrace
def ok_for_certification(student_data):
    visited_classes = len(student_data["Jelenlet"].split(", "))
    sent_homeworks = len(student_data["Hazi"].split(", "))
    return visited_classes >= 8 and sent_homeworks >= 8