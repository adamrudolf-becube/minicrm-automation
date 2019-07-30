"""
This library defines abstract functionalities and returns a string for them. This can be used for having the
higher level logic independent from the concrete commands, but also to help phrase the exoectations in the tests
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import json

from apirequest import ApiRequest, GET_METHOD, PUT_METHOD

_ = "WILDCARD"
"""
This is for testing purposes.

Can be used in place of every payload. If a request is created with a payload like this, it indicates for the testing
machinery that the test is expected with any payload. (Keeping in mind that the payload can have effect to the slogan
as well.) 
"""

CONTAINS = "CONTAINS"
"""
This is for testing purposes.

Defines a constant to indicate, we don't expect exact match in an expectation, we only would like to have a certain
list of elements in a commaseparated list included.
"""

EXCLUDES = "EXCLUDES"
"""
This is for testing purposes.

Defines a constant to indicate, we don't expect exact match in an expectation, we only would like to have a certain
list of elements in a commaseparated list excluded.
"""


def get_schema_for_module_number(module_id):
    """
    Creates an ApiRequest instance for getting the schema of a MiniCRM module.

    Examples can be: schema for students, schema for courses, or schema for locations. The schema is a JSON which
    contains the fields, and their possible values.

    Returns a GET request.

    :param module_id: ID number of the requested module.
    :type module_id: int

    :return: the encapsuladed API request for getting the schema for the given module.
    :rtype: ApiRequest
    """
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Schema/Project/{}".format(module_id),
        GET_METHOD,
        "Get schema for module {}".format(module_id)
    )


def get_project_list_for_status(status_number):
    """
    Creates an ApiRequest instance for getting the list of projects for the given status, for example getting a list
    of all courses in progress.

    Expects a status number.

    The API is paginated, this request will only return the first 100 projects.

    Returns a GET request.

    :param status_number: ID number of the requested status.
    :type status_number: int

    :return: the encapsuladed API request for
    :rtype: ApiRequest
    """

    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?StatusId={}".format(status_number),
        GET_METHOD,
        "Get project list for status {} (page 0)".format(status_number)
    )


def get_project_list_for_status_page1(status_number):
    """
    Creates an ApiRequest instance for getting the second page (page 1) of the list of projects for the given status,
    for example getting a list of all courses in progress.

    Expects a status number.

    The API is paginated, this request will only return the second 100 projects.

    Returns a GET request.

    :param status_number: ID number of the requested status.
    :type status_number: int

    :return: the encapsuladed API request for
    :rtype: ApiRequest
    """

    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?StatusId={}&Page=1".format(status_number),
        GET_METHOD,
        "Get project list for status {} (page 1)".format(status_number)
    )


def get_student(student_id):
    """
    Creates an ApiRequest instance for getting the full data of a specific student, based on their ID number.

    Note: this request will be the same as getting the data for any projects. Different functions have been created
    though to improve readability.

    Returns a GET request.

    :param student_id: ID number of the requested student.
    :type student_id: int

    :return: the encapsuladed API request for getting the fll data of a specific student.
    :rtype: ApiRequest
    """

    return get_project(student_id)


def get_location(location_id):
    """
    Creates an ApiRequest instance for getting the full data of a specific location, based on it's ID number.

    Note: this request will be the same as getting the data for any projects. Different functions have been created
    though to improve readability.

    Returns a GET request.

    :param location_id: ID number of the requested location.
    :type location_id: int

    :return: the encapsuladed API request for getting the fll data of a specific location.
    :rtype: ApiRequest
    """

    return get_project(location_id)


def get_course(course_id):
    """
    Creates an ApiRequest instance for getting the full data of a specific course, based on it's ID number.

    Note: this request will be the same as getting the data for any projects. Different functions have been created
    though to improve readability.

    Returns a GET request.

    :param course_id: ID number of the requested course.
    :type course_id: int

    :return: the encapsuladed API request for getting the fll data of a specific course.
    :rtype: ApiRequest
    """

    return get_project(course_id)


def get_course_list_by_course_code(course_code):
    """
    Creates an ApiRequest instance for getting a list of courses based on their course codes.

    Note: in our use cases the course code should be unique, this is not enforced by the MiniCRM system, and for the
    system it is only a regular text field. That is why the system is only able to return a list of courses for a given
    course code, although (if used well) this list will only contain one course.

    Returns a GET request.

    :param course_code: code of the requested course, for example "2019-6-D"
    :type course_code: str

    :return: the encapsuladed API request for getting a list of the courses which have the given course code.
    :rtype: ApiRequest
    """

    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?TanfolyamBetujele={}".format(course_code),
        GET_METHOD,
        "Get course list by course code: {}".format(course_code)
    )


def get_student_list_by_course_code(course_code):
    """
    """

    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja={}".format(course_code),
        GET_METHOD,
        "Get student list by course code: {}".format(course_code)
    )


def get_location_list_by_location_name(location_name):
    """
    Creates an ApiRequest instance for getting a list of locations based on their names.

    Note: in our use cases the location name should be unique, this is not enforced by the MiniCRM system, and for the
    system it is only a regular text field. That is why the system is only able to return a list of locations for a
    given location name, although (if used well) this list will only contain one location.

    Returns a GET request.

    :param location_name: name of the requested location, for example "Astoria"
    :type location_name: unicode

    :return: the encapsuladed API request for getting a list of the locations which have the given name.
    :rtype: ApiRequest
    """

    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?EgyediAzonosito={}".format(location_name),
        GET_METHOD,
        "Get location list by location name: {}".format(location_name)
    )


def get_project(project_id):
    """
    Creates an ApiRequest instance for getting the full data of any project (e.g. student, course, location).

    Returns a GET request.

    :param project_id: ID number of the requested project
    :type project_id: int

    :return: the encapsuladed API request for getting the full data of a project
    :rtype: ApiRequest
    """

    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project/{}".format(project_id),
        GET_METHOD,
        "Get project: {}".format(project_id)
    )


def set_project_data(project_id, data_json):
    """
    Creates an ApiRequest instance for modifying the data of an existing project (e.g. student, course or location).

    Returns a PUT request.

    Example usage:

    This is how you create a request to set student 1234 to waiting lis status:

    .. code-block:: python

      request = set_project_data(1234, {"StatusId": 2781})

    :param project_id: ID number of the project to be modified.
    :type project_id: int

    :param data_json: the dictionary of key-value pairs to be modified. You don't need to give the unchanged keys.
    :type data_json: dict

    :return: the encapsuladed API request for modifying the data of an existing project.
    :rtype: ApiRequest
    """

    if data_json == _:
        return ApiRequest(
            "https://r3.minicrm.hu/Api/R3/Project/{}".format(project_id),
            PUT_METHOD,
            "Set project data: {} to any data".format(project_id),
            _
        )
    else:
        return ApiRequest(
            "https://r3.minicrm.hu/Api/R3/Project/{}".format(project_id),
            PUT_METHOD,
            "Set project data: {} to {}".format(project_id, json.dumps(data_json)),
            data_json
        )


def get_student_list_by_course_code(course_code):
    """
    Creates an ApiRequest instance for getting a list of students based on their course codes.

    This returns a list of students attending the same course.

    Returns a GET request.

    :param course_code: code of the requested course, for example "2019-6-D"
    :type course_code: str

    :return: the encapsuladed API request for getting a list of the students which have the given course code.
    :rtype: ApiRequest
    """

    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja={}".format(course_code),
        GET_METHOD,
        "Get student list by course code: {}".format(course_code)
    )


def get_modul_dictionary():
    """
    Creates an ApiRequest instance for getting the list (dictionary) of modules existing in the MiniCRM system.

    The response is a dicionary where the keys are the ID numbers of the modules, and the values are the names of them.

    Returns a GET request.

    :return: the encapsuladed API request for getting the dictionary of the modules created in the MiniCRM system.
    :rtype: ApiRequest
    """

    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Category",
        GET_METHOD,
        "Get module dictionary"
    )


def raise_task(
        project_id,
        comment,
        deadline,
        userid=""):
    """
    Creates an ApiRequest instance for creating a new task in the MiniCRM system with the given details.

    In MiniCRM you can create a task on every project (student, course, location), and every task has a deadline, a
    text (also called comment) and a responsible, which is one of the users in MiniCRM.

    :param project_id: ID number of the project (student/course/location) you would like to raise the task on. The task
                       will be visible on the page of that project.
    :type project_id: int

    :param comment: the text you would like to show as the body of the task. Usually contains information what needs to
                    be done and how.
    :type comment: str

    :param deadline: deadline of the task. Has to be in the "%Y-%m-%d %H:%M:%S" format.
    :type deadline: str

    :param user_id: (optional) MiniCRM user who is responsible (assignee) for the task. Default so empty string, which
                    is valid from the MiniCRM point of view. If left empty, there will be no responsible for the task.
    :type user_id: int

    :return: the encapsuladed API request for
    :rtype: ApiRequest
    """

    if project_id == _:
        return ApiRequest(
            "https://{}:{}@r3.minicrm.hu/Api/R3/ToDo/",
            PUT_METHOD,
            "Raise task with any data",
            _
        )

    else:
        task_data = {
            "ProjectId": project_id,
            "Status": "Open",
            "Comment": comment,
            "Deadline": deadline,
            "UserId": userid
        }

        return ApiRequest(
            "https://{}:{}@r3.minicrm.hu/Api/R3/ToDo/",
            PUT_METHOD,
            "Raise task with data: {}".format(json.dumps(task_data)),
            task_data
        )
