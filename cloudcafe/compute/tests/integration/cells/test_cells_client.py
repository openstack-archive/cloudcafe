"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest2 as unittest
from httpretty import HTTPretty

from cloudcafe.compute.cells_api.client import CellsClient
from cloudcafe.compute.tests.integration.cells.responses \
    import CellsClientMockResponse
from cloudcafe.compute.tests.integration.fixtures \
    import IntegrationTestFixture

CELL_NAME = "cells_test"


class CellsClientTest(IntegrationTestFixture):

    @classmethod
    def setUpClass(cls):
        super(CellsClientTest, cls).setUpClass()
        cls.cells_client = CellsClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT
        )
        cells_uri = "{0}/os-cells".format(cls.COMPUTE_API_ENDPOINT)
        cls.cell_capacity_by_name_uri = "{0}/{1}/show_capacities".format(
            cells_uri, CELL_NAME)
        cls.aggr_cell_capacity_uri = "{0}/show_capacities".format(
            cells_uri)

    def test_get_aggr_cell_capacity(self):
        HTTPretty.register_uri(HTTPretty.GET, self.aggr_cell_capacity_uri,
                               body=CellsClientMockResponse.
                               get_aggr_cell_capacity())
        response = self.cells_client.get_aggregated_cell_capacity()
        self.assertEqual(200, response.status_code)
        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(CellsClientMockResponse.get_aggr_cell_capacity(),
                         response.content)

    def test_get_cell_capacity_by_name(self):
        HTTPretty.register_uri(HTTPretty.GET, self.cell_capacity_by_name_uri,
                               body=CellsClientMockResponse.
                               get_cell_capacity_by_cellname())
        response = self.cells_client.get_cell_capacity_by_name(CELL_NAME)
        self.assertEqual(200, response.status_code)
        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(CellsClientMockResponse.
                         get_cell_capacity_by_cellname(),
                         response.content)


if __name__ == '__main__':
    unittest.main()
