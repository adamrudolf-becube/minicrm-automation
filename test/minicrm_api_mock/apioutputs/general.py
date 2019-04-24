# -*- coding: ISO-8859-2 -*-

"""
List of MiniCRM modules (categories) with their ID numbers.

Example command: curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Category"
"""
MODULE_LIST = {
    u"response": {
        u"20":u"Jelentkezés",
        u"5":u"Info",
        u"9":u"Számlázu",
        u"21":u"Tanfolyamok",
        u"22":u"Helyszínek",
        u"24":u"Kuponok",
        u"23":u"HR"
    }
}

"""
description":u"Schema of project for module 20 (Jelentkezes). This is how a student is built up.
u"command":u"curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/20"
"""
SCHEMA_PROJECT_20_STUDENTS = {
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
			u"2796":u"\u00c9rdekl\u0151d\u0151",
			u"2741":u"Jelentkezett",
			u"2750":u"V\u00e1r\u00f3list\u00e1n van",
			u"2781":u"INFO lev\u00e9l kiment",
			u"2749":u"Kurzus folyamatban",
			u"2743":u"Elv\u00e9gezte",
			u"2784":u"Megfigyel\u0151",
			u"2745":u"Nem fizetett",
			u"2782":u"Nem jelzett vissza",
			u"2783":u"Lemondta",
			u"2786":u"Le\u00edratkozott"
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
		u"MelyikTanfolyamErdekli": {
			u"2358":u"2019-2-H-V",
			u"2360":u"2019-2-H-X",
			u"2758":u"2019-2-Y",
			u"2759":u"2019-2-Z",
			u"2763":u"SIGMA-01",
			u"2764":u"SIGMA-02"
			},
		u"TanfolyamKodja":u"Text(1024u",
		u"TeljesAr":u"Int",
		u"Fizetve":u"Int",
		u"Jelenlet": {
			u"1":u"1",
			u"2":u"2",
			u"4":u"3",
			u"8":u"4",
			u"16":u"5",
			u"32":u"6",
			u"64":u"7",
			u"128":u"8",
			u"256":u"9",
			u"512":u"10"
			},
		u"Hazi": {
			u"1":u"2",
			u"2":u"3",
			u"4":u"4",
			u"8":u"5",
			u"16":u"6",
			u"32":u"7",
			u"64":u"8",
			u"128":u"9"
			},
		u"Oklevel":u"File(10MBu",
		u"BaratiKedvezneny": {
			u"1":u"Hozom egy bar\u00e1tomat"
			},
		u"AkinekNeve":u"Text(1024u",
		u"EgyebKuponkod":u"Text(1024u",
		u"KuponJelentese":u"Text(1024u",
		u"EgyebKedvezmeny":u"Text(1024u",
		u"HagyomanyosAkciokBaratEarlyBirdAjandekTafnoylam":u"Int",
		u"ExtraAkciokIsmerosSzivessegStb":u"Int",
		u"Levelkuldesek": {
			u"1":u"V\u00e1r\u00f3lista",
			u"2":u"Kezd\u0151 INFO lev\u00e9l",
			u"4":u"Miket telep\u00edts\u00fcnk? - kezd\u0151",
			u"8":u"1. alkalom - kezd\u0151",
			u"16":u"2. alkalom - kezd\u0151",
			u"32":u"3. alkalom - kezd\u0151",
			u"64":u"4. alkalom - kezd\u0151",
			u"128":u"5. alkalom - kezd\u0151",
			u"256":u"6. alkalom - kezd\u0151",
			u"512":u"7. alkalom - kezd\u0151",
			u"1024":u"8. alkalom - kezd\u0151",
			u"2048":u"9. alkalom - kezd\u0151",
			u"4096":u"10. alkalom - kezd\u0151",
			u"8192":u"\u00datraval\u00f3",
			u"16384":u"Egy napod van jelentkezni",
			u"32768":u"Ma kell jelentkezni",
			u"65536":u"Toroltunk",
			u"131072":u"Felszabadult egy hely",
			u"262144":u"Oklev\u00e9l - kezd\u0151",
			u"524288":u"1. sz\u00fcnet",
			u"1048576":u"2. sz\u00fcnet",
			u"2097152":u"3. sz\u00fcnet",
			u"4194304":u"Halad\u00f3 INFO lev\u00e9l",
			u"8388608":u"Miket telep\u00edts\u00fcnk? - halad\u00f3",
			u"16777216":u"1. alkalom - halad\u00f3",
			u"33554432":u"2. alkalom - halad\u00f3",
			u"67108864":u"3. alkalom - halad\u00f3",
			u"134217728":u"4. alkalom - halad\u00f3",
			u"268435456":u"5. alkalom - halad\u00f3",
			u"536870912":u"6. alkalom - halad\u00f3",
			u"1073741824":u"7. alkalom - halad\u00f3",
			u"2147483648":u"8. alkalom - halad\u00f3",
			u"4294967296":u"9. alkalom - halad\u00f3",
			u"8589934592":u"10. alkalom - halad\u00f3",
			u"17179869184":u"\u00datraval\u00f3 - halad\u00f3",
			u"34359738368":u"Oklev\u00e9l - halad\u00f3"
			},
		u"TanfolyamTipusa2": {
			u"2497":u"Kezd\u0151 programoz\u00f3 tanfolyam",
			u"2498":u"Halad\u00f3 programoz\u00f3 tanfolyam",
			u"2499":u"Egynapos",
			u"2765":u"C\u00e9ges kezd\u0151",
			u"2766":u"C\u00e9ges halad\u00f3"
			},
		u"Helyszin2": {
			u"2501":u"Pannon Kincst\u00e1r",
			u"2502":u"Astoria",
			u"2714":u"Offline Center",
			u"2767":u"Sigma Technology"
			},
		u"HelyszinReszletesLeiras":u"Text(1024u",
		u"OrakIdopontja2":u"Text(1024u",
		u"VeglegesitesiHatarido":u"DateTime",
		u"N1Alkalom":u"DateTime",
		u"N2Alkalom2":u"DateTime",
		u"N3Alkalom2":u"DateTime",
		u"N4Alkalom2":u"DateTime",
		u"N5Alkalom2":u"DateTime",
		u"N6Alkalom2":u"DateTime",
		u"N7Alkalom2":u"DateTime",
		u"N8Alkalom2":u"DateTime",
		u"N9Alkalom2":u"DateTime",
		u"N10Alkalom2":u"DateTime",
		u"N2SzunetOpcionalis2":u"DateTime",
		u"N2SzunetOpcionalis3":u"DateTime",
		u"N3SzunetOpcionalis2":u"DateTime",
		u"Datumleirasok":u"Text(1024u",
		u"SzamlazasiCimMegadva": {
			u"1":u"Megadta a sz\u00e1ml\u00e1z\u00e1si c\u00edm\u00e9t"
			},
		u"OlyanVoltATanfolyamAmitVartal": {
			u"2385":u"Nem kaptam meg amit akartam",
			u"2386":u"Ilyesmire gondoltam",
			u"2387":u"Pont erre v\u00e1gytam",
			u"2388":u"Jobb volt mint sz\u00e1m\u00edtottam"
			},
		u"HaNemErreSzamitottalMiAzAmitVegulNemKaptalMeg":u"Text(1024u",
		u"MiTetszettATanfolyambanIrjValamiJot":u"Text(1024u",
		u"MinKelleneValtoztatnunkIrjValamiRosszat":u"Text(1024u",
		u"EredetilegMiertJelentkeztel": {
			u"2397":u"Csak \u00e9rdekelt  hogy mi ez az eg\u00e9sz (a programoz\u00e1su",
			u"2398":u"Szeretn\u00e9k m\u00e9lyebben tanulni \u00e9s j\u00f3 alapnak t\u0171nt",
			u"2399":u"Esetleg p\u00e1ly\u00e1t v\u00e1ltan\u00e9k",
			u"2400":u"Hogy a mostani munk\u00e1mat jobban \u00e9rtsem",
			u"2401":u"Egy\u00e9b"
			},
		u"Egyeb":u"Text(1024u",
		u"MireTervezedHasznalniAMegszerzettTudast":u"Text(1024u",
		u"HozzajarulszAVelemenyedReszeinekVagyEgeszenekKozlesere": {
			u"2545":u"Igen  teljes n\u00e9vvel",
			u"2546":u"Igen  keresztn\u00e9vvel",
			u"2547":u"Igen  n\u00e9v n\u00e9lk\u00fcl",
			u"2548":u"Nem"
			},
		u"MindentEgybevetveSzivesenJelentkeznelAFolytatasraIs": {
			u"2549":u"Igen",
			u"2550":u"Nem"
			},
		u"AValtozokrolSzoloResz": {
			u"2553":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2554":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2555":u"Megfelel\u0151  de unalmas volt",
			u"2556":u"T\u00fal neh\u00e9z volt"
			},
		u"AzIfWhile": {
			u"2557":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2558":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2559":u"Megfelel\u0151  de unalmas volt",
			u"2560":u"T\u00fal neh\u00e9z volt"
			},
		u"ATipusokrolIntStsBoolStbSzoloResz": {
			u"2561":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2562":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2563":u"Megfelel\u0151  de unalmas volt",
			u"2564":u"T\u00fal neh\u00e9z volt"
			},
		u"ACompiletinterpreter": {
			u"2565":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2566":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2567":u"Megfelel\u0151  de unalmas volt",
			u"2568":u"T\u00fal neh\u00e9z volt"
			},
		u"AzEgyszeruFuggvenyek": {
			u"2569":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2570":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2571":u"Megfelel\u0151  de unalmas volt",
			u"2572":u"T\u00fal neh\u00e9z volt"
			},
		u"AFuggvenyekParameterrelVisszateresiErtekkel": {
			u"2573":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2574":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2575":u"Megfelel\u0151  de unalmas volt",
			u"2576":u"T\u00fal neh\u00e9z volt"
			},
		u"AFileKezeles": {
			u"2577":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2578":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2579":u"Megfelel\u0151  de unalmas volt",
			u"2580":u"T\u00fal neh\u00e9z volt"
			},
		u"AListak": {
			u"2581":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2582":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2583":u"Megfelel\u0151  de unalmas volt",
			u"2584":u"T\u00fal neh\u00e9z volt"
			},
		u"ASzotarak": {
			u"2585":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2586":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2587":u"Megfelel\u0151  de unalmas volt",
			u"2588":u"T\u00fal neh\u00e9z volt"
			},
		u"APassBreakContinue": {
			u"2589":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2590":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2591":u"Megfelel\u0151  de unalmas volt",
			u"2592":u"T\u00fal neh\u00e9z volt"
			},
		u"AKivetelkezelesTryExpect": {
			u"2593":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2594":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2595":u"Megfelel\u0151  de unalmas volt",
			u"2596":u"T\u00fal neh\u00e9z volt"
			},
		u"ASajatModulImport": {
			u"2597":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2598":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2599":u"Megfelel\u0151  de unalmas volt",
			u"2600":u"T\u00fal neh\u00e9z volt"
			},
		u"EasyguiGombnyomogatosKattintgatos": {
			u"2601":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2602":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2603":u"Megfelel\u0151  de unalmas volt",
			u"2604":u"T\u00fal neh\u00e9z volt"
			},
		u"ArcadeMaszkalosLovagos": {
			u"2605":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2606":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2607":u"Megfelel\u0151  de unalmas volt",
			u"2608":u"T\u00fal neh\u00e9z volt"
			},
		u"OsztalyEsObjektumFogalma": {
			u"2726":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2727":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2728":u"Megfelel\u0151  de unalmas volt",
			u"2729":u"T\u00fal neh\u00e9z volt"
			},
		u"ASelfJelentese": {
			u"2730":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2731":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2732":u"Megfelel\u0151  de unalmas volt",
			u"2733":u"T\u00fal neh\u00e9z volt"
			},
		u"StatikusValtozok": {
			u"2734":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2735":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2736":u"Megfelel\u0151  de unalmas volt",
			u"2737":u"T\u00fal neh\u00e9z volt"
			},
		u"OroklodesSuperHasznalata": {
			u"2738":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2739":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2740":u"Megfelel\u0151  de unalmas volt",
			u"2741":u"T\u00fal neh\u00e9z volt"
			},
		u"OverridePolimorfizmus": {
			u"2742":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2743":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2744":u"Megfelel\u0151  de unalmas volt",
			u"2745":u"T\u00fal neh\u00e9z volt"
			},
		u"PrivatEsPublikusValtozokGetterSetter": {
			u"2746":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2747":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2748":u"Megfelel\u0151  de unalmas volt",
			u"2749":u"T\u00fal neh\u00e9z volt"
			},
		u"GitParancssorosHasznalata": {
			u"2750":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2751":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2752":u"Megfelel\u0151  de unalmas volt",
			u"2753":u"T\u00fal neh\u00e9z volt"
			},
		u"GithubHasznalata": {
			u"2754":u"T\u00fal k\u00f6nny\u0171 volt",
			u"2755":u"Megfelel\u0151 \u00e9s \u00e9lvezetes volt",
			u"2756":u"Megfelel\u0151  de unalmas volt",
			u"2757":u"T\u00fal neh\u00e9z volt"
			},
		u"TanarodMennyireVoltSzakmailagFelkeszult": {
			u"2609":u"1- egy\u00e1ltal\u00e1n nem",
			u"2610":u"2",
			u"2611":u"3",
			u"2612":u"4",
			u"2613":u"5 - teljesen"
			},
		u"TanarodMennyireMagyarazottKozerthetoen": {
			u"2614":u"1 - egy\u00e1ltal\u00e1n nem",
			u"2615":u"2",
			u"2616":u"3",
			u"2617":u"4",
			u"2618":u"5 - teljesen"
			},
		u"TanarodnakMennyireElvezetesAStilusa": {
			u"2619":u"1 - egy\u00e1ltal\u00e1n nem",
			u"2620":u"2",
			u"2621":u"3",
			u"2622":u"4",
			u"2623":u"5 - teljesen"
			},
		u"MegbizhatoanValaszoltEmailben": {
			u"2624":u"1 - egy\u00e1ltal\u00e1n nem",
			u"2625":u"2",
			u"2626":u"3",
			u"2627":u"4",
			u"2631":u"5 - teljesen"
			},
		u"AnonimMegjegyzesTanaroddalKapcsolatban":u"Text(1024u",
		u"MiertGondoltadMegMagad": {
			u"2673":u"Nem \u00e9rek r\u00e1",
			u"2674":u"T\u00fal dr\u00e1ga a tanfolyam",
			u"2675":u"Valamit f\u00e9lre\u00e9rtettem",
			u"2676":u"Egy\u00e9b"
			},
		u"MireLenneSzuksegHogyJelentkezz":u"Text(1024u"
		}
	}

"""
Schema of project for module 21 (Tanfolyamok). This is how a course built up"
Example command: curl -s --user FakeUserName:FakeApiKey "https://r3.minicrm.hu/Api/R3/Schema/Project/21"
"""
SCHEMA_PRPJECT_21_COURSES = {
	u"response": {
		u"AktualisLetszam":u"Int",
		u"BusinessId":u"Int",
		u"CategoryId": {
			u"20":u"Jelentkez\u00e9s",
			u"21":u"Tanfolyamok",
			u"22":u"Helysz\u00ednek",
			u"23":u"HR",
			u"24":u"Kuponok",
			u"5":u"Info",
			u"9":u"Sz\u00e1ml\u00e1z\u00f3"
			},
		u"ContactId":u"Int",
		u"CreatedAt":u"DateTime",
		u"CreatedBy": {
			u"56032":u"Vogel S\u00e1ra",
			u"56733":u"Rudolf \u00c1d\u00e1m"
			},
		u"Deleted":u"Int",
		u"ElsoAlkalom":u"DateTime",
		u"Frissitas": {
			u"1":u"Friss\u00edt\u00e9sre van sz\u00fcks\u00e9gu"
			},
		u"Helyszin": {
			u"2441":u"Pannon Kincst\u00e1r",
			u"2442":u"Astoria",
			u"2650":u"Budapesti M\u0171vel\u0151d\u00e9si K\u00f6zpont",
			u"2712":u"Offline Center"
			},
		u"Id":u"Int",
		u"MaximalisLetszam":u"Int",
		u"N10Alkalom":u"DateTime",
		u"N10AlkalomTanar":u"Text(1024u",
		u"N1AlkalomTanar":u"Text(1024u",
		u"N1ElmaradtIdopontOpcionalis":u"DateTime",
		u"N1SzunetOpcionalis":u"DateTime",
		u"N2Alkalom":u"DateTime",
		u"N2AlkalomTanar":u"Text(1024u",
		u"N2ElmaradtIdopontOpcionalis":u"DateTime",
		u"N2SzunetOpcionalis":u"DateTime",
		u"N3Alkalom":u"DateTime",
		u"N3AlkalomTanar":u"Text(1024u",
		u"N3SzunetOpcionalis":u"DateTime",
		u"N4Alkalom":u"DateTime",
		u"N4AlkalomTanar":u"Text(1024u",
		u"N5Alkalom":u"DateTime",
		u"N5AlkalomTanar":u"Text(1024u",
		u"N6Alkalom":u"DateTime",
		u"N6AlkalomTanar":u"Text(1024u",
		u"N7Alkalom":u"DateTime",
		u"N7AlkalomTanar":u"Text(1024u",
		u"N8Alkalom":u"DateTime",
		u"N8AlkalomTanar":u"Text(1024u",
		u"N9Alkalom":u"DateTime",
		u"N9AlkalomTanar":u"Text(1024u",
		u"Name":u"Text(512u",
		u"OrakIdopontja":u"Text(1024u",
		u"StatusId": {
			u"2752":u"Szervez\u00e9s alatt",
			u"2753":u"Jelentkez\u00e9s nyitva",
			u"2754":u"Befejezett",
			u"2756":u"Lef\u00fajva l\u00e9tsz\u00e1mhi\u00e1ny miatt",
			u"2757":u"Lef\u00fajva m\u00e1s okb\u00f3l",
			u"2758":u"Folyamatban",
			u"2797":u"Frissen v\u00e9gzett"
			},
		u"StatusUpdatedAt":u"DateTime",
		u"Tanar": {
			u"2491":u"B\u00e1n Marcell",
			u"2492":u"Papp M\u00e1ty\u00e1s",
			u"2493":u"Ferenczi Zsanett",
			u"2494":u"Kov\u00e1cs Gerg\u0151",
			u"2495":u"Rudolf D\u00e1niel",
			u"2651":u"D\u00e1niel P\u00e1l",
			u"2652":u"Farkas \u00c1mon",
			u"2653":u"Gr\u00f3f Attila",
			u"2654":u"Sipos D\u00e1vid",
			u"2655":u"Suh\u00e1nszki Norbert",
			u"2656":u"Schaum B\u00e9la",
			u"2657":u"Kun Szabolcs",
			u"2658":u"B\u00e9res Csan\u00e1d",
			u"2659":u"Bogn\u00e1r Kriszti\u00e1n",
			u"2660":u"D\u00e9nes Benj\u00e1min",
			u"2661":u"Szalai D\u00e1vid",
			u"2662":u"Sz\u00e9n\u00e9get\u0151 Gerg\u0151",
			u"2663":u"Forj\u00e1n Valentin",
			u"2664":u"Rudolf \u00c1d\u00e1m",
			u"2665":u"Pest Bal\u00e1zs",
			u"2711":u"Farkas M\u00e1t\u00e9"
			},
		u"TanfolyamBetujele":u"Text(1024u",
		u"TanfolyamTipusa": {
			u"2419":u"Kezd\u0151 programoz\u00f3 tanfolyam",
			u"2420":u"Halad\u00f3 programoz\u00f3 tanfolyam",
			u"2423":u"Egynapos"
			},
		u"UpdatedAt":u"DateTime",
		u"UpdatedBy": {
			u"56032":u"Vogel S\u00e1ra",
			u"56733":u"Rudolf \u00c1d\u00e1m"
			},
		u"UserId": {
			u"56032":u"Vogel S\u00e1ra",
			u"56733":u"Rudolf \u00c1d\u00e1m"
			}
		}
	}