"""
Copyright 2015 Rackspace

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

import json
import unittest

from cloudcafe.events.models.compute.common import FixedIp, FixedIps


class BaseFixedIpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseFixedIpTest, cls).setUpClass()

        cls.fixed_ip_dict = {
            "address": "10.10.0.0",
            "floating_ips": [],
            "label": "public",
            "meta": {},
            "type": "fixed",
            "version": 4,
            "vif_mac": "FE:ED:FA:00:1C:D4"
        }

        cls.fixed_ips_dict = {
            "fixed_ips": [cls.fixed_ip_dict]
        }

        cls.fixed_ip_obj = FixedIp._dict_to_obj(cls.fixed_ip_dict)
        cls.fixed_ips_obj = FixedIps._list_to_obj(
            cls.fixed_ips_dict['fixed_ips'])


class FixedIpTest(BaseFixedIpTest):

    def test_fixed_ip_json(self):
        expected_obj = self.fixed_ip_obj

        actual_json = json.dumps(self.fixed_ip_dict)
        actual_obj = FixedIp.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_fixed_ip_missing_attribute_json(self):
        modified_dict = self.fixed_ip_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = FixedIp.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_fixed_ip_extra_attribute_json(self):
        modified_dict = self.fixed_ip_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = FixedIp.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)


class FixedIpsTest(BaseFixedIpTest):

    def test_fixed_ips_json(self):
        expected_obj = self.fixed_ips_obj

        actual_json = json.dumps(self.fixed_ips_dict)
        actual_obj = FixedIps.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)

    def test_fixed_ips_missing_attribute_json(self):
        modified_dict = self.fixed_ips_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = FixedIps.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_fixed_ips_extra_attribute_json(self):
        modified_dict = self.fixed_ips_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = FixedIps.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)
