# BeCube MiniCRM automation script system

*Magyar leírásért kattints 
[ide](#becube-minicrm-automatizációs-szkriptrendszer-magyar-nyelvű-dokumentáció)! 
/ For Hungarian description, click
[here](#becube-minicrm-automatizációs-szkriptrendszer-magyar-nyelvű-dokumentáció)!*

**Note:** the API reference is [here](http://becube.hu/minicrm-documentation/).

## Description

### What is this thing

Me, Adam Rudolf run a little programming school in Hungary, called
[BeCube](https://www.becube.hu). BeCube uses a CRM (Customer
Relationship Management) software called [MiniCRM](https://www.minicrm.io/) by MiniCRM Zrt.
to store information about our customers,
teachers, courses, locations, invoicing and e-mailing.

Although MiniCRM provides a list of features to automate processes
related to organizing courses and manage the lifecycle of students, a
lot of customization is needed to fulfill needs of BeCube.

This project contains the script system, which communicates with the
MiniCRM system through it's [REST API](https://en.wikipedia.org/wiki/Representational_state_transfer) to automate processes. The
scripts work quasi as an additional user of MiniCRM who can read and
modify data.

### Why is it public

BeCube is a programming school. We teach the basic principles of
programming using Python. We thought that why not expose this code to
our students, and to the public.

If we teach coding, and do coding, we should show our students what code
we are writing to be the example we think is good.   

This principle is also called [dog fooding](https://en.wikipedia.org/wiki/Eating_your_own_dog_food).

## Principles

### Not storing information

The script system should never store any information it fetches from
the server (i.e. the MiniCRM system). It has multiple purposes:

* **Single source of truth** - the information is always stored in
MiniCRM, so it can be used as the single source of truth. Double storing
could cause inconsistencies, and more complex logic. Note that some data
can be temporarily stored in the memory for caching purposes. This data
is never written to the hard disk, and is never stored for more than the
scope of a function.

* **Information security** - in whatever machine this code is running,
it's simpler to care about information security, because the machine is
not storing information.
 
* **Server independency** - the script doesn't remember what it did last
time. What matters is only what happens in the current run. This gives
us more independency: we can change the machine for running this code
any time. The current machine can even explode, loosing everything on
it, we can immediately start running the code from another machine.
 
* **Consistency** - the script doesn't change the state of the machine
it's running on. This means that the script can die mid-run, we can
start it again without any cleanup or other preparation.

### Independent runs - can be run any time and repeatedly

These scripts should never leave the system in inconsistent state.

A run mustn't depend on a previous run.

A run of this script mustn't affect any of the later runs *directly*.
(The run depends on the state of the CRM system, and also changes the
state of the CRM system, so indirectly running a script can cause
changes in the next run.) 

If the script is run very frequently for testing purposes, it should not
cause problem.

If the script is not run for a while, it shouldn't cause a problem.

### Partiality - can be run partially and then run again

If the script dies mid-run, it should be able to be started over from
the beginning and not causing problems.

If only specific features are executed, it shouldn't cause a problem.

### Independency from server - can be run from anywhere

The MiniCRM system should not know about the server which runs these
scripts.

The MiniCRM system should not expect these scripts to be run.

It ensures that skipping or repeating these scripts are not a problem,
and also that the server can be changed without any additional
consideration. 
  
## Code quality

The code should always comply with these rules:

* **Clean code** - follow principles of [Rober C. Martin's Clean Code](https://cleancoders.com/).
We have to understand the Clean Code principles. We have to know why we
are following them, we have to know when to break them, and we have to
know why to break them.
 
* **Design patterns kept in mind** - we have to be aware of the commonly
used [design patterns](https://en.wikipedia.org/wiki/Software_design_pattern), and find the situations where they fit naturally.
If there is a standard way of doing something, we have to do it in that
standard way, but don't overuse design patterns if they don't fit.
Examples: we use the [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern) to inject the [RequestHandler](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.requesthandler) to
the [CrmFacade](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.crmfacade) instance to be able to use it with a mock for testing. We
also use [the Facade Pattern](https://en.wikipedia.org/wiki/Facade_pattern) for hiding the complexity of request
handling, creation of requests and additional logic from the users. But
we also use a factory module for request creation, which is not
following the traditional [Factory Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern). 

* **PEP-8 is followed** - we follow [the official Python styling
guidelines](https://www.python.org/dev/peps/pep-0008/) whenever we don't have explicit and understood reason why not
to. 

* **Nicely tested**
    * We use automated tests in different levels with nicely used
    mocking
    * We measure and control the test coverage. We don't use coverage as
    a goal, but as a tool to detect untested features or dead code.
    Whenever we have uncovered code, that is marked explicitly and we
    have a good reason for that.
    
* **Version controlled in a very nice manner** - code is kept in [Git](https://git-scm.com/). We
use small commits, split by feature, with understandable and transparent
commit messages. We use Git to make development easier, safer and faster
on long term. Version control also makes it easier to synchronize with
the production server.   

* **Data is separated from code.**
    * API data is stored in a separate file. Real key is not included in
    repo.
    * Example JSON data for tests are stored in separate files.
    * API data can be changed without touching the code and code
    doesn't know the API data.
    
* **Nicely documented**
    * The basic principles, high level code structure and pedagogic 
    description is stored in the README.md (this document). The rule of
    thumb is that the project should be understood by reading this, but
    everything which changes with code updates shouldn't be here.  
    * The low level functionality, implementation details are documented
    with inline doc comments in the code. This is compiled to an API
    documentation HTML by automated documentation tool. Every
    implementation detail should be documented here. If you need to
    understand and/or use the code, you have to read this and not the
    README. The API documentation can be found [here](http://becube.hu/minicrm-documentation/).


## Technical aspects

For historical reasons, the code is being run on a server where we have
no full control. Therefore we need to align with the not always
up-to-date versions of Python and modules. This is the reason we use
things, which you might find obsolete. 

* Code is written in Pyhton 2.7.9
* Main modules we use:
    * pip 10.0.1
    * For handling API requests we use [requests](https://realpython.com/python-requests/) 2.21.0
* We use unittest for automatic test runs, with [nose](https://nose.readthedocs.io/en/latest/) (1.3.7) for test
discovery.
* For test coverage, we use [coverage](https://coverage.readthedocs.io/en/v4.5.x/) 4.5.2.
* We use [Sphinx](http://www.sphinx-doc.org/en/master/) 1.4.8 for generating html from inline doc comments. 
* On the server the scripts are automated by [cron](https://en.wikipedia.org/wiki/Cron). This is a builtin
daemon (a software which always runs in the background) in Linux
systems, and you can schedule regular jobs (like running a Python
program) in a file called crontab. Our crontab runs "quickscript.py"
every 15 minutes and "dailyscript.py" every day at 8:00. The scripts can
be run in any other manner of course, but this was kept in mind when
writing these scripts.

## Structure

We will have only a high-level, pedagogical description of the system.
For details, please refer to the [API documentation](http://becube.hu/minicrm-documentation/).

![Simplified class diagram](simplified_class_diagram.png "Simplified
class diagram of MiniCRM Automation Script System")

Details of this picture are explained in the following subsections. 

### Applications, or scripts

This script system contains applications, or scripts.
These are in the root folder, like quickscript.py and dailyscript.py.

These are the highest level elements of the system, these are the ones
the user needs to run directly.

### Functionalities

The Functionalities are the mid-level features, which are the smallest
units of standalone workflow, and they make sense from the business
point of view.

Examples are: handle waiting list, register new applicants, or send
scheduled mails.

These functionalities still don't make up a whole application, but one
application (script) can use and reuse them. The
reasonale behind this layer is to provide modularity for clarity and
reusability.

They are used in the applications as high level keyword-like commands.

These are contained by the functionalities package.

### CrmFacade

This is a concrete class, which contains the lower level functionalities
of the CRM system. These still contain some logic and make the system
more user friendly, but these functionalities are too small to make
sense standalone.

The CrmFacade hides the [ApiRequest](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.apirequest) class (not on the picture), the 
[crmrequestfactory](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.crmrequestfactory) module to create ApiRequest instances and the
[RequestHandler](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.requesthandler) to communicate with the MiniCRM system.

The RequestHandler is created by the application and is injected to the
CrmFacade through a parameter in the CrmFacade constructor. Similarly,
the application is the owner of the CrmFacade instance and provides it
to every application it uses. This principle is called [Dependency
Injection](https://en.wikipedia.org/wiki/Dependency_injection) and the goal is that the application has control on which
RequestHandler is used with what API data, so test can use the mock
[RequestHandlerMock](http://becube.hu/minicrm-documentation/requesthandlermock.html) instead of connecting to the real CRM server. 

The CrmFacade and all of the mentioned supporting classes are contained 
by the minicrm package.

### Other

Some modules, like [commonfunctions](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.commonfunctions) and [tracing](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.tracing) are not mentioned in the
picture. These contain free utility functions used commonly by different
entities.

## Other folders

There are some other folders. Not all of them are part of the
Git repo (so you might not see them), but are generated when running
the script, tests, or generating documentation.

* **requesthandlermock** - This is an alternative to the RequestHandler
for testing purposes. It doesn't communicate with the real MiniCRM
system, and can also check if the script system tried to send the
expected requests or not. For more details, refer to the [API
documentation](http://becube.hu/minicrm-documentation/).
* **build** - Only for generated content. In the current setup the html
API documentation generated by Sphinx, based on the doc comments are
stored here.
* **coverage-reports** - Only for generated content. Test coverage html
(and other) reports come here.
* **source** - Needed for the generated html API documentation.
* **venv** - Virtual environment for the development.

## Test descriptions

Tests are stored in the test package.

We have 3 levels of testing:
* **Unit test level** - local methods and single API calls.
* **Module test level** - single, standalone API functionalities, like
cleaning INFO_SENT and handle waiting list. This is maybe the most
important level of testing. This tests the Functionalities.
* **Use cases** (or system tests) - whole scripts (applications) are
tested. Not evey possible combination is tested, only typical or
important scenarios, because the functionalities have been tested
toroughly on the module test level.

The folder structure of test reflects this structure.

In the test descriptions we will follow the given-when-then approach.

*Note*: normally tests are not documented in the API documentation. We
broke this rule intentionally. Since we use this project also as an
educational project, we found it important to show the tests as well
with a good self describing documentation so you can even browse the
html documentation to understand the requirements of the code.

Every test file contains tests for one Python file in the production
code, and every testcase (class, which is a set of tests) contains tests
for one method/function and vica versa.

Note that a low level function is not tested separately if good
enough coverage is already reached on higher level.

If you need to see usecases for the code, we recommend you to read the
tests, as they "tell a story" with the expectations and test names.

## Contact

If you have any questions, don't hesitate to send it to info@becube.hu!

# BeCube MiniCRM automatizációs szkriptrendszer - magyar nyelvű dokumentáció

*This is the Hungarian version of the documentation and is only the 
direct translation of the document above this line. Is you prefer to
read in English, please scroll up to the top of the document, or click
[here](#becube-minicrm-automation-script-system). / Ez a magyar nyelvű dokumentáció. A dokumentum ezen része 
egyszerűen az eddigiek közvetlen fordítása. A dokumentum innentől
olvasva teljes értékű magyar nyelvű dokumentációként használható.* 

**Megjegyzés:** az API dokumentáció [itt](http://becube.hu/minicrm-documentation/) elérhető. Az API
dokumentáció csak angolul elérhető. 

## Leírás

### Mi ez az egész

Én, Rudolf Ádám, egy kis, [BeCube](https://www.becube.hu) nevű
programozóiskolát üzemeltetek Magyarországon. A BeCube-nál egy [MiniCRM](https://www.minicrm.hu/index_2/?utm_expid=.dw7uqwHoRq-YarJAqQEuQQ.1&utm_referrer=https%3A%2F%2Fwww.google.com%2F)
nevű CRM rendszert használunk a MiniCRM Zrt.-től, hogy számon tartsuk
a diákjainkat, tanárainkat, tanfolyamokat, helyszíneket, számlákat és
e-maileket.

Habár a MiniCRM több funkciót is nyújt a jelentkezési folyamat és egyéb
folyamatok automatizálására, sok testreszabás szükséges, hogy a BeCube
igényeinek megfeleljen.

Ez a projekt tartalmazza azt a szkriptrendszert, ami kommunikál a
MiniCRM rendszerrel a [REST API](https://hu.wikipedia.org/wiki/REST)-ján keresztül, hogy folyamatokat
automatizáljon. A szkriptek kvázi egy plusz MiniCRM felhasználóként
működnek, aki be tud jelentkezni, tudja olvasni és módosítani az
adatokat.

### Miért publikus?

A BeCube egy programozóiskola. A programozás alapvető elveit tanítjuk
Python nyelv használatával. Úgy gondoltuk, miért ne tegyük közzé ezt a
kódot a diákjaink, és mindenki számára!

Ha már kódolni tanítunk, és kódolunk is, meg kell mutatnunk a
diákjainknak a kódot, amit írunk, hogy ez legyen a példa, amit mi jónak
hiszünk.

Ezt az elvet angolul [dog fooding](https://en.wikipedia.org/wiki/Eating_your_own_dog_food)-nak
hívják (jobb fordítás hiáynában "kutyakajázás").

## Elvek

### Nem tárol információt

A szkriptrendszer soha nem tárolhat információt, amit a szervertól
(vagyis a MiniCRM rendszertől) kapott. Ennek több oka van:

* **Az igazság egyetlen forrása** - az információ mindig a MiniCRM
rendszerben van tárolva, így a szervert lehet az igazság egyetlen és
megbízható forrásának tekinteni. A dupla tárolás inkonzisztenciát és
bonyolultabb kezelési logikát eredményezhetne. Megjegyezzük, hogy a
memóriában valamennyi információt ideiglenesen eltárolunk. Ez azonban
sosem kerül mentésre a merevlemezen, és egy függvény hatókörénél nagyobb
kontxtusban sosem marad életben.

* **Információbiztonság** - akármilyen számítógépen is fut ez a kód,
sokkal egyszerűbb információbiztonsági szempontokat figyelembe venni,
mivel a gép nem tárol információt.

* **Szerverzfüggetlenség** - a szkript nem emlékszik, mit csinált a
legutóbbi futtatáskor. Csak az számít, hogy az aktuális futáskor mi
történik. Ez több függetlenséget biztosít számunkra: bármikor
lecserélhetjük a gépet, ami a kódot futtatja. A jelenlegi gép akár fel
is robbanhat, és elveszíthet minen információt, a kódot akár azonnal
elkezdhetjük futtatni egy másik számítógépről.

* **Konzisztencia** - a szkript nem változtatja meg a futtató gép
állapotát. Ez azt jelenti, hogy a szkript leállhat a futás közepén is,
mi akkor is minden előkészület nélkül újra tudjuk indítani.

### Független futások - akármikor és akárhányszor futtatható

Ezeknek a szkripteknek soha nem szabad a rendszert inkonzisztens
állapotan hagyni.

Egy futás soha nem függhet egy korábbi futástól.

Egy futás soha nem hathat ki *közvetlenül* egy későbbi futásra. (A
futás függ a MiniCRM rendszer jelenlegi állapotától, amit pedig 
befolyásol a szkript korábbi futása, szóval közvetetten egy futtatás
kihat a későbbi futtatásokra.)

Ha a szkriptet tesztelési célokból nagyon gykran futtatjuk, az nem
okozhat problémát.

Ha a szkriptet nem futtatjuk egy darabig, az nem okozhat problémát.

### Részlegesség - lehet részlegesen futtatni és újrafuttatni

Ha a szkript futás közben leáll, nem szabad, hogy gondot okozzon, ha
a részleges futás után elölről újraindítjuk.

Nem szabad, hogy gondot okozzon, ha csak bizonyos funkciókat futtatunk.

### Szerverfüggetlenség - akárhonnan lehet futtatni

A MiniCRM rendszernek nem szabad tudnia arról a számítógépről, ami 
ezeket a szkripteket futtatja.

A MiniCRM rendszer nem várhatja el, hogy futtasuk ezeket a szkripteket.

Ez biztosítja, hogy ha kihagyjuk, vagys éppen ismételjük ezeket a
szkripteket, az nem okoz gondot, és hogy a futtató számítógépet bármikor
lecserélhetjük mindenféle megfontolás nélkül.
  
## Kódminóség

A kódnak ezen elveknek kell megfelelnie:

* **Tiszta kód (Clean Code)** - követi [Rober C. Martin Clean Code
(Tiszta kód)](https://cleancoders.com/) című könyvében leírt elveket. Tudjuk, hogy miért
követjük az elveket, tudjuk, hogy mikor szegjük meg a szabályokat, 
és pontosan tudjuk, hogy miért szegjük meg a szabályoat.

* **A tervezési minták szem előtt tartása** - ismerjük a közismert
[tervezési mintákat](https://hu.wikipedia.org/wiki/Programtervez%C3%A9si_minta), és megtaláljuk azokat a helyeket, ahova ezek
természetes módon beillenek. Ha egy probléma megoldásának van elterjedt
módja, akkor azt használjuk, de nem használjuk túl a tervezési mintákat,
ha nem illenek oda. Itt leírunk néhány példát, viszont meggyőződésünk
szerint a minták (pattern-ök) angol nevét használjuk akkor is, ha van
elfogadott magyar fordítás, ugyanis a steril iskolai körülményeken és
néhány könyvön kívül soha nem használatosak a magyar elnevezések. Példa:  
a [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern)-t
(magyarul: [Stratégia Programtervezési Minta](https://hu.wikipedia.org/wiki/Strat%C3%A9gia_programtervez%C3%A9si_minta))
 használjuk, hogy a [RequestHandler](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.requesthandler)-t
beinjektáljuk a [CrmFacade](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.crmfacade)
példányba, hogy teszteléskoz 
használhassuk a [mockolt RequestHandler](http://becube.hu/minicrm-documentation/requesthandlermock.html)-t.
Szintén használjuk a
[Facade Pattern](https://en.wikipedia.org/wiki/Facade_pattern)-t 
(habár nem ajánljuk ezeket magyarul megtanulni, de [Homlokzat programtervezési minta
](https://hu.wikipedia.org/wiki/Homlokzat_programtervez%C3%A9si_minta)), hogy elrejtsük az API requestek kezelésének
részleteit, és némileg felhasználóbarátabbá tegyük a CRM rendszerrel
való kommunikációt. De egy factory modult is használunk, hogy API
requesteket készítsünk, de ez például nem követi a tradícionális
[Factory Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)-t ("[Gyártó minta](https://hu.wikipedia.org/wiki/Gy%C3%A1rt%C3%B3_met%C3%B3dus_programtervez%C3%A9si_minta)"). 
 
* **Követi a PEP-8 konvenciókat** - követjük [a hivatalos Python kód
formázási útmutatót](https://www.python.org/dev/peps/pep-0008/), amennyiben nincs explicit és jól megindokolt
okunk eltérni tőle.
 
* **Szépen tesztelt**
    * Automatizált teszteket használunk kölünböző absztrakciós
    szinteken, rendesen megírt mockokkal.
    * Mérjük és ellenőrizzük a teszt coverage-et (lefedettséget). De ezt
    nem használjuk számszerű célként, ehelyett egy eszköznek tekintjük,
    ami felfedhet teszteletlen funkcionalitást, vagy nem használt kódot.
    Bármilyen szándékosan nem tesztelt kód explicit módon jelölve van,
    és jól megalapozott okunk van rá, hogy ne teszteljük.
    
* **Verziókezelés szép módon** - a kódot [Gitben](https://git-scm.com/) tároljuk. Kis
kommitokat használunk, amit a funkcionalitás szerint osztunk fel,
érthető és transzparens commit message-ekkel. A Gitet nem csak kötelező
jelleggel használjuk, hanem úgy, hogy megkönnyítse a fejlesztőmunkát,
valamint hosszútávon biztinságosabbá és gyorsabbá tegye azt. A
verziókezelés arra is jó, hogy könnyebben szinkronizálhassuk a munkát
a fejlesztő és a futtató gépek között.

* **Az adatok a kódtól külön tárolódnak**
    * Az API adatok (bejelentkezési név és jelszó, azaz API kulcs) egy
    külön fáljban vannak tárolva. A valódi kulcsot nem töltjük föl a
    repóba.
    * A teszteléshez használt példa JSON válaszok (hamis válaszok a
    szervertől) egy külön mapparendszerben, külön fájlokban vannak
    tárolva.
    * Az API adatokat meg tudjuk változtatni anélkül, hogy a kódhoz
    hozzá kellene nyúlni.
    
* **Szépen dokumentált**
    * Az alapvető elvek, a magas szintű kódszerkezet, és didaktikus
    leírás megtalálható a README.md fájlban (ez a dokumentum). Az
    ökölszabály az, hogy ezt a dokumentumot elolvasva a projekt céljának
    és lényegének érthetővé kell válnia, semmilyen olyan technikai
    részletet nem kéne tartalmaznia, ami a kód írása közben változik.
    * Az alacsonyabb szintű funkcionalitást, az implementációs
    részleteket kódon belüli, ún. doc commentek tartalmazzák. Ezekből
    automatikusan generálunk HTML dokumentációt. Minden implementációs
    részletnek ebben a dokumentációban kell szerepelnie. Ha magát a
    kódot kell megértened, vagy használnod, ezt a dokumentumot kell
    böngészned, és nem a READE-t. Ez az API dokumentáció [itt](http://becube.hu/minicrm-documentation/)
    található.

## Technikai részletek

Történeti okokból a kódot olyan szerveren futtatjuk, amire nincs teljes
ráhatásunk. Emiatt alkalmazkodnunk kell a nem mindig naprakész Python
és modul verziókhoz. Emiatt használunk olyan dolgokat, amiket elavulthak
találhatsz.

* A kód Python 2.7.9-ben íródott
* A fontosabb modulok:
    * pip 10.0.1
    * Az API requestek kezelésére a [requests](https://realpython.com/python-requests/) modul 2.21.0 verzióját
    használjuk
* Az automatikus tesztekhez a unittest, a teszt
felderítéshez pedig [nose](https://nose.readthedocs.io/en/latest/) (1.3.7) modult használunk
* Teszt lefedettség: [coverage](https://coverage.readthedocs.io/en/v4.5.x/) 4.5.2.
* Az html API dokumentációt [Sphinx](http://www.sphinx-doc.org/en/master/) 1.4.8 segítségével generáljuk
* A szerveren a szkripteket a [cron](https://hu.wikipedia.org/wiki/Cron) Linux daemon automatizálja. Ez
egy beépített daemon (olyan szoftver, ami folyamatosan fut a háttérben),
amivel feladatokat lehet ütemezni egy crontab nevű fájl segíségével, ez
esetben például Python programok futtatását. A mi crontabunk a
"quickscript.py"-t 15 percenként futtatja, a "dailyscript.py"-t pedig
minden reggel 8:00-kor. A szkripteket természetesen bármilyen más módon
is lehet futtatni, de írásukkor ezt a fajta felhasználást tartottuk szem
előtt.

## Flépítés

Itt csak egy nagyjábóli, didaktikus leírását közöljük a rendszernek. A
részletekért nézd meg a (csak angolul elérhető) [API dokumentációt](http://becube.hu/minicrm-documentation/).

![Simplified class diagram](simplified_class_diagram.png "A MiniCRM
automatizációs szkriptrendszer egyszerűsített osztálydiagramja")

A diagram részleteit az alábbi alfejezetekben fejtjük ki. 

### Applications, avagy a szkriptek

A szkriptrenszerben vannak úgynevezett applikációk, vagy szkriptek.
Ezek a gyökérkönyvtárban vannak, mint a quickscript.py és a
dailyscript.py.

Ezek a rendszer legmagasabb szintű elemei, ezeket futtatja a felhasználó
közvetlenül.

### Funkcionalitások (Functionalities)

A Funkcionalitások középszintű feature-ök, amik a munkafolyamatok
legkisebb önállóan értelmezhető elemeit valósítják meg, vagyi a legkisebb
elemeknek számítanak, amiknek üzleti logika szempontjából ünállóan
futtatva még van értelme. 

Példák: várólista kezelése, új jelentkező regisztrálása, vagy ütemezett
emailek kiküldése.

Ezek a funkcionalitások még nem alkotnak teljes applikációt, de egy-egy
applikáció (szkript) használhatja és újrahasználhatja őket. Ennek az
absztrakciós rétegnek a célja a modlaritás biztosítása az átláthatóság
és újrahasznosíhatóság céljából.

Ezek a funkcionalitások magas szintű kulcsszavakként, avagy
parancsokként használhatóak a szkripekben.

Ezeket a functionalities package tartalmazza.

### CrmFacade

A CrmFacade egy konkrét osztály, ami a CRM rendszer alacsonyabb szintű
funkcióit tartalmazza. Még mindig megvalósít némi logikát, hogy
felhasználóbarátabbé tegye a rendszert, de ezek a funkcionalitások
túl kicsik, hogy önállóan értelmezhetőek legyenek a külső felhasználó
számára. 

A CrmFacade elrejti az [ApiRequest](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.apirequest) osztályt (nincs a képen), a
[crmrequestfactory](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.crmrequestfactory) modult aApiRequest példányoklegyártására, és a
[RequestHandler](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.requesthandler) példányt, ami kommunikál a MiniCRM rendszerrel.

A RequestHandlert az applikáció készíti el, és a CrmFacade példányba
a konstruktoron keresztül injektálja be. Hasonlóan, maga az applikáció
a tulajdonosa a CrmFacade példánynak, és adja azt oda minden
funkcionalitásnak. Ezt az elvet [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)-nek hívják 
(nem tudjuk hangsúlyozni, hogy milyen szörnyű ez lefordítva, de ha
magyarul olvasnál róla itt megteheted: 
"[A függőség befecskendezése](https://hu.wikipedia.org/wiki/A_f%C3%BCgg%C5%91s%C3%A9g_befecskendez%C3%A9se)"),
és ez esetben az a célja, hogy az applikációnak befolyása legyen arra,
hogy melyik RequestHandlert használja milyen API adatokkal, így a
tesztek dönthetnek úgy, hogy a mockolt 
[RequestHandlerMock](http://becube.hu/minicrm-documentation/requesthandlermock.html) osztályt
használják ahelyett, hogy valóban kapcsolódnának a CRM rendszerhez.

A CrmFacade és az összes itt említett segédosztály a minicrm package-ben
található meg.

### Egyéb

Néhány modul, például a 
[commonfunctions](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.commonfunctions) vagy a 
[tracing](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.tracing) nincs
megemlítve a képen. Ezek szabadonálló függvényeket tartalmaznak, amiket
különböző szoftverrészek megosztva használnak.

## Más mappák

Van néhány másik mappa is. Nem mindegyik része ennek a Git repónak
(vagyis lehet, hogy itt nem látod őket), viszont legenerálódnak, amikor
például futtatod a szkriptet, teszteket, vagy dokumentációt generálsz.

* **requesthandlermock** - Ez a
[RequestHandler](http://becube.hu/minicrm-documentation/minicrm.html#module-minicrm.requesthandler)
osztály alternatívája, amit tesztelésre használunk. Nem kommunikál a
valódi CRM rendszerrel, így nem is függ tőle, viszont tudja ellenőrizni,
hogy a szkriptek az előre beállított, elvárt API requesteket, vagy sem.
Több részletért nézd meg az [API dokumentációt](http://becube.hu/minicrm-documentation/)!
* **build** - Kizárólag generált tartalomnak. A jelenlegi beállításban
a Sphinx ide generálja a html API dokumentációt a doc commentek alapján.
* **coverage-reports** - Kizárólag generált tartalomnak. A teszt
lefedettség html (és más formátumú) eredményei kerülnek ide.
* **source** - A generált API dokumentációhoz szükséges.
* **venv** - A fejleszzés közben használt virtuális környezet fájljai.

## Teszt leírások

A teszteket a test package (mappa) tartalmazza.

3 absztrakciós szintet használunk teszteléskor:
* **Unit teszt szint** - helyi metódusok, és egyedülálló API hívások.
* **Modul teszt szint** - egyedülálló API funkcionalitások, mint
az INFO_LEVEL_KIMENT állapot "kipucolása", vagy a várólista kezelése.
Ez talán a tesztelés legfontosabb szintje. Ezek a fentebb említett
Funkcionalitásokat tesztelik.
* **Use case szint** (vagy rendszertesztek) - az egész szkripteket
(applikációkat) teszteli. Nem tesztelünk minden lehetséges kombinációt,
csak tipikusakat, mivel modul teszt szinten ezeket már lefedtük. Ez a
szint azt biztosítja, hogy a szkriptek a megfelelő funkcionalitásokat
használják a megfelelő sorrendben.

A tesztek mappaszerkezete is ezt a hármas felépítést követi.

A tesztek leírása a given-when-then (Adott-amikor-akkor) megközelítést
használja.

*Megjegyzés*: normális esetben a teszteket nem dokumentálják az API
dokumentációban, mivel nem képezik a végtermék részét. Mi szándékosan
törtük meg ezt a szokást. Mivel ez a projekt oktatási anyag is egyben,
fontosnak találtuk, hogy a teszteket is megmutassuk, és hogy azoknak
érthető, önmagyarázó dokumentációja legyen, hogy a html dokumentációt
böngészve is megérthesd a kóddal szemben támasztott követelményeket.
(A tesztek ugyanis a kód nyelvén megfogalmazott követelmények.)

Minden tesztfile egy Python file tartalmával szemben támaszt
követelményeket, és minden TestCase (teszteket tartalmazó osztály)
pontosan egy függvény/metódus követelményeit tartalmazza, valamint
fordítva.

Megjegyezzü, hogy egy alacsonyabb szintű függvény, vagy metódus nincs
külön tesztelve, ha megfelelő lefedettéget már elértük magasabb szinten,
és a tesztek túl redundánsak lennének.

Ha a kód használati eseteit szeretnéd látni, azt javasoljuk, olvasd a
teszteket, mert azok "elmesélnek egy történetet" a követlemények és a
tesztek nevei segítségével.

## Kapcsolat

Ha bármilyen kérdésed van, ne habozz írni az info@becube.hu címre!
