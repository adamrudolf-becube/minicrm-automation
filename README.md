# BeCube MiniCRM automation script system

**Disclaimer**: this software is in production, but is currently under heavy refactoration. This includes (among many other things) writing this README. So this (although contains the truth) is heavily under construction. 

## Description

### What is this for

Me, Adam Rudolf run a little programming school in Hungary, called BeCube. BeCube uses a CRM (Customer Relationship Management) software called MiniCRM by MiniCRM Zrt. to store information about our customers, teachers, courses, locations, invoicing and e-mailing.

Although MiniCRM provides a list of features to automate processes related to organizing courses and manage the lifecycle of students, a lot of customization is needed to fulfill needs of BeCube.

This project contains the script system, which communicates with the MiniCRM system through it's REST API.

### Why is it public

BeCube is a programming school. We teach the basic principles of programming using Python. We thought that why not expose this code to our students, and to the public.   

## Principles

## Technical aspects

### Not storing information
### Independent runs - can be run any time and repeatedly
### Partiality - can be run partially and then run again
### Independency from server - can be run from anywhere
### MiniCRM application must be independent from it

TODO Can be run any time and be repeated any times. Can be stopped  

### Code quality

* Clean code
* Design patterns kept in mind
* PEP-8 is followed
* Nicely tested
    * Automated tests in different levels with nicely used mocking
    * Measured and controlled test coverage
* Version controlled in a very nice manner
* Data is separated from code.
    * API data is stored in a separate file. Real key is not included in repo
    * Example JSON data for tests are stored in separate files
Even good to syncronize with the production server
* Nicely documented
    * Here in this README
    * In the code with doc comments

## Structure

TODO: define english abstract state and field names

## Test sescriptions

We have 3 levels of testing:
* **Unit test level** - local methods and single API calls.
* **Module test level** - single, standalone API functionalities, like cleaning INFO_SENT and handle waiting list. This is maybe the most important level of testing.
* **Use cases** - whole scripts are tested. Not evey possible combination is tested, only typical or important scenarios.

In the test descriptions we will follow the given-when-then approach, except that the logic of the script is to query the system and modify it. The script's behavious only depends on the state of the system, and the script always initializes. Therefore actions in the CRM system are never triggers to any action, every trigger is that the script is being run. The "when" part therefore is excluded from the test descriptions.

### Use case description

#### Clean INFO_SENT

This loops through students in the given state. The action made on them is independent from the other students so in the tests it is enough to check every possibility with one student and check some examples with a set.

##### Student gave positive answer, make him/her active

**This is done by the MiniCRM framework, not by this script.**
    
* Given:
    * Student is in INFO_SENT state
    * Finalizing form has been sent
* Then:
    * Raise task to MiniCRM user to send invoice
    * Trigger What to install (miket telepitsunk) e-mail (can be done from the MiniCRM system's builtin automation features)
    * Set state to ACTIVE

##### Student did not finalize, deadline has not spent, but within 24 hours, send reminder

* Description
* Testname (slogan)
* Given:
    * Student is in INFO_SENT state
    * Finalizing form has not been sent
    * Deadline is greater than _today's date, but difference is smaller than 24 hours
* Then:
    * Trigger sending reminder e-mail
    * Create task for MiniCRM responsible

##### Student did not finalize, deadline has been spent, but not more then 24 hours ago, send reminder again and raise task to call student

* Description
* Testname (slogan)
* Given:
    * Student is in INFO_SENT state
    * Finalizing form has not been sent
    * Today is greater than deadline, and difference is not greater than 24 hours
* Then:
    * Trigger sending 2nd mail and create reminder
    * Create task for MiniCRM responsible

##### Student did not finalize, deadline has been spent more than 24 hours ago

* Description
* Testname (slogan)
* Given:
    * Student is in INFO_SENT state
    * Finalizing form has not been sent
    * Today is greater than deadline and difference is bigger than 24 hours
* Then:
    * Set state to DID_NOT_FINALIZE
    * Trigger sending e-mail about deleting him/her
    * Trigger raising task about deleting student and deleting invoice

##### Student did not finalize, but deadline is more then 1 day away, do nothing

* Description
* Testname (slogan)
* Given:
    * Student is in INFO_SENT state
    * Finalizing form has not been sent
    * Today is smaller than deadline and difference is not smaller than 24 hours
* Then:
    * Do nothing

#### Handle waiting list

##### If there is one student on waiting list, but there are free places, do nothing
##### If there are multiple students on waiting list, but there are free places, do nothing
##### If there is one student on waiting list, and there is one free place, put student to INFO_SENT
##### If there are multiple students on waiting list, and there is one free place, put the earlier student to INFO_SENT (check both ways)
##### If there are 2 students on the waiting list, and there are two free places, put both students to INFO_SENT
##### If there are 5 students on the waiting list, and there are two free places, put the earliest two students to INFO_SENT


#### Register new applicants

##### If there is a student in APPLIED status, and the headcount is less than the limit, put student to INFO_SENT status, and update headcounts
Also copy course data
##### If there is a student in APPLIED status, and the course doesn't exist, raise task with error message
##### If there is a student in APPLIED status, and the headcount is not less than the limit, put student to WAITING_LIST status
##### [PLANNED] Deadline is not set for waiting list students


#### Send scheduled mails

For all students in ACTIVE or SPECTATOR status, and where "delta" is 3 days.

##### If date is more than delta days less than 1st occasion, do nothing - beginner
##### If time is not less than 1st occasion - delta, send first e-mail - beginner
##### If time is more than 1st occasion, send e-mail - beginner
##### If there is no change, don't send change - beginner
##### If no mails have been sent, but more than 1 has passed, send it - beginner
##### One day after last occasion, send UTRAVALO - beginner
##### 2 days after last occasion, send certification if applicable - beginner
##### 2 days after last occasion, don't send certification if not applicable - beginner

##### If date is more than delta days less than 1st occasion, do nothing - advanced
##### If time is not less than 1st occasion - delta, send first e-mail - advanced
##### If time is more than 1st occasion, send e-mail - advanced
##### If there is no change, don't send change - advanced
##### If no mails have been sent, but more than 1 has passed, send it - advanced
##### One day after last occasion, send UTRAVALO - advanced
##### 2 days after last occasion, send certification if applicable - advanced
##### 2 days after last occasion, don't send certification if not applicable - advanced

#### Set course states

For all courses which are APPLICATION_OPEN, IN_PROGRESS, or RECENLTY_FINISHED status

##### If first day has passed, but not last, and course is not IN_PROGRESS, course should be put to IN_PROGRESS
##### If lasd day has passed, but not 35 days more, and course is not RECENTLY_CLOSED, it should be put to RECENTLY_CLOSED
##### If last day plus 35 days has passed, and course is not CLOSED, is should be put to CLOSED
##### If first or last day's date is missing, no error should happen, and np state change should be made
##### [PLANNED] If course is started, put waiting list students to SUBSCRIBED (erdeklodo) state and send mail


#### Update headcounts

For all APPLICATION_OPEN courses: INFO_SENT and ACTIVE students should be counted

##### If no students are there, count is 0. No change, nothing sent.
##### If no students are there, count is 0. It was 1, update sent.
##### If no students are there, count is 0. It was 2, update sent.
##### If there is one INFO_SENT student, and no one else, count is 1. No change, nothing sent.
##### If there is one INFO_SENT student, and no one else, count is 1. It was more, update sent.
##### If there is one INFO_SENT student, and no one else, count is 1. It was less, update sent.
##### If there is one ACTIVE student, and no one else, count is 1
##### If there is one ACTIVE and one INFO_SENT student, and no one else, count is 2
##### If there is a student with another state, cound is 0
##### If there is 2 INFO_SENT, 3 ACTIVE and 4 other students with miced states, count is 5

set PYTHONPATH=%PYTHONPATH%;.
nosetests --with-coverage --cover-erase --cover-html-dir=./coverage-reports --cover-html --cov-config .coveragerc

nosetests test.module_tests.test_clean_info_level_kiment > text.txt 2>&1


nosetests --with-coverage --cover-erase --cover-html-dir=./coverage-reports --cover-html --cov-config .coveragerc > text.txt 2>&1

DONE
- make commandfactory not a class
- fix coverage
- create consistent naming (command/request, factory, execute, no Hungarian names, etc)
- fix import order
- format PEP8
- fix remaining problems with naming
- folder structure
- remove duplications from api outputs
- try to remove encoding things, only the necessary should remain
- structure of functions/classes
- test structure: put tests for one class to one file
- eliminate magic values
- get rid of unicode encodings
- merge_dicts on crmfacade 228 and other places
- crm_data to facade, commandhandler to requesthandler
- hun names still
- go through it few times for little errors/illogical stuff
- remove wildcard imports
- public api __all__
- can we make constants constants?
- dunder names
    - how to document constructors
    - how to give code examples
    - how to denote parameter types

todo:
- write code documentation and generate (including json responses)
    - why all doc says args kwargs?
    - how to denote return types 
- check against clean code checklists
- check against design patterns (correct pattern structure, consistent naming)
- write readme correctly


* Description
* Testname (slogan)
* Given:
**
* Then:
**