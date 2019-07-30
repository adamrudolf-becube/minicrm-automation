"""
Contains a function to update course dates for its students.

BeCube MiniCRM automation project.
"""
__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2019"

from minicrm.tracing import stacktrace


@stacktrace
def update_course_dates_for_all_students_for_that_course(crm_facade, course_code):
    """
    Gets all students for a given course, reads the dates of the course, and copies it to the student data of all.

    Sometimes course dates change even after many students have been enrolled to it. Students keep a copy of the
    course dates, but it doesn't get automatically updated, so an additional action is needed. This is for that.

    :param crm_facade: instance of the CrmFacade class this functionality will use to communicate with a MiniCRM system.
    :type crm_facade: CrmFacade

    :param course_code: code of the course you wish to update student dates, for example "2019-4-Q"
    :type course_code: str

    :return: None
    """

    course_data = crm_facade.get_course_by_course_code(course_code)
    student_list_for_course = crm_facade.get_student_list_for_course_code(course_code)

    for student in student_list_for_course:
        crm_facade.update_student_dates(student, course_data)
