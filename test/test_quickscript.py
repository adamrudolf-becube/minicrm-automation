from becube_crm_library import *
from test.minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "../api_info_real.json"

reload(sys)
sys.setdefaultencoding('utf8')


def quick_script(system_id, api_key):
    command_handler = CommandHandlerMock()
    command_handler.set_return_value(
        'curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Category"',
        'api_outputs/category_01.txt'
    )
    crm_data = CrmData(system_id, api_key, command_handler)
    crm_data.clean_info_level_kiment()
    crm_data.handle_waiting_list()
    crm_data.register_new_applicants()
    trace("QUICK SCRIPT TEST EXITED")


if __name__ == "__main__":
    system_id, api_key = load_api_info(API_INFO_JSON_FILE)
    quick_script(system_id, api_key)