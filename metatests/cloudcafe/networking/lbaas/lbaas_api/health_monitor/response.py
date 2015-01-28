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

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.health_monitor.response \
    import HealthMonitor, HealthMonitors


class BaseHealthMonitorResponseTest(unittest.TestCase):
    """
    @summary: Unit tests for the load balancer "healthmonitor" response model.

    HealthMonitorResponseTest
    HealthMonitorsResponseTest
    """
    @classmethod
    def setUpClass(cls):
        super(BaseHealthMonitorResponseTest, cls).setUpClass()
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.id_ = "8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
        cls.type_ = "HTTP"
        cls.tenant_id = "7725fe12-1c14-4f45-ba8e-44bf01763578"
        cls.delay = 20
        cls.timeout = 10
        cls.max_retries = 5
        cls.url_path = "/check"
        cls.expected_codes = "200-299"
        cls.admin_state_up = True
        cls.status = "ACTIVE"

        cls.healthmonitor_obj = HealthMonitor(
            id_=cls.id_, type_=cls.type_, tenant_id=cls.tenant_id,
            delay=cls.delay, timeout=cls.timeout, max_retries=cls.max_retries,
            url_path=cls.url_path, expected_codes=cls.expected_codes,
            admin_state_up=cls.admin_state_up, status=cls.status)
        healthmonitor_list = [cls.healthmonitor_obj]
        cls.healthmonitors_obj = HealthMonitors(healthmonitor_list)

        cls.healthmonitor_attribute_kwargs = {
            "id_": cls.id_,
            "type_": cls.type_,
            "tenant_id": cls.tenant_id,
            "delay": cls.delay,
            "timeout": cls.timeout,
            "max_retries": cls.max_retries,
            "url_path": cls.url_path,
            "expected_codes": cls.expected_codes,
            "admin_state_up": str(cls.admin_state_up).lower(),
            "status": cls.status
        }
        cls.actual_json_base = """
                    "id": "{id_}",
                    "type": "{type_}",
                    "tenant_id":"{tenant_id}",
                    "delay": {delay},
                    "timeout": {timeout},
                    "max_retries": {max_retries},
                    "url_path": "{url_path}",
                    "expected_codes": "{expected_codes}",
                    "admin_state_up": {admin_state_up},
                    "status": "{status}"
        """.format(**cls.healthmonitor_attribute_kwargs)

        cls.actual_xml_base = """
                    id="{id_}"
                    type="{type_}"
                    tenant_id="{tenant_id}"
                    delay="{delay}"
                    timeout="{timeout}"
                    max_retries="{max_retries}"
                    url_path="{url_path}"
                    expected_codes="{expected_codes}"
                    admin_state_up="{admin_state_up}"
                    status="{status}"
        """.format(**cls.healthmonitor_attribute_kwargs)


class HealthMonitorResponseTest(BaseHealthMonitorResponseTest):

    def setUp(self):
        super(HealthMonitorResponseTest, self).setUp()
        self.ROOT_TAG = HealthMonitor.ROOT_TAG
        self.expected_obj = self.healthmonitor_obj

    def test_healthmonitor_json(self):
        actual_json = """
            {{ "{root_tag}":
                {{
                    {actual_json_base}
                }}
            }}
            """.format(root_tag=self.ROOT_TAG,
                       actual_json_base=self.actual_json_base,
                       **self.healthmonitor_attribute_kwargs)
        actual_obj = HealthMonitor.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_healthmonitor_xml(self):
        actual_xml = """{xml_header}
                            <{root_tag}
                                {actual_xml_base}
                                xmlns="{xmlns}"
                            />""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            actual_xml_base=self.actual_xml_base,
            **self.healthmonitor_attribute_kwargs)
        actual_obj = HealthMonitor.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)


class HealthMonitorsResponseTest(BaseHealthMonitorResponseTest):

    def setUp(self):
        super(HealthMonitorsResponseTest, self).setUp()
        self.ROOT_TAG = HealthMonitors.ROOT_TAG
        self.CHILD_TAG = HealthMonitor.ROOT_TAG
        self.expected_obj = self.healthmonitors_obj

    def test_healthmonitors_json(self):
        actual_json = """
                        {{ "{root_tag}":
                            [{{
                                {actual_json_base}
                            }}]
                        }}
                        """.format(root_tag=self.ROOT_TAG,
                                   actual_json_base=self.actual_json_base,
                                   **self.healthmonitor_attribute_kwargs)
        actual_obj = HealthMonitors.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_healthmonitors_xml(self):
        actual_xml = """{xml_header}
                            <{root_tag} xmlns="{xmlns}">
                                <{child_tag}
                                    {actual_xml_base}
                                />
                            </{root_tag}>""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            child_tag=self.CHILD_TAG,
            actual_xml_base=self.actual_xml_base,
            **self.healthmonitor_attribute_kwargs)
        actual_obj = HealthMonitors.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)


if __name__ == "__main__":
    unittest.main()
