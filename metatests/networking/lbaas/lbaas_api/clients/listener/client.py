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

from cloudcafe.networking.lbaas.lbaas_api.clients.listener.client import \
    ListenersClient
from cloudcafe.networking.lbaas.lbaas_api.models.request.listener import \
    CreateListener, UpdateListener
from cloudcafe.networking.lbaas.lbaas_api.models.response.listener import \
    Listener, Listeners


class ListenersClientFixture(unittest.TestCase):
    """
    @summary: Listener Client Tests
    """
    @classmethod
    def setUpClass(cls):
        super(ListenersClientFixture, cls).setUpClass()

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

        cls.full_url_listeners = (
            ListenersClient._LISTENERS_URL.format(
                base_url=cls.url))
        cls.full_url_listener = (
            ListenersClient._LISTENER_URL.format(
                base_url=cls.url,
                listener_id=cls.listener_id))

        cls.listeners_client = ListenersClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)


class ListenersClientTests(object):

    @mock.patch.object(ListenersClient, 'request', autospec=True)
    def test_create_listener(self, mock_request):

        create_listener_kwargs = (
            {'name': self.name,
             'load_balancer_id': self.load_balancer_id,
             'tenant_id': self.tenant_id,
             'default_pool_id': self.default_pool_id,
             'protocol': self.protocol,
             'protocol_port': self.protocol_port,
             'description': self.description,
             'connection_limit': self.connection_limit,
             'admin_state_up': self.admin_state_up})
        self.listeners_client.create_listener(
            **create_listener_kwargs)
        create_listener_request = CreateListener(
            **create_listener_kwargs)
        mock_request.assert_called_once_with(
            self.listeners_client,
            'POST',
            self.full_url_listeners,
            request_entity=create_listener_request,
            response_entity_type=Listener,
            requestslib_kwargs=None)

    @mock.patch.object(ListenersClient, 'request', autospec=True)
    def test_list_listener(self, mock_request):

        self.listeners_client.list_listeners()
        mock_request.assert_called_once_with(
            self.listeners_client,
            'GET',
            self.full_url_listeners,
            response_entity_type=Listeners,
            requestslib_kwargs=None)

    @mock.patch.object(ListenersClient, 'request', autospec=True)
    def test_get_listener(self, mock_request):

        self.listeners_client.get_listener(
            listener_id=self.listener_id)
        mock_request.assert_called_once_with(
            self.listeners_client,
            'GET',
            self.full_url_listener,
            response_entity_type=Listener,
            requestslib_kwargs=None)

    @mock.patch.object(ListenersClient, 'request', autospec=True)
    def test_update_listener(self, mock_request):

        update_listener_kwargs = (
            {'name': self.name,
             'description': self.description,
             'load_balancer_id': self.load_balancer_id,
             'default_pool_id': self.default_pool_id,
             'admin_state_up': self.admin_state_up})
        self.listeners_client.update_listener(
            listener_id=self.listener_id,
            **update_listener_kwargs)
        update_listener_request = UpdateListener(
            **update_listener_kwargs)
        mock_request.assert_called_once_with(
            self.listeners_client,
            'PUT',
            self.full_url_listener,
            request_entity=update_listener_request,
            response_entity_type=Listener,
            requestslib_kwargs=None)

    @mock.patch.object(ListenersClient, 'request', autospec=True)
    def test_delete_listener(self, mock_request):

        self.listeners_client.delete_listener(
            listener_id=self.listener_id)
        mock_request.assert_called_once_with(self.listeners_client,
                                             'DELETE',
                                             self.full_url_listener,
                                             requestslib_kwargs=None)


class ListenersClientTestsXML(ListenersClientFixture,
                              ListenersClientTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class ListenersClientTestsJSON(ListenersClientFixture,
                               ListenersClientTests):
    SERIALIZE = 'json'
    DESERIALIZE = 'json'
