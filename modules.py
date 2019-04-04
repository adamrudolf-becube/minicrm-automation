# -*- coding: utf-8 -*-
# MiniCRM automation
# Copyright Adam Rudolf, 2018
# BeCube programming school

from tracing import stacktrace, trace, pretty_print
from commandmapper import CommandMapper
from commonfunctions import *


class Module:
    """
    Represents a CRM module.

    Stores a collection of projects, and other module-level data, for example status codes
    """
    @stacktrace
    def __init__(self, module_id, system_id, api_key, command_handler):
        self.module_id = module_id
        self.api_key = api_key
        self.command_handler = command_handler
        self.system_id = system_id
        self.command_mapper = CommandMapper(system_id, api_key)
        self.available_values = self.query_available_values()
        self.project_list = self.query_project_list()

    @stacktrace
    def query_available_values(self):
        return self.command_handler.get_json_array_for_command(
                 self.command_mapper.get_schema_for_module_number(self.module_id))

    @stacktrace
    def query_project_list(self):
        return self.command_handler.get_json_array_for_command(
                 self.command_mapper.query_project_list(self.module_id))

    @stacktrace
    def query_project_list_with_status(self, status):
        trace(self.get_status_number_by_name(status))
        response = self.command_handler.get_json_array_for_command(
                        self.command_mapper.get_project_list_for_status(self.get_status_number_by_name(status)))
        if response["Count"] > 100:
            response_second_page = self.command_handler.get_json_array_for_command(
                        self.command_mapper.get_project_list_for_status_page1(self.get_status_number_by_name(status)))
            response["Results"] = dict(dict(response["Results"]), **dict(response_second_page["Results"]))

        return response

    @stacktrace
    def get_status_number_by_name(self, status_name):
        status_dictionary = self.available_values["StatusId"]
        return_value = get_key_from_value(status_dictionary, unicode(status_name, "utf-8"))
        trace("STATUS CODE FOR [{}] IS [{}]".format(status_name, return_value))
        return get_key_from_value(status_dictionary, unicode(status_name, "utf-8"))


class CourseList(Module):
    @stacktrace
    def get_course_by_course_code(self, course_code):

        # TODO https://r3.minicrm.hu/Api/R3/Project?TanfolyamBetujele=2019-4-E
        pretty_print(self.project_list)
        for course in self.project_list["Results"]:
            course_info = self.command_handler.get_json_array_for_command(
                 self.command_mapper.get_course(course))
            if course_info["TanfolyamBetujele"] == course_code:
                return course_info
        trace("COURSE NOT FOUND: [{}]".format(course_code))


class LocationList(Module):
    @stacktrace
    def get_location_by_name(self, location_name):
        for location in self.project_list["Results"]:
            location_info = self.command_handler.get_json_array_for_command(
                    self.command_mapper.get_location(location))
            trace("NAME CHECKED: "+location_info["Name"])
            if location_info["Name"] == location_name:
                return location_info
