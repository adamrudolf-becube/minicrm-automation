"""
	u"description":u"List of all students who applied to 2019-1-Q",
	u"command":u"curl -s --user FakeUserName:FakeApiKey \"https://r3.minicrm.hu/Api/R3/Project?TanfolyamKodja=2019-1-Q\"",
"""
COURSE_CODE_IS_2019_1_Q = {
	u"response": {
		u"Count": 11,
		u"Results": {
			u"2131": {
				u"ContactId": 1043,
				u"Deleted": 0,
				u"Id": 2131,
				u"Name":u"Benkovich  \u00c1d\u00e1m",
				u"StatusId": 2749,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2131",
				u"UserId": 56733
				},
			u"2274": {
				u"ContactId": 1094,
				u"Deleted": 0,
				u"Id": 2274,
				u"Name":u"Szab\u00f3 Rich\u00e1rd",
				u"StatusId": 2782,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2274",
				u"UserId": 56733
				},
			u"2351": {
				u"ContactId": 1106,
				u"Deleted": 0,
				u"Id": 2351,
				u"Name":u"Bal\u00e1zs  Rozi",
				u"StatusId": 2783,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2351",
				u"UserId": 56733
				},
			u"2378": {
				u"BusinessId": 1119,
				u"ContactId": 1110,
				u"Deleted": 0,
				u"Id": 2378,
				u"Name":u"V\u00e9gh \u00c1d\u00e1m",
				u"StatusId": 2749,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2378",
				u"UserId": 56733
				},
			u"2384": {
				u"ContactId": 1113,
				u"Deleted": 0,
				u"Id": 2384,
				u"Name":u"Galambos Anna",
				u"StatusId": 2782,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2384",
				u"UserId": 56733
				},
			u"2434": {
				u"ContactId": 1128,
				u"Deleted": 0,
				u"Id": 2434,
				u"Name":u"Galambos Anna",
				u"StatusId": 2749,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2434",
				u"UserId": 56733
				},
			u"2496": {
				u"ContactId": 1149,
				u"Deleted": 0,
				u"Id": 2496,
				u"Name":u"Racz Daniel",
				u"StatusId": 2782,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2496",
				u"UserId": 56733
				},
			u"2523": {
				u"ContactId": 1150,
				u"Deleted": 0,
				u"Id": 2523,
				u"Name":u"Lad\u00e1nyi \u00c1d\u00e1m",
				u"StatusId": 2749,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2523",
				u"UserId": 56733
				},
			u"2524": {
				u"ContactId": 1158,
				u"Deleted": 0,
				u"Id": 2524,
				u"Name":u"Hank\u00f3 Zs\u00f3fia",
				u"StatusId": 2749,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2524",
				u"UserId": 56733
				},
			u"2549": {
				u"ContactId": 1161,
				u"Deleted": 0,
				u"Id": 2549,
				u"Name":u"Varga Attila",
				u"StatusId": 2782,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2549",
				u"UserId": 56733
				},
			u"2601": {
				u"ContactId": 1176,
				u"Deleted": 0,
				u"Id": 2601,
				u"Name":u"Moln\u00e1r P\u00e9ter",
				u"StatusId": 2781,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2601",
				u"UserId": 56733
				}
			}
		}
	}

ONE_STUDENT_IN_INFO_SENT_STATE = {
	u"description":u"List of students with status INFO_SENT. For simplify testing, this contains only 1 student nowu",
	u"command":u"curl -s --user FakeUserName:FakeApiKey \"https://r3.minicrm.hu/Api/R3/Project?StatusId=2781\"",
	u"response": {
		u"Count": 1,
		u"Results": {
			u"2601": {
				u"ContactId": 1176,
				u"Deleted": 0,
				u"Id": 2601,
				u"Name":u"Gipsz Jakab",
				u"StatusId": 2601,
				u"Url":u"https://r3.minicrm.hu/Api/R3/Project/2601",
				u"UserId": 56733
				}
			}
		}
	}