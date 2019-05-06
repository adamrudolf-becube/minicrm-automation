# -*- coding: utf-8 -*-
import crmrequestfactory

from minicrmtestbase import MiniCrmTestBase

import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.locationlists as apioutputs_locationlists
import test.minicrm_api_mock.apioutputs.locations as apioutputs_locations


class TestGetLocationByName(MiniCrmTestBase):
    def test_get_location_by_name_returns_correct_course(self):
        self.command_handler.expect_command(
            crmrequestfactory.get_location_list_by_location_name("Pannon Kincstár"),
            apioutputs_locationlists.LOCATION_LIST_FOR_LOCATION_NAME
        )

        self.command_handler.expect_command(
            crmrequestfactory.get_location(19),
            apioutputs_locations.PANNON_KINCSTAR
        )

        result = self.crm_data.get_location_by_name("Pannon Kincstár")
        self.assertEqual(result, apioutputs_locations.PANNON_KINCSTAR[u"response"])

    def test_get_location_by_name_returns_none_for_nonexistent_course_code(self):
        self.command_handler.expect_command(
            crmrequestfactory.get_location_list_by_location_name("NONEXISTENT"),
            apioutputs_general.EMPTY_LIST
        )

        result = self.crm_data.get_location_by_name("NONEXISTENT")
        self.assertIsNone(result)