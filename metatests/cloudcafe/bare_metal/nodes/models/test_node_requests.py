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

import json
import unittest

from cloudcafe.bare_metal.nodes.models.requests import (
    CreateNode, SetNodePowerState, SetNodeConsoleMode)


class CreateNodeModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        node_request = CreateNode(
            chassis_uuid='1', driver='fake', properties={'key1': 'val1'},
            driver_info={'key3': 'val3'}, extra={'key2': 'val2'})
        cls.node_json = node_request.serialize('json')

    def test_create_node_json(self):
        expected_json = (
            '{"driver_info": {"key3": "val3"}, "driver": "fake", '
            '"properties": {"key1": "val1"}, "chassis_uuid": "1", '
            '"extra": {"key2": "val2"}}')
        self.assertEqual(self.node_json, expected_json)


class SetNodePowerStateModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        power_state_request = SetNodePowerState(power_state='off')
        cls.request_json = power_state_request.serialize('json')

    def test_set_node_power_state_json(self):
        expected_json = json.dumps({'target': 'off'})
        self.assertEqual(self.request_json, expected_json)


class SetNodeConsoleModeModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        console_mode_request = SetNodeConsoleMode(enabled=True)
        cls.request_json = console_mode_request.serialize('json')

    def test_set_node_console_mode_json(self):
        expected_json = json.dumps({'enabled': True})
        self.assertEqual(self.request_json, expected_json)
