from becube_crm_library import *
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "api_info.json"

system_id = None
api_key = None

reload(sys)
sys.setdefaultencoding('utf8')


def quick_script():
    global system_id
    global api_key

    command_handler = CommandHandlerMock()
    crm_data = CrmData(system_id, api_key, command_handler)
    crm_data.clean_info_level_kiment()
    crm_data.handle_waiting_list()
    crm_data.register_new_applicants()
    trace("QUICK SCRIPT TEST EXITED")


if __name__ == "__main__":
    load_api_info()
    quick_script()