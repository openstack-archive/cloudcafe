"""
Copyright 2014 Rackspace
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

import unittest
import mock
import json

from cloudcafe.identity.v3.common.catalog.models.responses import (
    Catalog, Links, Endpoint, Endpoints, Service)


class Mock(object):
    ROOT_TAG = 'endpoints'
    endpoints = 'mocked stuff'

    @classmethod
    def _dict_to_obj(cls, data):
        return "mocked stuff"

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return "mocked stuff"

    @classmethod
    def _list_to_obj(cls, data):
        return cls


class CatalogResponseTests(unittest.TestCase):
    """
    Metatests for v3 Catalog response model
    """
    RESPONSES = 'cloudcafe.identity.v3.common.catalog.models.responses'

    @mock.patch(RESPONSES+'.Links', Mock)
    @mock.patch(RESPONSES+'.Catalog', Mock)
    def test_json_to_obj(self):
        """
        test to verify Catalog.json_to_obj() can convert a JSON
        representation of a Catalog to a Catalog object
        """
        # ARRANGE
        catalog_dict = {
            'catalog': 'test_catalog',
            'links': 'test_links'
        }

        catalog_json = json.dumps(catalog_dict)

        expected_catalog_obj = Catalog(catalog='mocked stuff',
                                       links='mocked stuff')
        # ACT
        catalog_resp_obj = Catalog._json_to_obj(catalog_json)
        # ASSERT
        self.assertEqual(expected_catalog_obj, catalog_resp_obj)

    @mock.patch(RESPONSES+'.Service', Mock)
    def test_dict_to_obj(self):
        """
        test to verify Catalog.json_to_obj() can convert a JSON
        representation of a Catalog to a Catalog object
        """
        # ARRANGE
        catalog_dict = {
            'catalog': 'test_catalog',
            'links': 'test_links'
        }
        expected_catalog_obj = ['mocked stuff', 'mocked stuff']
        # ACT
        catalog_resp_obj = Catalog._dict_to_obj(catalog_dict)
        # ASSERT
        self.assertEqual(expected_catalog_obj, catalog_resp_obj)


class LinksResponseTests(unittest.TestCase):
    """
    Metatests for v3 Links response model
    """
    def test_dict_to_obj(self):
        """
        test to verify Links.dict_to_obj() can convert a dictionary
        representation of a Links to a Links object
        """
        # ARRANGE
        links_dict = {
            'self': 'test_self'
        }
        expected_links_obj = Links(self_='test_self')
        # ACT
        links_resp_obj = Links._dict_to_obj(links_dict)
        # ASSERT
        self.assertEqual(expected_links_obj, links_resp_obj)


class ServiceResponseTests(unittest.TestCase):
    """
    Metatests for v3 Service response model
    """
    RESPONSES = 'cloudcafe.identity.v3.common.catalog.models.responses'

    @mock.patch(RESPONSES+'.Endpoints', Mock)
    def test_dict_to_obj(self):
        """
        test to verify Service.dict_to_obj() can convert a dictionary
        representation of a Service to a Service object
        """
        # ARRANGE
        service_dict = {
            'endpoints': 'test_endpoints',
            'type': 'test_type'
        }
        expected_service_obj = Service(endpoints='mocked stuff',
                                       type='test_type')
        # ACT
        service_resp_obj = Service._dict_to_obj(service_dict)
        # ASSERT
        self.assertEqual(expected_service_obj, service_resp_obj)


class EndpointResponseTests(unittest.TestCase):
    """
    Metatests for v3 Endpoint response model
    """
    def test_dict_to_obj(self):
        """
        test to verify Endpoint.dict_to_obj() can convert a dictionary
        representation of a Endpoint to a Endpoint object
        """
        # ARRANGE
        endpoint_dict = {
            'interface': 'test_interface',
            'id': 'test_id',
            'region': 'test_region',
            'url': 'test_url'
        }
        expected_endpoint_obj = Endpoint(interface='test_interface',
                                         id='test_id',
                                         region='test_region',
                                         url='test_url')
        # ACT
        endpoint_resp_obj = Endpoint._dict_to_obj(endpoint_dict)
        # ASSERT
        self.assertEqual(expected_endpoint_obj, endpoint_resp_obj)


class EndpointsResponseTests(unittest.TestCase):
    """
    Metatests for v3 Endpoints response model
    """
    RESPONSES = 'cloudcafe.identity.v3.common.catalog.models.responses'
    ROOT_TAG = 'endpoints'

    @mock.patch(RESPONSES+'.Endpoint', Mock)
    def test_list_to_obj(self):
        """
        test to verify Endpoints.list_to_obj() can convert a list
        representation of Endpoints to an Endpoints object
        """
        # ARRANGE
        endpoints_list = ['test_endpoint_1',
                          'test_endpoint_2',
                          'test_endpoint_3']
        expected_endpoints_obj = Endpoints(endpoints=['mocked stuff',
                                                      'mocked stuff',
                                                      'mocked stuff'])
        # ACT
        endpoints_resp_obj = Endpoints._list_to_obj(endpoints_list)
        # ASSERT
        self.assertEqual(expected_endpoints_obj, endpoints_resp_obj)

    @mock.patch(RESPONSES+'.Endpoint', Mock)
    def test_json_to_obj(self):
        """
        test to verify Endpoints.list_to_obj() can convert a list
        representation of Endpoints to an Endpoints object
        """
        # ARRANGE
        endpoints_list = ['test_endpoint_1',
                          'test_endpoint_2',
                          'test_endpoint_3']
        endpoints_dict = {
            self.ROOT_TAG: endpoints_list}
        endpoints_json = json.dumps(endpoints_dict)
        expected_endpoints_obj = Endpoints(endpoints=['mocked stuff',
                                                      'mocked stuff',
                                                      'mocked stuff'])
        # ACT
        endpoints_resp_obj = Endpoints._json_to_obj(endpoints_json)
        # ASSERT
        self.assertEqual(expected_endpoints_obj, endpoints_resp_obj)


if __name__ == '__main__':
    unittest.main()
