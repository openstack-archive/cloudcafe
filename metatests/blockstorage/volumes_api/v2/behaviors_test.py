"""
Copyright 2013 Rackspace

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
from mock import MagicMock, Mock
from requests import Response

from cloudcafe.blockstorage.volumes_api.common.behaviors import \
    VolumesAPIBehaviorException
from cloudcafe.blockstorage.volumes_api.v2.behaviors import \
    VolumesAPI_Behaviors
from cloudcafe.blockstorage.volumes_api.v2.models.responses import\
    VolumeResponse, VolumeSnapshotResponse
from cloudcafe.blockstorage.volumes_api.v2.client import VolumesClient
from cloudcafe.blockstorage.volumes_api.common.config import VolumesAPIConfig


class wait_for_snapshot_status(unittest.TestCase):

    class defaults:
        snapshot_id = '111111'
        snapshot_name = 'mock_snapshot'
        expected_status = 'available'
        timeout = 10
        poll_rate = 2

    def get_mocks(self):
        client = Mock(spec=VolumesClient)
        config = Mock(spec=VolumesAPIConfig)
        snapshot_model = Mock(spec=VolumeSnapshotResponse)
        response = Mock(spec=Response)

        config.snapshot_status_poll_frequency = 1
        response.ok = True
        snapshot_model.status = self.defaults.expected_status
        response.entity = snapshot_model
        client.get_snapshot_info = MagicMock(return_value=response)
        return (client, config, snapshot_model, response)

    def test_good_response_code_manual_poll_rate(self):
        client, config, snapshot_model, response = self.get_mocks()

        behavior = VolumesAPI_Behaviors(client, config)
        resp = behavior.wait_for_snapshot_status(
            self.defaults.snapshot_id, self.defaults.expected_status,
            self.defaults.timeout, poll_rate=self.defaults.poll_rate)

        self.assertIsNone(resp)

    def test_good_response_code_config_wait_period(self):
        client, config, snapshot_model, response = self.get_mocks()

        behavior = VolumesAPI_Behaviors(client, config)
        resp = behavior.wait_for_snapshot_status(
            self.defaults.snapshot_name, self.defaults.expected_status,
            self.defaults.timeout)

        self.assertIsNone(resp)

    def test_good_response_code_bad_status(self):
        client, config, snapshot_model, response = self.get_mocks()

        behavior = VolumesAPI_Behaviors(client, config)
        resp = behavior.wait_for_snapshot_status(
            self.defaults.snapshot_name, self.defaults.expected_status,
            self.defaults.timeout, poll_rate=self.defaults.poll_rate)

        self.assertIsNone(resp)

    def test_bad_response_code(self):
        client, config, snapshot_model, response = self.get_mocks()

        response.ok = False
        response.entity = snapshot_model
        response.status_code = '401'
        client.get_snapshot_info = MagicMock(return_value=response)
        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_snapshot_status(
                self.defaults.snapshot_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)

    def test_good_response_code_empty_entity(self):
        client, config, snapshot_model, response = self.get_mocks()

        response.entity = None
        response.status_code = '200'
        client.get_snapshot_info = MagicMock(return_value=response)
        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_snapshot_status(
                self.defaults.snapshot_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)

    def test_good_response_good_entity_bad_status(self):
        client, config, snapshot_model, response = self.get_mocks()

        recieved_status = 'error'
        poll_rate = 1
        snapshot_model.status = recieved_status
        response.entity = snapshot_model
        client.get_snapshot_info = MagicMock(return_value=response)
        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_snapshot_status(
                self.defaults.snapshot_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=poll_rate)


class wait_for_volume_status(unittest.TestCase):

    class defaults:
        volume_id = '111111'
        volume_name = 'mock_volume'
        expected_status = 'available'
        timeout = 10
        poll_rate = 2

    def get_mocks(self):
        client = Mock(spec=VolumesClient)
        config = Mock(spec=VolumesAPIConfig)
        volume_model = Mock(spec=VolumeResponse)
        response = Mock(spec=Response)

        config.volume_status_poll_frequency = 1
        volume_model.status = self.defaults.expected_status
        response.ok = True
        response.entity = volume_model
        client.get_volume_info = MagicMock(return_value=response)

        return (client, config, volume_model, response)

    def test_get_volume_status(self):
        client, config, volume_model, response = self.get_mocks()

        behavior = VolumesAPI_Behaviors(client, config)

        status = behavior.get_volume_status(self.defaults.volume_id)
        self.assertEqual(status, self.defaults.expected_status)

    def test_good_response_code(self):
        client, config, volume_model, response = self.get_mocks()

        behavior = VolumesAPI_Behaviors(client, config)

        resp = behavior.wait_for_volume_status(
            self.defaults.volume_id, self.defaults.expected_status,
            self.defaults.timeout, poll_rate=self.defaults.poll_rate)

        self.assertIsNone(resp)

    def test_good_response_code_configured_poll_period(self):
        client, config, volume_model, response = self.get_mocks()

        behavior = VolumesAPI_Behaviors(client, config)
        resp = behavior.wait_for_volume_status(
            self.defaults.volume_name, self.defaults.expected_status,
            self.defaults.timeout)

        self.assertIsNone(resp)

    def test_good_response_code_bad_status(self):
        client, config, volume_model, response = self.get_mocks()

        behavior = VolumesAPI_Behaviors(client, config)
        resp = behavior.wait_for_volume_status(
            self.defaults.volume_name, self.defaults.expected_status,
            self.defaults.timeout, poll_rate=self.defaults.poll_rate)

        self.assertIsNone(resp)

    def test_bad_response_code(self):
        client, config, volume_model, response = self.get_mocks()

        response.ok = False
        response.entity = volume_model
        response.status_code = '401'
        client.get_volume_info = MagicMock(return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)
        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_volume_status(
                self.defaults.volume_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)

    def test_good_response_code_empty_entity(self):
        client, config, volume_model, response = self.get_mocks()

        response.entity = None
        response.status_code = '200'
        client.get_volume_info = MagicMock(return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)
        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_volume_status(
                self.defaults.volume_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)

    def test_good_response_and_entity_bad_status(self):
        client, config, volume_model, response = self.get_mocks()

        recieved_status = 'error'
        timeout = 2
        poll_rate = 1

        volume_model.status = recieved_status
        response.entity = volume_model
        client.get_volume_info = MagicMock(return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)
        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_volume_status(
                self.defaults.volume_name, self.defaults.expected_status,
                timeout, poll_rate=poll_rate)


class create_available_volume(unittest.TestCase):

    class defaults:
        display_name = "mock_volume"
        volume_type = "mock_type"
        size = 1

    def get_mocks(self):
        client = Mock(spec=VolumesClient)
        volume_model = Mock(spec=VolumeResponse)
        volume_create_response = Mock(spec=Response)
        volume_model.id_ = "mock"
        volume_create_response.entity = volume_model
        volume_create_response.ok = True
        client.create_volume = MagicMock(return_value=volume_create_response)

        config = Mock(spec=VolumesAPIConfig)
        config.serialize_format = "json"
        config.deserialize_format = "json"
        config.max_volume_size = 1024
        config.min_volume_size = 1
        config.volume_status_poll_frequency = 5
        config.volume_create_min_timeout = 1
        config.volume_create_max_timeout = 10
        config.volume_create_wait_per_gigabyte = 1
        config.volume_create_base_timeout = 0

        return (client, config, volume_model, volume_create_response)

    def test_happy_path(self):
        client, config, volume_model, volume_create_response = self.get_mocks()

        behavior = VolumesAPI_Behaviors(client, config)
        behavior.get_volume_status = MagicMock(return_value='available')

        volume_entity = behavior.create_available_volume(
            self.defaults.display_name, self.defaults.size,
            self.defaults.volume_type)

        self.assertIsInstance(volume_entity, VolumeResponse)

    def test_timeout_failure(self):
        client, config, volume_model, volume_create_response = self.get_mocks()

        volume_create_response.entity = None
        volume_create_response.status_code = 200

        client.create_volume = MagicMock(return_value=volume_create_response)

        behavior = VolumesAPI_Behaviors(client, config)
        behavior.wait_for_volume_status = MagicMock(
            side_effect=VolumesAPIBehaviorException)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.create_available_volume(
                self.defaults.display_name, self.defaults.size,
                self.defaults.volume_type)
