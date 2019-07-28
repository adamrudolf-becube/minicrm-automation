"""
Contains common functions for the functionalities module.

If something is used by different functionalities, it is put here to avoid dependency between functionalities. If the
common functionality doens't contain business logic, and is only a feature of the CRM system, it should be part of
CrmFacade, but if it contains too much business logic, it needs to be here.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2019"