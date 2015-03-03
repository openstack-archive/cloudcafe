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

from cloudcafe.compute.events.models.instance_delete import (
    InstanceDeleteStart, InstanceDeleteEnd)


class BaseInstanceActionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseInstanceActionsTest, cls).setUpClass()

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

        cls.base_instance_delete_dict = {
            "access_ip_v4": "10.10.0.0",
            "access_ip_v6": None,
            "architecture": "x64",
            "availability_zone": None,
            "cell_name": "cell name",
            "created_at": "2015-01-15 18:59:29",
            "deleted_at": "",
            "disk_gb": 20,
            "display_name": "server123456",
            "ephemeral_gb": 0,
            "host": None,
            "hostname": "server123456",
            "image_meta": cls.image_meta_dict,
            "image_ref_url": "http://127.0.0.1/images/my_image",
            "instance_flavor_id": "instance_flavor_id",
            "instance_id": "performance1-1",
            "instance_type": "1 GB Performance",
            "instance_type_id": "9",
            "kernel_id": "",
            "launched_at": "",
            "memory_mb": 1024,
            "metadata": {},
            "node": None,
            "os_type": "linux",
            "progress": "",
            "ramdisk_id": "",
            "reservation_id": "r-abcdefg",
            "root_gb": 20,
            "state": "building",
            "state_description": "",
            "tenant_id": "123456",
            "terminated_at": "",
            "user_id": "123456789",
            "vcpus": 1
        }

        cls.instance_delete_start_obj = InstanceDeleteStart._dict_to_obj(
            cls.base_instance_delete_dict)
        cls.instance_delete_end_obj = InstanceDeleteEnd._dict_to_obj(
            cls.base_instance_delete_dict)


class InstanceDeleteStartTest(BaseInstanceActionsTest):

    def test_instance_delete_start_valid_json(self):
        """Verify that the valid event deserialized correctly"""
        expected_obj = self.instance_delete_start_obj

        actual_json = json.dumps(self.base_instance_delete_dict)
        actual_obj = InstanceDeleteStart.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_instance_delete_start_missing_attribute_json(self):
        """Verify event missing expected attribute does not deserialize"""
        modified_dict = self.base_instance_delete_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = InstanceDeleteStart.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_instance_delete_start_extra_attribute_json(self):
        """Verify event with unexpected attribute does not deserialize"""
        modified_dict = self.base_instance_delete_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = InstanceDeleteStart.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)


class InstanceDeleteEndTest(BaseInstanceActionsTest):

    def test_instance_delete_end_valid_json(self):
        """Verify that the valid event deserialized correctly"""
        expected_obj = self.instance_delete_end_obj

        actual_json = json.dumps(self.base_instance_delete_dict)
        actual_obj = InstanceDeleteEnd.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_instance_delete_end_missing_attribute_json(self):
        """Verify event missing expected attribute does not deserialize"""
        modified_dict = self.base_instance_delete_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = InstanceDeleteEnd.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_instance_delete_end_extra_attribute_json(self):
        """Verify event with unexpected attribute does not deserialize"""
        modified_dict = self.base_instance_delete_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = InstanceDeleteEnd.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)
