# -*- coding: utf-8 -*-
"""
This library defines abstract functionalities and returns a string for them. This can be used for having the
higher level logic independent from the concrete commands, but also to help phrase the exoectations in the tests
"""

import json

from apirequest import ApiRequest, GET_METHOD, PUT_METHOD


_ = "WILDCARD"

def get_schema_for_module_number(module_id):
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Schema/Project/{}".format(module_id),
        GET_METHOD,
        "Get schema for module {}".format(module_id)
    )

def get_project_list_for_status(status_number):
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?StatusId={}".format(status_number),
        GET_METHOD,
        "Get project list for status {} (page 0)".format(status_number)
    )

def get_project_list_for_status_page1(status_number):
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?StatusId={}&Page=1".format(status_number),
        GET_METHOD,
        "Get project list for status {} (page 1)".format(status_number)
    )

def get_student(student_id):
    return get_project(student_id)

def get_location(location_id):
    return get_project(location_id)

def get_course(course_id):
    return get_project(course_id)

def get_course_list_by_course_code(course_code):
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?TanfolyamBetujele={}".format(course_code),
        GET_METHOD,
        "Get course list by course code: {}".format(course_code)
    )

def get_location_list_by_location_name(location_name):
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?EgyediAzonosito={}".format(location_name),
        GET_METHOD,
        "Get location list by location name: {}".format(location_name)
    )

def get_project(project_id):
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project/{}".format(project_id),
        GET_METHOD,
        "Get project: {}".format(project_id)
    )

def set_project_data(project_id, data_json):
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
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja={}".format(course_code),
        GET_METHOD,
        "Get student list by course code: {}".format(course_code)
    )

def get_modul_dictionary():
    return ApiRequest(
        "https://r3.minicrm.hu/Api/R3/Category",
        GET_METHOD,
        "Get module dictionary"
    )

def raise_task(
        project_id,
        comment,
        deadline,
        userid = ""):
    """
    Creates a new task in teh CRM ssytem with the given details
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
            "Raise task with any data".format(json.dumps(task_data)),
            task_data
        )