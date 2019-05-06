# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from __future__ import print_function

import datetime

from minicrm.tracing import stacktrace, trace


@stacktrace
def register_new_applicants(crm_data):
    """
    Lists all of the "Jelentkezett" students, and looks for their courses. Based on the course, it fills
    the needed data in the student's page.
    If the course is not found, it raises a task in CRM. (Not yet)
    Assumes that jelentkezok.new_students is up-to-date
    """

    student_list = crm_data.get_student_list_with_status("Jelentkezett")
    trace("LOOPING THROUGH STUDENTS WITH NEW STATUS")

    for student in student_list:
        crm_data.update_headcounts()
        student_data = crm_data.get_student(student)
        trace("COURSE FOR " + student_data["Name"] + " IS " + student_data["MelyikTanfolyamErdekli"])
        course_code = student_data["MelyikTanfolyamErdekli"]

        trace("\nGET COURSE DATA BASED ON COURSE CODE\n")

        course_data = crm_data.get_course_by_course_code(course_code)
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
                (crm_data.get_today() + datetime.timedelta(days=3)).__str__())
