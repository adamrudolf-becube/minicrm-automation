# -*- coding: ISO-8859-2 -*-

API_OUTPUTS = {
u"course_list_for_course_code": {
	u"description":u"",
	u"command":u"https://r3.minicrm.hu/Api/R3/Project?TanfolyamBetujele=2019-4-E",
	u"response": {
		u"Count":1,
		u"Results": {
			u"1164": {
				u"Id":1164,
				u"Name": u"2019-4-E",
				u"Url": u"https:\/\/r3.minicrm.hu\/Api\/R3\/Project\/3110",
				u"ContactId":1290,
				u"StatusId":2753,
				u"UserId":56733,
				u"Deleted":0
				}
			}
		}
	},

u"location_list_for_location_name": {
	u"description":u"",
	u"command":u"curl -s --user FakeUserName:FakeApiKey \"https://r3.minicrm.hu/Api/R3/Project?EgyediAzonosito=\"Pannon Kincstár\"\"",
	u"response": {
		u"Count":1,
		u"Results": {
			u"19": {
				u"Id":19,
				u"Name": u"Pannon Kincstár",
				u"Url": u"https:\/\/r3.minicrm.hu\/Api\/R3\/Project\/19",
				u"ContactId":1290,
				u"StatusId":2753,
				u"UserId":56733,
				u"Deleted":0
				}
			}
		}
	}
}