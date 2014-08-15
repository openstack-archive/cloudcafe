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

from cloudcafe.networking.lbaas.lbaas_api.pool.client import \
    PoolsClient
from cloudcafe.networking.lbaas.lbaas_api.pool.request import \
    CreatePool, UpdatePool
from cloudcafe.networking.lbaas.lbaas_api.pool.response import \
    Pool, Pools


class PoolsClientFixture(unittest.TestCase):
    """
    @summary: Pool Client Tests
    """
    @classmethod
    def setUpClass(cls):
        super(PoolsClientFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.url = "http://fake.url.endpoint"
        cls.pool_id = "12345"
        cls.name = "Example HTTPS Pool"
        cls.description = "Example HTTPS Pool Description"
        cls.tenant_id = "352686b7-c4b2-44ec-a458-84239713f685"
        cls.protocol = "HTTPS"
        cls.lb_algorithm = "ROUND_ROBIN"
        cls.healthmonitor_id = "health_monitor_123"
        cls.admin_state_up = True
        cls.sp_type = "COOKIE"
        cls.sp_cookie_name = "session_persistence_cookie"
        cls.session_persistence = {"type": cls.sp_type,
                                   "cookie_name": cls.sp_cookie_name}

        cls.full_url_pools = (
            PoolsClient._POOLS_URL.format(
                base_url=cls.url))
        cls.full_url_pool = (
            PoolsClient._POOL_URL.format(
                base_url=cls.url,
                pool_id=cls.pool_id))

        cls.pools_client = PoolsClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)


class PoolsClientTests(object):

    @mock.patch.object(PoolsClient, 'request', autospec=True)
    def test_create_pool(self, mock_request):

        create_pool_kwargs = (
            {'name': self.name,
             'tenant_id': self.tenant_id,
             'protocol': self.protocol,
             'lb_algorithm': self.lb_algorithm,
             'description': self.description,
             'session_persistence': self.session_persistence,
             'healthmonitor_id': self.healthmonitor_id,
             'admin_state_up': self.admin_state_up})
        self.pools_client.create_pool(**create_pool_kwargs)
        create_pool_request = CreatePool(**create_pool_kwargs)
        mock_request.assert_called_once_with(
            self.pools_client,
            'POST',
            self.full_url_pools,
            request_entity=create_pool_request,
            response_entity_type=Pool,
            requestslib_kwargs=None)

    @mock.patch.object(PoolsClient, 'request', autospec=True)
    def test_list_pool(self, mock_request):

        self.pools_client.list_pools()
        mock_request.assert_called_once_with(
            self.pools_client,
            'GET',
            self.full_url_pools,
            response_entity_type=Pools,
            requestslib_kwargs=None)

    @mock.patch.object(PoolsClient, 'request', autospec=True)
    def test_get_pool(self, mock_request):

        self.pools_client.get_pool(pool_id=self.pool_id)
        mock_request.assert_called_once_with(
            self.pools_client,
            'GET',
            self.full_url_pool,
            response_entity_type=Pool,
            requestslib_kwargs=None)

    @mock.patch.object(PoolsClient, 'request', autospec=True)
    def test_update_pool(self, mock_request):

        update_pool_kwargs = (
            {'name': self.name,
             'description': self.description,
             'session_persistence': self.session_persistence,
             'lb_algorithm': self.lb_algorithm,
             'healthmonitor_id': self.healthmonitor_id,
             'admin_state_up': self.admin_state_up})
        self.pools_client.update_pool(pool_id=self.pool_id,
                                      **update_pool_kwargs)
        update_pool_request = UpdatePool(**update_pool_kwargs)
        mock_request.assert_called_once_with(
            self.pools_client,
            'PUT',
            self.full_url_pool,
            request_entity=update_pool_request,
            response_entity_type=Pool,
            requestslib_kwargs=None)

    @mock.patch.object(PoolsClient, 'request', autospec=True)
    def test_delete_pool(self, mock_request):

        self.pools_client.delete_pool(pool_id=self.pool_id)
        mock_request.assert_called_once_with(self.pools_client,
                                             'DELETE',
                                             self.full_url_pool,
                                             requestslib_kwargs=None)


class PoolsClientTestsXML(PoolsClientFixture, PoolsClientTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class PoolsClientTestsJSON(PoolsClientFixture, PoolsClientTests):

    SERIALIZE = 'json'
    DESERIALIZE = 'json'
