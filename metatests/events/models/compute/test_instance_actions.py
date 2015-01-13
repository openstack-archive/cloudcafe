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

from cloudcafe.events.models.compute.instance_actions import (
    ComputeInstanceCreate, ComputeInstanceDelete, ComputeInstanceRebuild,
    ComputeInstanceResizePrep)


class BaseInstanceActionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseInstanceActionsTest, cls).setUpClass()

        cls.fixed_ip_dict = {
            'floating_ips': [],
            'meta': {},
            'type': 'fixed',
            'version': 4,
            'address': '10.10.0.0',
            'label': 'public'
        }

        cls.base_instance_dict = {
            'tenant_id': '123456',
            'user_id': 'some_user',
            'instance_id': 'some_uuid',
            'instance_type': 'flavor name',
            'instance_type_id': 'flavor id',
            'display_name': 'a display name',
            'created_at': '2015-01-09 21:26:54',
            'launched_at': '2015-01-09 21:27:54',
            'image_ref_url': 'url.example',
            'state': 'active',
            'state_description': 'state description',
            'fixed_ips': [cls.fixed_ip_dict],
            'memory_mb': 1024,
            'disk_gb': 20,
        }

        cls.instance_create_dict = cls.base_instance_dict.copy()
        cls.instance_create_dict['message'] = 'descriptive message'

        cls.instance_resize_prep_dict = cls.base_instance_dict.copy()
        cls.instance_resize_prep_dict['new_instance_type'] = 'new type'
        cls.instance_resize_prep_dict['new_instance_type_id'] = 'new id'

        cls.instance_create_obj = ComputeInstanceCreate._dict_to_obj(
            cls.instance_create_dict)
        cls.instance_delete_obj = ComputeInstanceDelete._dict_to_obj(
            cls.base_instance_dict)
        cls.instance_rebuild_obj = ComputeInstanceRebuild._dict_to_obj(
            cls.base_instance_dict)
        cls.instance_resize_prep_obj = ComputeInstanceResizePrep._dict_to_obj(
            cls.instance_resize_prep_dict)


class InstanceCreateTest(BaseInstanceActionsTest):

    def test_instance_create_valid_json(self):
        expected_obj = self.instance_create_obj

        actual_json = json.dumps(self.instance_create_dict)
        actual_obj = ComputeInstanceCreate.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_instance_create_missing_attribute_json(self):
        modified_dict = self.instance_create_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = ComputeInstanceCreate.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_instance_create_extra_attribute_json(self):
        modified_dict = self.instance_create_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = ComputeInstanceCreate.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)


class InstanceDeleteTest(BaseInstanceActionsTest):

    def test_instance_delete_valid_json(self):
        expected_obj = self.instance_delete_obj

        actual_json = json.dumps(self.base_instance_dict)
        actual_obj = ComputeInstanceDelete.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_instance_delete_missing_attribute_json(self):
        modified_dict = self.base_instance_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = ComputeInstanceDelete.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_instance_delete_extra_attribute_json(self):
        modified_dict = self.base_instance_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = ComputeInstanceDelete.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)


class InstanceRebuildTest(BaseInstanceActionsTest):

    def test_instance_rebuild_valid_json(self):
        expected_obj = self.instance_rebuild_obj

        actual_json = json.dumps(self.base_instance_dict)
        actual_obj = ComputeInstanceRebuild.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_instance_rebuild_missing_attribute_json(self):
        modified_dict = self.base_instance_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = ComputeInstanceRebuild.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_instance_rebuild_extra_attribute_json(self):
        modified_dict = self.base_instance_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = ComputeInstanceRebuild.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)


class InstanceResizePrepTest(BaseInstanceActionsTest):

    def test_instance_resize_prep_valid_json(self):
        expected_obj = self.instance_resize_prep_obj

        actual_json = json.dumps(self.instance_resize_prep_dict)
        actual_obj = ComputeInstanceResizePrep.deserialize(actual_json, 'json')

        self.assertEqual(expected_obj, actual_obj)
        self.assertFalse(actual_obj.is_empty())

    def test_instance_resize_prep_missing_attribute_json(self):
        modified_dict = self.instance_resize_prep_dict.copy()
        modified_dict.popitem()

        actual_json = json.dumps(modified_dict)
        actual_obj = ComputeInstanceResizePrep.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)

    def test_instance_resize_prep_extra_attribute_json(self):
        modified_dict = self.instance_resize_prep_dict.copy()
        modified_dict['test_dummy'] = 'test_dummy'

        actual_json = json.dumps(modified_dict)
        actual_obj = ComputeInstanceResizePrep.deserialize(actual_json, 'json')
        self.assertIsNone(actual_obj)
