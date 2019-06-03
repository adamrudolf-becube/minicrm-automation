"""
Contains modules that implement mid-level functionality for using the MiniCRM facade.

The CrmFacade class implements the low-level functionalities, which don't make sense from the business point of view.
The free functions here use the CrmFacade to communicate with the MiniCRM system, but implement higher level business
logic. For example handling a new applicant includes deciding whether they go to waiting list or not, calculating the
application deadline, sending the initial mail and updating the headcounts of the courses. From business point of view
this can be implemented in one functionality, called "Handle New Applicant".

These functionalities still don't make up a whole application, but one application (script) can use and reuse them. The
reasonale behind this layer is to provide modularity for clarity and reusability.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"