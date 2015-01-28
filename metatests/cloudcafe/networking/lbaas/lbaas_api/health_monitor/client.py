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

from cloudcafe.networking.lbaas.lbaas_api.health_monitor.client \
    import HealthMonitorsClient
from cloudcafe.networking.lbaas.lbaas_api.health_monitor.request \
    import CreateHealthMonitor, UpdateHealthMonitor
from cloudcafe.networking.lbaas.lbaas_api.health_monitor.response \
    import HealthMonitor, HealthMonitors


class HealthMonitorsClientFixture(unittest.TestCase):
    """
    @summary: Health Monitor Client Tests
    """
    @classmethod
    def setUpClass(cls):
        super(HealthMonitorsClientFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.url = "http://fake.url.endpoint"
        cls.health_monitor_id = "12345"
        cls.type_ = "HTTP"
        cls.tenant_id = "453105b9-1754-413f-aab1-55f1af620750"
        cls.delay = 20
        cls.timeout = 10
        cls.max_retries = 5
        cls.http_method = "GET"
        cls.url_path = "/check"
        cls.expected_codes = "200-299"
        cls.admin_state_up = False

        cls.full_url_health_monitors = (
            HealthMonitorsClient._HEALTH_MONITORS_URL.format(
                base_url=cls.url))
        cls.full_url_health_monitor = (
            HealthMonitorsClient._HEALTH_MONITOR_URL.format(
                base_url=cls.url,
                health_monitor_id=cls.health_monitor_id))

        cls.health_monitors_client = HealthMonitorsClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)


class HealthMonitorsClientTests(object):

    @mock.patch.object(HealthMonitorsClient, 'request', autospec=True)
    def test_create_health_monitor(self, mock_request):

        create_health_monitor_kwargs = (
            {'type_': self.type_,
             'tenant_id': self.tenant_id,
             'delay': self.delay,
             'timeout': self.timeout,
             'max_retries': self.max_retries,
             'http_method': self.http_method,
             'url_path': self.url_path,
             'expected_codes': self.expected_codes,
             'admin_state_up': self.admin_state_up})
        self.health_monitors_client.create_health_monitor(
            **create_health_monitor_kwargs)
        create_health_monitor_request = CreateHealthMonitor(
            **create_health_monitor_kwargs)
        mock_request.assert_called_once_with(
            self.health_monitors_client,
            'POST',
            self.full_url_health_monitors,
            request_entity=create_health_monitor_request,
            response_entity_type=HealthMonitor,
            requestslib_kwargs=None)

    @mock.patch.object(HealthMonitorsClient, 'request', autospec=True)
    def test_list_health_monitor(self, mock_request):

        self.health_monitors_client.list_health_monitors()
        mock_request.assert_called_once_with(
            self.health_monitors_client,
            'GET',
            self.full_url_health_monitors,
            response_entity_type=HealthMonitors,
            requestslib_kwargs=None)

    @mock.patch.object(HealthMonitorsClient, 'request', autospec=True)
    def test_get_health_monitor(self, mock_request):

        self.health_monitors_client.get_health_monitor(
            health_monitor_id=self.health_monitor_id)
        mock_request.assert_called_once_with(
            self.health_monitors_client,
            'GET',
            self.full_url_health_monitor,
            response_entity_type=HealthMonitor,
            requestslib_kwargs=None)

    @mock.patch.object(HealthMonitorsClient, 'request', autospec=True)
    def test_update_health_monitor(self, mock_request):

        update_health_monitor_kwargs = (
            {'delay': self.delay,
             'timeout': self.timeout,
             'max_retries': self.max_retries,
             'http_method': self.http_method,
             'url_path': self.url_path,
             'expected_codes': self.expected_codes,
             'admin_state_up': self.admin_state_up})
        self.health_monitors_client.update_health_monitor(
            health_monitor_id=self.health_monitor_id,
            **update_health_monitor_kwargs)
        update_health_monitor_request = UpdateHealthMonitor(
            **update_health_monitor_kwargs)
        mock_request.assert_called_once_with(
            self.health_monitors_client,
            'PUT',
            self.full_url_health_monitor,
            request_entity=update_health_monitor_request,
            response_entity_type=HealthMonitor,
            requestslib_kwargs=None)

    @mock.patch.object(HealthMonitorsClient, 'request', autospec=True)
    def test_delete_health_monitor(self, mock_request):

        self.health_monitors_client.delete_health_monitor(
            health_monitor_id=self.health_monitor_id)
        mock_request.assert_called_once_with(self.health_monitors_client,
                                             'DELETE',
                                             self.full_url_health_monitor,
                                             requestslib_kwargs=None)


class HealthMonitorsClientTestsXML(HealthMonitorsClientFixture,
                                   HealthMonitorsClientTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class HealthMonitorsClientTestsJSON(HealthMonitorsClientFixture,
                                    HealthMonitorsClientTests):

    SERIALIZE = 'json'
    DESERIALIZE = 'json'
