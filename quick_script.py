# -*- coding: utf-8 -*-
# MiniCRM automation

import becube_crm_library

system_id, api_key = becube_crm_library.load_api_info(becube_crm_library.API_INFO_JSON_FILE)
becube_crm_library.quick_script(system_id, api_key)