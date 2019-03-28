"""
This library defines abstract functionalities and returns a string for them. This can be used for having the
higher level logic independent from the concrete commands, but also to help phrase the exoectations in the tests
"""

class CommandMapper:
    def __init__(self, system_id, api_key):
        self.system_id = system_id
        self.api_key = api_key

    def get_schema_for_module_number(self, module_id):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Schema/Project/{}"'. \
                format(self.system_id, self.api_key, module_id)

    def query_project_list(self, module_id):
        return 'curl -s --user {}:{} "https://r3.minicrm.hu/Api/R3/Project?CategoryId={}"'. \
               format(self.system_id, self.api_key, module_id)