# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function
import datetime
from commonfunctions import *

from tracing import stacktrace, trace


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
