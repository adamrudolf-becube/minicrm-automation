# -*- coding: utf-8 -*-
"""
This library defines abstract functionalities and returns a string for them. This can be used for having the
higher level logic independent from the concrete commands, but also to help phrase the exoectations in the tests
"""

import json


class MinicrmCommandFactory:
    def __init__(self, system_id, api_key):
        self.system_id = system_id
        self.api_key = api_key

    def get_schema_for_module_number(self, module_id):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Schema/Project/{}"'. \
                format(self.system_id, self.api_key, module_id)

    def query_project_list(self, module_id):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?CategoryId={}"'. \
               format(self.system_id, self.api_key, module_id)

    def get_project_list_for_status(self, status_number):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?StatusId={}"'. \
               format(self.system_id, self.api_key, status_number)

    def get_project_list_for_status_page1(self, status_number):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?StatusId={}&Page=1"'. \
               format(self.system_id, self.api_key, status_number)

    def get_student(self, student_id):
        return self.get_project(student_id)

    def get_location(self, location_id):
        return self.get_project(location_id)

    def get_course(self, course_id):
        return self.get_project(course_id)

    def get_course_list_by_course_code(self, course_code):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?TanfolyamBetujele={}"'.\
            format(self.system_id, self.api_key, course_code)

    def get_location_list_by_location_name(self, location_name):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?EgyediAzonosito=\"{}\""'.\
            format(self.system_id, self.api_key, location_name)

    def get_project(self, project_id):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project/{}"'. \
                 format(self.system_id, self.api_key, project_id)

    def set_project_data(self, project_id, data_json):
        return 'curl -s --user {}:{} -XPUT "https://r3.minicrm.hu/Api/R3/Project/{}" -d '. \
                   format(self.system_id, self.api_key, project_id) +\
                   "'{}'".format(json.dumps(data_json, separators=(',', ':')))

    def get_student_list_by_course_code(self, course_code):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja={}"'. \
                             format(self.system_id, self.api_key, course_code)

    def get_modul_dictionary(self):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Category"'.format(self.system_id, self.api_key)

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

        return "curl -XPUT https://{}:{}@r3.minicrm.hu/Api/R3/ToDo/ -d '{}'".\
                    format(self.system_id, self.api_key, json.dumps(task_data, separators=(',',':')))