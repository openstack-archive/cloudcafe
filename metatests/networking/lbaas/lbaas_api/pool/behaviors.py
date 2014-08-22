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

import mock
import unittest

from cloudcafe.networking.lbaas.lbaas_api.pool.behaviors import PoolBehaviors
from cloudcafe.networking.lbaas.lbaas_api.pool.client import PoolsClient


class PoolBehaviorsFixture(unittest.TestCase):
    """
    @summary: Pool Behaviors Tests
    """
    @classmethod
    def setUpClass(cls):
        super(PoolBehaviorsFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.url = "http://fake.url.endpoint"
        cls.pool_id = "12345"
        cls.name = "Example HTTPS Pool"
        cls.description = "Example HTTPS Pool Description"
        cls.tenant_id = "352686b7-c4b2-44ec-a458-84239713f685"
        cls.protocol = "HTTPS"
        cls.lb_algorithm = "ROUND_ROBIN"
        cls.pool_id = "pool_123"
        cls.admin_state_up = True
        cls.sp_type = "COOKIE"
        cls.sp_cookie_name = "session_persistence_cookie"
        cls.session_persistence = {"type": cls.sp_type,
                                   "cookie_name": cls.sp_cookie_name}

        cls.desired_status = "ACTIVE"
        cls.interval_time = 20
        cls.timeout = 120

        cls.pools_client = PoolsClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)

        cls.pool_behaviors = PoolBehaviors(
            pools_client=cls.pools_client, config=None)


class PoolBehaviorsTests(object):

    @mock.patch.object(PoolBehaviors, 'create_active_pool', autospec=True)
    def test_create_active_pool(self, mock_request):
        create_active_pool_kwargs = (
            {'name': self.name,
             'tenant_id': self.tenant_id,
             'protocol': self.protocol,
             'lb_algorithm': self.lb_algorithm,
             'description': self.description,
             'session_persistence': self.session_persistence,
             'pool_id': self.pool_id,
             'admin_state_up': self.admin_state_up})
        self.pool_behaviors.create_active_pool(**create_active_pool_kwargs)
        mock_request.assert_called_once_with(
            self.pool_behaviors,
            **create_active_pool_kwargs)

    @mock.patch.object(PoolBehaviors, 'update_pool_and_wait_for_active',
                       autospec=True)
    def test_update_pool_and_wait_for_active(self, mock_request):
        update_pool_and_wait_for_active_kwargs = (
            {'name': self.name,
             'description': self.description,
             'session_persistence': self.session_persistence,
             'lb_algorithm': self.lb_algorithm,
             'pool_id': self.pool_id,
             'admin_state_up': self.admin_state_up})
        self.pool_behaviors.update_pool_and_wait_for_active(
            **update_pool_and_wait_for_active_kwargs)
        mock_request.assert_called_once_with(
            self.pool_behaviors,
            **update_pool_and_wait_for_active_kwargs)

    @mock.patch.object(PoolBehaviors, 'wait_for_pool_status', autospec=True)
    def test_wait_for_pool_status(self, mock_request):
        wait_for_pool_status_kwargs = (
            {'pool_id': self.pool_id,
             'desired_status': self.desired_status,
             'interval_time': self.interval_time,
             'timeout': self.timeout})
        self.pool_behaviors.wait_for_pool_status(**wait_for_pool_status_kwargs)
        mock_request.assert_called_once_with(
            self.pool_behaviors,
            **wait_for_pool_status_kwargs)


class PoolsClientTestsXML(PoolBehaviorsFixture, PoolBehaviorsTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class PoolsClientTestsJSON(PoolBehaviorsFixture, PoolBehaviorsTests):
    SERIALIZE = 'json'
    DESERIALIZE = 'json'
