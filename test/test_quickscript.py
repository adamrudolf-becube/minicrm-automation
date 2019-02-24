from becube_crm_library import *
from minicrm_api_mock.commandhandlermock import CommandHandlerMock

API_INFO_JSON_FILE = "../api_info_real.json"

reload(sys)
sys.setdefaultencoding('utf8')


def quick_script(system_id, api_key):

    command_handler = CommandHandlerMock()
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Category"', 'api_outputs/category_01.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Schema/Project/20"','api_outputs/project_20_01.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?CategoryId=20"', 'api_outputs/category_id_20.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Schema/Project/21"', 'api_outputs/schema_project_21.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?CategoryId=21"', 'api_outputs/category_id_21.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?StatusId=2781"', 'api_outputs/status_id_2781.json')
    command_handler = set_participant_number_expectations(command_handler)
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/2601"', 'api_outputs/project_2601.json')
    command_handler = set_participant_number_expectations(command_handler)
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?StatusId=2750"', 'api_outputs/status_id_2750.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/2612"', 'api_outputs/project_2612.json')
    command_handler = set_participant_number_expectations(command_handler)
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/1164"', 'api_outputs/project_1164.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/1165"', 'api_outputs/project_2038_fake_course.json')
    command_handler = set_participant_number_expectations(command_handler)
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?StatusId=2741"', 'api_outputs/status_id_2741.json')

    crm_data = CrmData(system_id, api_key, command_handler, datetime.datetime(2019, 1, 21, 7, 30))
    crm_data.clean_info_level_kiment()
    crm_data.handle_waiting_list()
    crm_data.register_new_applicants()
    trace("QUICK SCRIPT TEST EXITED")

def set_participant_number_expectations(command_handler):

    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?StatusId=2753"', 'api_outputs/status_id_2753.json')

    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/2037"', 'api_outputs/project_2037.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja=2019-1-Q"', 'api_outputs/tanfolyam_kodja_2019_1_Q.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab -XPUT "https://r3.minicrm.hu/Api/R3/Project/2037" -d \'{"AktualisLetszam":6}\'', 'api_outputs/xput_2037.json')

    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/2041"', 'api_outputs/project_2041.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja=2019-1-U"', 'api_outputs/tanfolyam_kodja_2019_1_U.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab -XPUT "https://r3.minicrm.hu/Api/R3/Project/2041" -d \'{"AktualisLetszam":7}\'', 'api_outputs/xput_2041.json')

    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/2040"', 'api_outputs/project_2040.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja=2019-1-T"', 'api_outputs/tanfolyam_kodja_2019_1_T.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab -XPUT "https://r3.minicrm.hu/Api/R3/Project/2040" -d \'{"AktualisLetszam":1}\'', 'api_outputs/xput_2040.json')

    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/2039"', 'api_outputs/project_2039.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja=2019-1-S"', 'api_outputs/tanfolyam_kodja_2019_1_S.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab -XPUT "https://r3.minicrm.hu/Api/R3/Project/2039" -d \'{"AktualisLetszam":1}\'', 'api_outputs/xput_2039.json')

    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project/2038"', 'api_outputs/project_2038.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab "https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja=2019-1-R"', 'api_outputs/tanfolyam_kodja_2019_1_R.json')
    command_handler.expect_command('curl -s --user 38539:xhkjtSKq6v40BdfnsGIwrWLQ7OFiEDab -XPUT "https://r3.minicrm.hu/Api/R3/Project/2038" -d \'{"AktualisLetszam":10}\'', 'api_outputs/xput_2038.json')

    return command_handler


if __name__ == "__main__":
    system_id, api_key = load_api_info(API_INFO_JSON_FILE)
    quick_script(system_id, api_key)