"""
Contains modules to provide an out-of-the-box solution to communicate with the MiniCRM system.

This package contains modules to handle http connection, create requests, trace behaviour, and provide a simple facade
for the users. The clients only have to instantiate a CrmFacade object with the connections and use it's simple
interface. Clients can also use functionalities directly, for example for tracing.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"