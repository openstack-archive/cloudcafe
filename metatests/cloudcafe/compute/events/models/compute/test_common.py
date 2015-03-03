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

from cloudcafe.compute.events.models.common import (
    Bandwidth, BandwidthInterface, FixedIp, FixedIps, ImageMeta,
    InstanceException)


class BaseCommonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseCommonTest, cls).setUpClass()

        cls.bandwidth_interface_dict = {
            "bw_in": 123456,
            "bw_out": 654321
        }

        cls.bandwidth_dict = {
            "private": cls.bandwidth_interface_dict,
            "public": cls.bandwidth_interface_dict,
            "extra": cls.bandwidth_interface_dict
        }

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

        cls.image_meta_dict = {
            "auto_disk_config": "disabled",
            "base_image_ref": "5e91ad7f-afe4-4a83-bd5f-84673462cae1",
            "container_format": "ovf",
            "disk_format": "vhd",
            "image_type": "base",
            "min_disk": "20",
            "min_ram": "512",
            "org.openstack__1__architecture": "x64",
            "org.openstack__1__os_distro": "com.ubuntu",
            "org.openstack__1__os_version": "12.04",
            "os_type": "linux"
        }

        cls.instance_exception_dict = {
            "kwargs": {
                "instance_uuid": "5e91ad7f-afe4-4a83-bd5f-84673462cae1",
                "reason": "Something broke",
                "code": 500
            }
        }

        cls.bandwidth_obj = Bandwidth._dict_to_obj(cls.bandwidth_dict)
        cls.bandwidth_interface_obj = BandwidthInterface._dict_to_obj(
            cls.bandwidth_interface_dict)
        cls.fixed_ip_obj = FixedIp._dict_to_obj(cls.fixed_ip_dict)
        cls.fixed_ips_obj = FixedIps._list_to_obj(
            cls.fixed_ips_dict['fixed_ips'])
        cls.image_meta_obj = ImageMeta._dict_to_obj(cls.image_meta_dict)
        cls.instance_exception_obj = InstanceException._dict_to_obj(
            cls.instance_exception_dict)


class BandwidthTest(BaseCommonTest):

    def test_bandwidth_json(self):
        expected_obj = self.bandwidth_obj

        actual_json = json.dumps(self.bandwidth_dict)
        actual_obj = Bandwidth.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_bandwidth_empty_json(self):
        empty_dict = {}
        expected_obj = Bandwidth._dict_to_obj(empty_dict)

        actual_json = json.dumps(empty_dict)
        actual_obj = Bandwidth.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertTrue(actual_obj.is_empty())

    def test_bandwidth_extra_attribute_json(self):
        modified_dict = self.bandwidth_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = Bandwidth.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)


class BandwidthInterfaceTest(BaseCommonTest):

    def test_bandwidth_instance_json(self):
        expected_obj = self.bandwidth_interface_obj

        actual_json = json.dumps(self.bandwidth_interface_dict)
        actual_obj = BandwidthInterface.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_bandwidth_interface_missing_attribute_json(self):
        modified_dict = self.bandwidth_interface_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = BandwidthInterface.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_bandwidth_interface_extra_attribute_json(self):
        modified_dict = self.bandwidth_interface_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = BandwidthInterface.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)


class FixedIpTest(BaseCommonTest):

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


class FixedIpsTest(BaseCommonTest):

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


class ImageMetaTest(BaseCommonTest):

    def test_image_meta_json(self):
        expected_obj = self.image_meta_obj

        actual_json = json.dumps(self.image_meta_dict)
        actual_obj = ImageMeta.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)

    def test_image_meta_missing_attribute_json(self):
        modified_dict = self.image_meta_dict.copy()
        modified_dict.pop('os_type')

        actual_json = json.dumps(modified_dict)
        actual_obj = ImageMeta.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_image_meta_extra_attribute_json(self):
        modified_dict = self.image_meta_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = ImageMeta.deserialize(actual_json, 'json')
        self.assertIsNotNone(actual_obj)


class InstanceExceptionTest(BaseCommonTest):

    def test_instance_exception_json(self):
        expected_obj = self.instance_exception_obj

        actual_json = json.dumps(self.instance_exception_dict)
        actual_obj = InstanceException.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)

    def test_instance_exception_missing_attribute_json(self):
        modified_dict = self.instance_exception_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = InstanceException.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_instance_exception_extra_attribute_json(self):
        modified_dict = self.instance_exception_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = InstanceException.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)
