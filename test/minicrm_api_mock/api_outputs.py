# -*- coding: ISO-8859-2 -*-

API_OUTPUTS = {
u"places_schema": {
	u"description":u"Schema for modue 22, the places",
	u"command":u"curl -s --user FakeUserName:FakeApiKey \"https://r3.minicrm.hu/Api/R3/Schema/Project/22\"",
	u"response": {
		u"Id":u"Int",
		u"CategoryId": {
			u"20":u"Jelentkez\u00e9s",
			u"21":u"Tanfolyamok",
			u"22":u"Helysz\u00ednek",
			u"24":u"Kuponok",
			u"9":u"Sz\u00e1ml\u00e1z\u00f3",
			u"5":u"Info",
			u"23":u"HR"
			},
		u"ContactId":u"Int",
		u"BusinessId":u"Int",
		u"StatusId": {
			u"2759":u"Majd egyszer\/tal\u00e1n",
			u"2760":u"T\u00e1rgyal\u00e1s alatt",
			u"2761":u"Haszn\u00e1latban",
			u"2764":u"Megszak\u00edtva"
			},
		u"UserId": {
			u"56733":u"Rudolf \u00c1d\u00e1m",
			u"56032":u"Vogel S\u00e1ra"
			},
		u"Name":u"Text(512u",
		u"StatusUpdatedAt":u"DateTime",
		u"Deleted":u"Int",
		u"CreatedBy": {
			u"56733":u"Rudolf \u00c1d\u00e1m",
			u"56032":u"Vogel S\u00e1ra"
			},
		u"CreatedAt":u"DateTime",
		u"UpdatedBy": {
			u"56733":u"Rudolf \u00c1d\u00e1m",
			u"56032":u"Vogel S\u00e1ra"
			},
		u"UpdatedAt":u"DateTime",
		u"EgyediAzonosito":u"Text(1024u",
		u"ReszletesHelyszinleiras":u"Text(1024u"
		}
	},
u"places_list": {
	u"description":u"List of possible places of courses",
	u"command":u"curl -s --user FakeUserName:FakeApiKey \"https://r3.minicrm.hu/Api/R3/Project?CategoryId=22\"",
	u"response": {
		u"Count": 5,
		u"Results": {
			u"19": {
				u"Id": 19,
				u"Name":u"Pannon Kincst\u00e1r",
				u"Url":u"https:\/\/r3.minicrm.hu\/Api\/R3\/Project\/19",
				u"ContactId": 17,
				u"StatusId": 2761,
				u"UserId": 56733,
				u"Deleted": 0
				},
			u"20": {
				u"Id": 20,
				u"Name":u"Astoria",
				u"Url":u"https:\/\/r3.minicrm.hu\/Api\/R3\/Project\/20",
				u"ContactId": 18,
				u"StatusId": 2761,
				u"UserId": 56733,
				u"Deleted": 0
				},
			u"1096": {
				u"Id": 1096,
				u"Name":u"Offline Center",
				u"Url":u"https:\/\/r3.minicrm.hu\/Api\/R3\/Project\/1096",
				u"ContactId": 828,
				u"StatusId": 2761,
				u"UserId": 56733,
				u"Deleted": 0
				},
			u"2853": {
				u"Id": 2853,
				u"Name":u"Sigma Technology",
				u"Url":u"https:\/\/r3.minicrm.hu\/Api\/R3\/Project\/2853",
				u"ContactId": 1217,
				u"StatusId": 2761,
				u"UserId": 56733,
				u"Deleted": 0
				},
			u"745": {
				u"Id": 745,
				u"Name":u"Budapesti M\u0171vel\u0151d\u00e9si K\u00f6zpont",
				u"Url":u"https:\/\/r3.minicrm.hu\/Api\/R3\/Project\/745",
				u"ContactId": 630,
				u"StatusId": 2764,
				u"UserId": 56733,
				u"Deleted": 0
				}
			}
		}
	},
u"pannon_kincstar_data": {
	u"description":u"Detailed data of specific place called 'Pannon Kincstaru",
	u"command":u"curl -s --user FakeUserName:FakeApiKey \"https://r3.minicrm.hu/Api/R3/Project/19\"",
	u"response": {
		u"Id": 19,
		u"CategoryId": 22,
		u"ContactId": 17,
		u"StatusId":u"Haszn\u00e1latban",
		u"UserId":u"Rudolf \u00c1d\u00e1m",
		u"Name":u"Pannon Kincst\u00e1r",
		u"StatusUpdatedAt":u"2018-07-17 19:47:08",
		u"Deleted": 0,
		u"CreatedBy":u"Rudolf \u00c1d\u00e1m",
		u"CreatedAt":u"2018-06-17 16:32:50",
		u"UpdatedBy":u"Rudolf \u00c1d\u00e1m",
		u"UpdatedAt":u"2018-07-17 19:47:08",
		u"EgyediAzonosito":u"Pannon Kincst\u00e1r",
		u"ReszletesHelyszinleiras":u"A lot of detailes here..u"
		}
	},
u"empty_student_list": {
	u"description":u"",
	u"command":u"",
	u"response": {
		u"Count": 0,
		u"Results": {}
		}
	},


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
	},


u"course_list_for_nonexistent_course_code": {
	u"description":u"",
	u"command": u"https://r3.minicrm.hu/Api/R3/Project?TanfolyamBetujele=NONEXISTENT",
	u"response": {
		u"Count":0,
		u"Results":[]}
	}
}