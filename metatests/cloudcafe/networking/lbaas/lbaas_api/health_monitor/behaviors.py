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

from cloudcafe.networking.lbaas.lbaas_api.health_monitor.behaviors \
    import HealthMonitorBehaviors
from cloudcafe.networking.lbaas.lbaas_api.health_monitor.client \
    import HealthMonitorsClient


class HealthMonitorBehaviorsFixture(unittest.TestCase):
    """
    @summary: Health Monitor Behaviors Tests
    """
    @classmethod
    def setUpClass(cls):
        super(HealthMonitorBehaviorsFixture, cls).setUpClass()

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

        cls.desired_status = "ACTIVE"
        cls.interval_time = 20
        cls.timeout = 120

        cls.health_monitors_client = HealthMonitorsClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)

        cls.health_monitor_behaviors = HealthMonitorBehaviors(
            health_monitors_client=cls.health_monitors_client, config=None)


class HealthMonitorBehaviorsTests(object):

    @mock.patch.object(HealthMonitorBehaviors, 'create_active_health_monitor',
                       autospec=True)
    def test_create_active_health_monitor(self, mock_request):

        create_active_health_monitor_kwargs = (
            {'type_': self.type_,
             'tenant_id': self.tenant_id,
             'delay': self.delay,
             'timeout': self.timeout,
             'max_retries': self.max_retries,
             'http_method': self.http_method,
             'url_path': self.url_path,
             'expected_codes': self.expected_codes,
             'admin_state_up': self.admin_state_up})
        self.health_monitor_behaviors.create_active_health_monitor(
            **create_active_health_monitor_kwargs)
        mock_request.assert_called_once_with(
            self.health_monitor_behaviors,
            **create_active_health_monitor_kwargs)

    @mock.patch.object(HealthMonitorBehaviors,
                       'update_health_monitor_and_wait_for_active',
                       autospec=True)
    def test_update_health_monitor_and_wait_for_active(self, mock_request):

        update_health_monitor_and_wait_for_active_kwargs = (
            {'health_monitor_id': self.health_monitor_id,
             'delay': self.delay,
             'timeout': self.timeout,
             'max_retries': self.max_retries,
             'http_method': self.http_method,
             'url_path': self.url_path,
             'expected_codes': self.expected_codes,
             'admin_state_up': self.admin_state_up})
        self.health_monitor_behaviors.\
            update_health_monitor_and_wait_for_active(
                **update_health_monitor_and_wait_for_active_kwargs)
        mock_request.assert_called_once_with(
            self.health_monitor_behaviors,
            **update_health_monitor_and_wait_for_active_kwargs)

    @mock.patch.object(HealthMonitorBehaviors,
                       'wait_for_health_monitor_status',
                       autospec=True)
    def test_wait_for_health_monitor_status(self, mock_request):

        wait_for_health_monitor_status_kwargs = (
            {'health_monitor_id': self.health_monitor_id,
             'desired_status': self.desired_status,
             'interval_time': self.interval_time,
             'timeout': self.timeout})
        self.health_monitor_behaviors.wait_for_health_monitor_status(
            **wait_for_health_monitor_status_kwargs)
        mock_request.assert_called_once_with(
            self.health_monitor_behaviors,
            **wait_for_health_monitor_status_kwargs)


class HealthMonitorsClientTestsXML(HealthMonitorBehaviorsFixture,
                                   HealthMonitorBehaviorsTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class HealthMonitorsClientTestsJSON(HealthMonitorBehaviorsFixture,
                                    HealthMonitorBehaviorsTests):
    SERIALIZE = 'json'
    DESERIALIZE = 'json'
