# BeCube MiniCRM automation script system

**Disclaimer**: this software is in production, but is currently under
heavy refactoration. This includes (among many other things) writing
this README. So this (although contains the truth) is heavily under
construction. 

## Description

### What is this for

Me, Adam Rudolf run a little programming school in Hungary, called
BeCube. BeCube uses a CRM (Customer Relationship Management) software
called MiniCRM by MiniCRM Zrt. to store information about our customers,
teachers, courses, locations, invoicing and e-mailing.

Although MiniCRM provides a list of features to automate processes
related to organizing courses and manage the lifecycle of students, a
lot of customization is needed to fulfill needs of BeCube.

This project contains the script system, which communicates with the
MiniCRM system through it's REST API to automate processes.

This principle is also called [dog fooding](https://en.wikipedia.org/wiki/Eating_your_own_dog_food).

### Why is it public

BeCube is a programming school. We teach the basic principles of
programming using Python. We thought that why not expose this code to
our students, and to the public.

If we teach coding, and do coding, we should show our students what code
we are writing to be the example we think is good.   

## Principles

### Not storing information

The script system should never store any information it fetches from
the server (i.e. the MiniCRM system). It has mupltiple purposes:

* **Single source of truth** - the information is always stored in
MiniCRM, so it can be used as the single source of truth. Double storing
could cause inconsystencies, and more complex logic. Note that some data
can be temprorarily stored in the memory for caching purposes. This data
is never written to the hard disk, and is never stored for more than the
scope of a function.

* **Information security** - in whatever machine this code is running,
we don't have to care about information security, because the machine is
not storing informaition.
 
* **Server independency** - the script doesn't remember what it did last
time. What matters is only what happens in the current run. This gives
us more independency: we can change the machine for running this code
any time. The current machine can even explode, loosing everything on
it, we can immediately start running the code from another machine.
 
* **Consistency** - the scrpipt doesn't change the state of the machine
it's runnign on. This means that the scipt can die mid-run, we can start
it again withour any cleanup or other preparation.

### Independent runs - can be run any time and repeatedly

These scripts should never leave the system in inconsistent state.

A run mustn't depend on a previous run.

A run of this script musntn't affect any of the later runs *directly*.
(The run depends on the state of the CRM system, and also changes the
state of the CRM system, so indirectly running a script can cause
changes in the next run.) 

If the script is run very frequently for testing purposes, it should not
cause problem.

If the script is not run for a while, it shouldn't cause a problem.

### Partiality - can be run partially and then run again

If the script dies mid-run, it should be able to be started over from
the beginning and not causing problems.

If only specific features are executed, it shoudn't cause a problem.

### Independency from server - can be run from anywhere

The MiniCRM system should not know about the server which runs these
scripts.

The MiniCRM system should not expect these scripts to be run.

It ensures that skipping or repeating these scripts are not a problem,
and also that the server can be changed without any additional
consideration. 
  
## Code quality

The code should always comply with these rules:

* **Clean code** - follow principles of Rober C. Martin's clean code.
We have to understand the Clean Code principles. We have to know why we
are following them, we have to know when to break them, and we have to
know why to break them.
 
* **Design patterns kept in mind** - we have to be aware of the commonly
used design patterns, and find the situations where they fit naturally.
If there is a standard way of doing something, we have to do it in that
standard way, but don't overuse design patterns if they don't fit.
Examples: we use the Strategy Pattern to inject the RequestHandler to
the CrmFacade instance to be able to use it with a mock for testing. We
also use the Facade pattern for hiding the complexity of request
handling, creation of requests and additional logic from the users. But
we also use a factory module for requeast creation, which is not
following the traditional Factory Pattern. 

* **PEP-8 is followed** - we follow the official Python styling
guidelines whenever we don't have explicit and understood reason why not
to. 

* **Nicely tested**
    * We use automated tests in different levels with nicely used
    mocking
    * We measure and control the test coverage. We don't use coverage as
    a goal, but as a tool to detect untested features or dead code.
    Whenever we have uncovered code, that is marked explicitly and we
    have a good reason for that.
    
* **Version controlled in a very nice manner** - code is kept in Git. We
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
    * The basic principles, high level code structre and pedagigic 
    description is stored in the README.md (this document). The rule of
    thumb is that the project should be understood by reading this, but
    everything which changes with code updates shouldn't be here.  
    * The low level functionality, implementation details are documented
    with inline doc comments in the code. This is compiled to an API
    documentation HTML by automated documentation tool. Every
    implementation detail should be documented here. If you need to
    understand and/or use the code, you have to read this and not the
    README:


## Technical aspects

For historical reasons, the code is being run on a server where we have
no full control. Therefore we need to align with the not always
up-to-date versions of Python and modules. This is the reason we use
things, which you might find obsolete. 

* Code is written in Pyhton 2.7.9
* Main modules we use:
    * pip 10.0.1
    * For handling API requests we use requests 2.21.0
* unittest, coverage and documentation frameworks
* We use unittest for automatic test runs, with nose (1.3.7) for test
discovery.
* For test coverage, we use coverage 4.5.2.
* We use Sphinx 1.4.8 for generating html from inline doc comments. 
* On the server the scripts are automated by cron. This is a builtin
daemon (a software which always runs in the background) in Linux
systems, and you can schedule regular jobs (like running a Python
program) in a file called crontab. Our crontab runs "quickscript.py"
every 15 minutes and "dailyscript.py" every day at 8:00. The scripts can
be run in any other manner of course, but this was kept in mind when'
writing these scripts.

## Structure



## Test sescriptions

We have 3 levels of testing:
* **Unit test level** - local methods and single API calls.
* **Module test level** - single, standalone API functionalities, like cleaning INFO_SENT and handle waiting list. This is maybe the most important level of testing.
* **Use cases** - whole scripts are tested. Not evey possible combination is tested, only typical or important scenarios.

In the test descriptions we will follow the given-when-then approach, except that the logic of the script is to query the system and modify it. The script's behavious only depends on the state of the system, and the script always initializes. Therefore actions in the CRM system are never triggers to any action, every trigger is that the script is being run. The "when" part therefore is excluded from the test descriptions.
