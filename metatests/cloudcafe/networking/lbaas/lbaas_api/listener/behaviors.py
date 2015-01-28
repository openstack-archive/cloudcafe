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

from cloudcafe.networking.lbaas.lbaas_api.listener.behaviors import \
    ListenerBehaviors
from cloudcafe.networking.lbaas.lbaas_api.listener.client import \
    ListenersClient


class ListenerBehaviorsFixture(unittest.TestCase):
    """
    @summary: Listener Behaviors Tests
    """
    @classmethod
    def setUpClass(cls):
        super(ListenerBehaviorsFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.url = "http://fake.url.endpoint"
        cls.listener_id = "12345"
        cls.name = "Example HTTPS Listener"
        cls.load_balancer_id = "b8a35470-f65d-11e3-a3ac-0800200c9a66"
        cls.tenant_id = "352686b7-c4b2-44ec-a458-84239713f685"
        cls.default_pool_id = "8311446e-8a13-4c00-95b3-03a92f9759c7"
        cls.protocol = "https"
        cls.protocol_port = 443
        cls.description = "A very simple example of an HTTPS listener."
        cls.connection_limit = 200
        cls.admin_state_up = True

        cls.desired_status = "ACTIVE"
        cls.interval_time = 20
        cls.timeout = 120

        cls.listeners_client = ListenersClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)

        cls.listener_behaviors = ListenerBehaviors(
            listeners_client=cls.listeners_client, config=None)


class ListenerBehaviorsTests(object):

    @mock.patch.object(ListenerBehaviors, 'create_active_listener',
                       autospec=True)
    def test_create_active_listener(self, mock_request):
        create_active_listener_kwargs = (
            {'name': self.name,
             'load_balancer_id': self.load_balancer_id,
             'tenant_id': self.tenant_id,
             'default_pool_id': self.default_pool_id,
             'protocol': self.protocol,
             'protocol_port': self.protocol_port,
             'description': self.description,
             'connection_limit': self.connection_limit,
             'admin_state_up': self.admin_state_up})
        self.listener_behaviors.create_active_listener(
            **create_active_listener_kwargs)
        mock_request.assert_called_once_with(
            self.listener_behaviors,
            **create_active_listener_kwargs)

    @mock.patch.object(ListenerBehaviors,
                       'update_listener_and_wait_for_active',
                       autospec=True)
    def test_update_listener_and_wait_for_active(self, mock_request):
        update_listener_and_wait_for_active_kwargs = (
            {'name': self.name,
             'description': self.description,
             'default_pool_id': self.default_pool_id,
             'load_balancer_id': self.load_balancer_id,
             'admin_state_up': self.admin_state_up})
        self.listener_behaviors.update_listener_and_wait_for_active(
            **update_listener_and_wait_for_active_kwargs)
        mock_request.assert_called_once_with(
            self.listener_behaviors,
            **update_listener_and_wait_for_active_kwargs)

    @mock.patch.object(ListenerBehaviors,
                       'wait_for_listener_status',
                       autospec=True)
    def test_wait_for_listener_status(self, mock_request):
        wait_for_listener_status_kwargs = (
            {'listener_id': self.listener_id,
             'desired_status': self.desired_status,
             'interval_time': self.interval_time,
             'timeout': self.timeout})
        self.listener_behaviors.wait_for_listener_status(
            **wait_for_listener_status_kwargs)
        mock_request.assert_called_once_with(
            self.listener_behaviors,
            **wait_for_listener_status_kwargs)


class ListenersClientTestsXML(ListenerBehaviorsFixture,
                              ListenerBehaviorsTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class ListenersClientTestsJSON(ListenerBehaviorsFixture,
                               ListenerBehaviorsTests):
    SERIALIZE = 'json'
    DESERIALIZE = 'json'
