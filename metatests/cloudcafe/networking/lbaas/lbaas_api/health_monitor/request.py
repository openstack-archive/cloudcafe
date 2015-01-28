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

@summary: Unit tests for the load balancer "health monitor" request model.

CreateHealthMonitorRequestTest
UpdateHealthMonitorRequestTest
"""

import json
import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.health_monitor.request \
    import CreateHealthMonitor, UpdateHealthMonitor


class HealthMonitorRequestTestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.type_ = "HTTP"
        cls.tenant_id = "453105b9-1754-413f-aab1-55f1af620750"
        cls.delay = 20
        cls.timeout = 10
        cls.max_retries = 5
        cls.http_method = "GET"
        cls.url_path = "/check"
        cls.expected_codes = "200-299"
        cls.admin_state_up = False
        cls.create_health_monitor_obj = CreateHealthMonitor(
            type_=cls.type_,
            tenant_id=cls.tenant_id,
            delay=cls.delay,
            timeout=cls.timeout,
            max_retries=cls.max_retries,
            http_method=cls.http_method,
            url_path=cls.url_path,
            expected_codes=cls.expected_codes,
            admin_state_up=cls.admin_state_up
        )

        cls.updated_delay = 30
        cls.updated_timeout = 20
        cls.updated_max_retries = 10
        cls.updated_http_method = "POST"
        cls.updated_url_path = "/health_check"
        cls.updated_expected_codes = "200-220"
        cls.updated_admin_state_up = True
        cls.update_health_monitor_obj = UpdateHealthMonitor(
            delay=cls.updated_delay,
            timeout=cls.updated_timeout,
            max_retries=cls.updated_max_retries,
            http_method=cls.updated_http_method,
            url_path=cls.updated_url_path,
            expected_codes=cls.updated_expected_codes,
            admin_state_up=cls.updated_admin_state_up
        )


class CreateHealthMonitorRequestTest(HealthMonitorRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = CreateHealthMonitor.ROOT_TAG

    def test_create_health_monitor_json(self):
        actual_json = json.loads(
            self.create_health_monitor_obj.serialize('json'))
        # Create python dict then JSON transform to handle
        # JSON objects and types such as the boolean
        json_dict = {self.ROOT_TAG: {'type': self.type_,
                                     'tenant_id': self.tenant_id,
                                     'delay': self.delay,
                                     'timeout': self.timeout,
                                     'max_retries': self.max_retries,
                                     'http_method': self.http_method,
                                     'url_path': self.url_path,
                                     'expected_codes': self.expected_codes,
                                     'admin_state_up': self.admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_create_health_monitor_xml(self):
        actual_xml = self.create_health_monitor_obj.serialize('xml')
        expected_xml = (
            '{xml_header}<{root_tag} '
            'admin_state_up="{admin_state_up}" '
            'delay="{delay}" '
            'expected_codes="{expected_codes}" '
            'http_method="{http_method}" '
            'max_retries="{max_retries}" '
            'tenant_id="{tenant_id}" '
            'timeout="{timeout}" '
            'type="{type_}" '
            'url_path="{url_path}" '
            'xmlns="{xmlns}" />').format(
                xml_header=self.XML_HEADER,
                xmlns=self.XML_NS,
                root_tag=self.ROOT_TAG,
                type_=self.type_, tenant_id=self.tenant_id,
                delay=self.delay, timeout=self.timeout,
                max_retries=self.max_retries, http_method=self.http_method,
                url_path=self.url_path, expected_codes=self.expected_codes,
                admin_state_up=self.admin_state_up)
        self.assertEqual(expected_xml, actual_xml)


class UpdateHealthMonitorRequestTest(HealthMonitorRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = UpdateHealthMonitor.ROOT_TAG

    def test_update_health_monitor_json(self):
        actual_json = json.loads(
            self.update_health_monitor_obj.serialize('json'))
        json_dict = {self.ROOT_TAG: {
            "delay": self.updated_delay,
            "timeout": self.updated_timeout,
            "max_retries": self.updated_max_retries,
            "http_method": self.updated_http_method,
            "url_path": self.updated_url_path,
            "expected_codes": self.updated_expected_codes,
            "admin_state_up": self.updated_admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_update_health_monitor_xml(self):
        actual_xml = self.update_health_monitor_obj.serialize('xml')
        expected_xml = ('{xml_header}<{root_tag} '
                        'admin_state_up="{admin_state_up}" '
                        'delay="{delay}" '
                        'expected_codes="{expected_codes}" '
                        'http_method="{http_method}" '
                        'max_retries="{max_retries}" '
                        'timeout="{timeout}" '
                        'url_path="{url_path}" '
                        'xmlns="{xmlns}" />').format(
                            xml_header=self.XML_HEADER,
                            xmlns=self.XML_NS,
                            root_tag=self.ROOT_TAG,
                            delay=self.updated_delay,
                            timeout=self.updated_timeout,
                            max_retries=self.updated_max_retries,
                            http_method=self.updated_http_method,
                            url_path=self.updated_url_path,
                            expected_codes=self.updated_expected_codes,
                            admin_state_up=self.updated_admin_state_up)
        self.assertEqual(expected_xml, actual_xml)

if __name__ == "__main__":
    unittest.main()
