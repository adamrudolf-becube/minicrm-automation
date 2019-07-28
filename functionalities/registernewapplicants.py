# -*- coding: utf-8 -*-
"""
Registers newly applied students for the courses or puts them to the waiting list.

BeCube MiniCRM automation project.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import datetime

from minicrm.commonfunctions import add_element_to_commasep_list
from minicrm.tracing import pretty_print
from minicrm.tracing import stacktrace, trace
from subfunctionalities.enrollstudenttocourse import enroll_student_to_course

INFO_SENT_STATE = "INFO levél kiment"
WAITING_LIST_STATE = "Várólistán van"
APPLIED_STATE = "Jelentkezett"
STUDENT_NAME_FILED = "Name"
MAILS_TO_SEND_FIELD = "Levelkuldesek"
MAX_HEADCOUNT_FIELD = "MaximalisLetszam"
CURRENT_HEADCOUNT_FIELD = "AktualisLetszam"
STATUS_ID_FIELD = "StatusId"
STUDENT_ID_FIELD = "Id"
COURSE_TYPE_FIELD = "TanfolyamTipusa"
CHOSEN_COURSE_FIELD = "MelyikTanfolyamErdekli"
BEGINNER_COURSE_TYPE = "Kezdő programozó tanfolyam"
ADVANCED_COURSE_TYPE = "Haladó programozó tanfolyam"
WAITING_LIST_MAIL_NAME = "Várólista"
BEGINNER_INFO_MAIL_NAME = "Kezdő INFO levél"
ADVANCED_INFO_MAIL_NAME = "Haladó INFO levél"


@stacktrace
def put_student_to_waiting_list(crm_facade, student_data):
    """
    This function sends the waiting list email to the given student.

    This mail is information about that the student got to waiting list.

    :param crm_facade: instance of the CrmFacade class this functionality will use to communicate with a MiniCRM system.
    :type crm_facade: CrmFacade

    :param student_data: full JSON array of a student as stored in the MiniCRM system.
    :type student_data: dict

    :return: None
    """
    update_data = {}

    update_data[MAILS_TO_SEND_FIELD] = add_element_to_commasep_list(
        student_data[MAILS_TO_SEND_FIELD],
        WAITING_LIST_MAIL_NAME
    )

    update_data[STATUS_ID_FIELD] = crm_facade.get_student_status_number_by_name(WAITING_LIST_STATE)

    trace("DATA TO UPDATE:")
    pretty_print(update_data)

    crm_facade.set_student_data(student_data[STUDENT_ID_FIELD], update_data)


@stacktrace
def register_new_applicants(crm_facade):
    """
    This function loops through all of the newly applied students and registers them to the courses.

    The function lists all of the "Applied" ("Jelentkezett") students, and looks for their courses. Based on the course,
    it fills the needed data in the student's page. If the course is not found, it raises a task in MiniCRM system.

    The function

    - decides whether the student got into waiting list or to the course

    - decides what type of course the student applied

    - fetches course and location data and fills it into the student's data

    - sends the initial mail, which can be a beginner/advanced info mail or a waiting list mail

    - sets the status of the student

    - updates the headcounts of the courses and leaves a consistent state

    :param crm_facade: instance of the CrmFacade class this functionality will use to communicate with a MiniCRM system.

    :return: None
    """

    applied_students = crm_facade.get_student_list_with_status(APPLIED_STATE)
    trace("LOOPING THROUGH STUDENTS WITH NEW STATUS")

    for student in applied_students:
        crm_facade.update_headcounts()
        student_data = crm_facade.get_student(student)
        trace("COURSE FOR " + student_data[STUDENT_NAME_FILED] + " IS " + student_data[CHOSEN_COURSE_FIELD])
        course_code = student_data[CHOSEN_COURSE_FIELD]

        trace("\nGET COURSE DATA BASED ON COURSE CODE\n")

        course_data = crm_facade.get_course_by_course_code(course_code)

        if not course_data:
            crm_facade.raise_task(
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
                (crm_facade.get_today() + datetime.timedelta(days=3)).__str__())
            return

        crm_facade.copy_applied_course_to_course_code(student_data)

        trace("ACTUAL HEADCOUNT: [{}], MAXIMAL: [{}]. STUDENT GOT TO WAITING LIST.".
              format(course_data[CURRENT_HEADCOUNT_FIELD], course_data[MAX_HEADCOUNT_FIELD]))

        if course_data[CURRENT_HEADCOUNT_FIELD] >= course_data[MAX_HEADCOUNT_FIELD]:
            put_student_to_waiting_list(crm_facade, student_data)
        else:
            enroll_student_to_course(crm_facade, student_data, course_data)
