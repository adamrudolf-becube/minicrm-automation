from becube_crm_library import *
from commandhandlermock import CommandHandlerMock

def quick_script():
    global system_id
    global api_key

    command_handler = CommandHandlerMock()
    crm_data = CrmData(system_id, api_key, command_handler)
    crm_data.clean_info_level_kiment()
    crm_data.handle_waiting_list()
    crm_data.register_new_applicants()
    trace("QUICK SCRIPT EXITED")