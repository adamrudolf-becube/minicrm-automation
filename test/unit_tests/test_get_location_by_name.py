# -*- coding: utf-8 -*-
from minicrm import crmrequestfactory
import test.requesthandlermock.responses.general as responses_general
import test.requesthandlermock.responses.locationlists as responses_locationlists
import test.requesthandlermock.responses.locations as responses_locations
from minicrmtestbase import MiniCrmTestBase


class TestGetLocationByName(MiniCrmTestBase):
    def test_get_location_by_name_returns_correct_course(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_location_list_by_location_name("Pannon Kincstár"),
            responses_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )

        self.request_handler.expect_request(
            crmrequestfactory.get_location(19),
            responses_locations.PANNON_KINCSTAR
        )

        result = self.crm_facade.get_location_by_name("Pannon Kincstár")
        self.assertEqual(result, responses_locations.PANNON_KINCSTAR[u"response"])

    def test_get_location_by_name_returns_none_for_nonexistent_course_code(self):
        self.request_handler.expect_request(
            crmrequestfactory.get_location_list_by_location_name("NONEXISTENT"),
            responses_general.EMPTY_LIST
        )

        result = self.crm_facade.get_location_by_name("NONEXISTENT")
        self.assertIsNone(result)
