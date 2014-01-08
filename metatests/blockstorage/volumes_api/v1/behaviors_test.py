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

from cloudcafe.blockstorage.volumes_api.v1.behaviors import \
    VolumesAPI_Behaviors, VolumesAPIBehaviorException
from cloudcafe.blockstorage.volumes_api.v1.models.responses import\
    VolumeResponse, VolumeSnapshotResponse
from cloudcafe.blockstorage.volumes_api.v1.client import VolumesClient
from cloudcafe.blockstorage.volumes_api.v1.config import VolumesAPIConfig


class wait_for_snapshot_status(unittest.TestCase):

    class defaults:
        snapshot_name = 'mock_snapshot'
        snapshot_id = '111111'
        expected_status = 'available'
        timeout = 10
        poll_rate = 2

    def test_wait_for_snapshot_status_good_response_code(self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.snapshot_status_poll_frequency = 1

        snapshot_model = Mock(spec=VolumeSnapshotResponse)
        snapshot_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = snapshot_model

        client.get_snapshot_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        resp = behavior.wait_for_snapshot_status(
            self.defaults.snapshot_id, self.defaults.expected_status,
            self.defaults.timeout, poll_rate=self.defaults.poll_rate)

        self.assertIsNone(resp)

    def test_wait_for_snapshot_status_good_response_code_config_wait_period(
            self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.snapshot_status_poll_frequency = 1

        snapshot_model = Mock(spec=VolumeSnapshotResponse)
        snapshot_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = snapshot_model

        client.get_snapshot_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        resp = behavior.wait_for_snapshot_status(
            self.defaults.snapshot_name, self.defaults.expected_status,
            self.defaults.timeout)

        self.assertIsNone(resp)

    def test_wait_for_snapshot_status_good_response_code_bad_status(self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.snapshot_status_poll_frequency = 1

        snapshot_model = Mock(spec=VolumeSnapshotResponse)
        snapshot_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = snapshot_model

        client.get_snapshot_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        resp = behavior.wait_for_snapshot_status(
            self.defaults.snapshot_name, self.defaults.expected_status,
            self.defaults.timeout, poll_rate=self.defaults.poll_rate)

        self.assertIsNone(resp)

    def test_wait_for_snapshot_status_bad_response_code(self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.snapshot_status_poll_frequency = 1

        snapshot_model = Mock(spec=VolumeSnapshotResponse)
        snapshot_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = False
        response.entity = snapshot_model
        response.status_code = '401'

        client.get_snapshot_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_snapshot_status(
                self.defaults.snapshot_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)

    def test_wait_for_snapshot_status_good_response_code_empty_entity(self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.snapshot_status_poll_frequency = 1

        snapshot_model = Mock(spec=VolumeSnapshotResponse)
        snapshot_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = None
        response.status_code = '200'

        client.get_snapshot_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_snapshot_status(
                self.defaults.snapshot_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)

    def test_wait_for_snapshot_status_good_response_and_entity_bad_status(
            self):
        recieved_status = 'error'

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.snapshot_status_poll_frequency = 1

        snapshot_model = Mock(spec=VolumeSnapshotResponse)
        snapshot_model.status = recieved_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = snapshot_model

        client.get_snapshot_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_snapshot_status(
                self.defaults.snapshot_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)


class wait_for_volume_status(unittest.TestCase):

    class defaults:
        volume_id = '111111'
        volume_name = 'mock_volume'
        expected_status = 'available'
        timeout = 10
        poll_rate = 2
        timeout = 10

    def test_wait_for_volume_status_good_response_code(self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.volume_status_poll_frequency = 1

        volume_model = Mock(spec=VolumeResponse)
        volume_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = volume_model

        client.get_volume_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        resp = behavior.wait_for_volume_status(
            self.defaults.volume_id, self.defaults.expected_status,
            self.defaults.timeout, poll_rate=self.defaults.poll_rate)

        self.assertIsNone(resp)

    def test_wait_for_volume_status_good_response_code_configured_poll_rate(
            self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.volume_status_poll_frequency = 1

        volume_model = Mock(spec=VolumeResponse)
        volume_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = volume_model

        client.get_volume_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        resp = behavior.wait_for_volume_status(
            self.defaults.volume_name, self.defaults.expected_status,
            self.defaults.timeout)

        self.assertIsNone(resp)

    def test_wait_for_volume_status_good_response_code_bad_status(self):
        volume_name = 'mock_volume'
        expected_status = 'available'
        timeout = 10
        poll_rate = 2

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.volume_status_poll_frequency = 1

        volume_model = Mock(spec=VolumeResponse)
        volume_model.status = expected_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = volume_model

        client.get_volume_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        resp = behavior.wait_for_volume_status(
            volume_name, expected_status, timeout, poll_rate=poll_rate)

        self.assertIsNone(resp)

    def test_wait_for_volume_status_bad_response_code(self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.volume_status_poll_frequency = 1

        volume_model = Mock(spec=VolumeResponse)
        volume_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = False
        response.entity = volume_model
        response.status_code = '401'

        client.get_volume_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_volume_status(
                self.defaults.volume_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)

    def test_wait_for_volume_status_good_response_code_empty_entity(self):

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.volume_status_poll_frequency = 1

        volume_model = Mock(spec=VolumeResponse)
        volume_model.status = self.defaults.expected_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = None
        response.status_code = '200'

        client.get_volume_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_volume_status(
                self.defaults.volume_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)

    def test_wait_for_volume_status_good_response_and_entity_bad_status(self):
        recieved_status = 'error'

        client = Mock(spec=VolumesClient)

        config = Mock(spec=VolumesAPIConfig)
        config.volume_status_poll_frequency = 1

        volume_model = Mock(spec=VolumeResponse)
        volume_model.status = recieved_status

        response = Mock(spec=Response)
        response.ok = True
        response.entity = volume_model

        client.get_volume_info = MagicMock(
            return_value=response)

        behavior = VolumesAPI_Behaviors(client, config)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.wait_for_volume_status(
                self.defaults.volume_name, self.defaults.expected_status,
                self.defaults.timeout, poll_rate=self.defaults.poll_rate)


class create_available_volume(unittest.TestCase):

    class defaults:
        display_name = "mock_volume"
        volume_type = "mock_type"
        size = 1

    def test_create_availabe_volume_happy_path(self):

        volume_model = Mock(spec=VolumeResponse)
        volume_model.id_ = "mock"
        volume_create_response = Mock(spec=Response)
        volume_create_response.entity = volume_model
        volume_create_response.ok = True

        client = Mock(spec=VolumesClient)
        client.create_volume = MagicMock(return_value=volume_create_response)
        config = Mock(spec=VolumesAPIConfig)
        config.volume_create_timeout = 5
        behavior = VolumesAPI_Behaviors(client, config)
        behavior.wait_for_volume_status = MagicMock(return_value=None)

        volume_entity = behavior.create_available_volume(
            self.defaults.display_name, self.defaults.size,
            self.defaults.volume_type)
        self.assertIsInstance(volume_entity, VolumeResponse)

    def test_create_available_volume_failure_response_no_model(self):

        volume_model = Mock(spec=VolumeResponse)
        volume_model.id_ = "mock"
        volume_create_response = Mock(spec=Response)
        volume_create_response.entity = None
        volume_create_response.ok = False
        volume_create_response.status_code = 500

        client = Mock(spec=VolumesClient)
        client.create_volume = MagicMock(return_value=volume_create_response)
        config = Mock(spec=VolumesAPIConfig)
        config.volume_create_timeout = 5
        behavior = VolumesAPI_Behaviors(client, config)
        behavior.wait_for_volume_status = MagicMock(return_value=None)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.create_available_volume(
                self.defaults.display_name, self.defaults.size,
                self.defaults.volume_type)

    def test_create_available_volume_failure_response_with_model(self):

        volume_model = Mock(spec=VolumeResponse)
        volume_model.id_ = "mock"
        volume_create_response = Mock(spec=Response)
        volume_create_response.entity = None
        volume_create_response.ok = True
        volume_create_response.status_code = 200

        client = Mock(spec=VolumesClient)
        client.create_volume = MagicMock(return_value=volume_create_response)
        config = Mock(spec=VolumesAPIConfig)
        config.volume_create_timeout = 5
        behavior = VolumesAPI_Behaviors(client, config)
        behavior.wait_for_volume_status = MagicMock(return_value=None)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.create_available_volume(
                self.defaults.display_name, self.defaults.size,
                self.defaults.volume_type)

    def test_create_available_volume_timeout_failure(self):

        volume_model = Mock(spec=VolumeResponse)
        volume_model.id_ = "mock"
        volume_create_response = Mock(spec=Response)
        volume_create_response.entity = None
        volume_create_response.ok = True
        volume_create_response.status_code = 200

        client = Mock(spec=VolumesClient)
        client.create_volume = MagicMock(return_value=volume_create_response)
        config = Mock(spec=VolumesAPIConfig)
        config.volume_create_timeout = 5
        behavior = VolumesAPI_Behaviors(client, config)
        behavior.wait_for_volume_status = MagicMock(
            side_effect=VolumesAPIBehaviorException)

        with self.assertRaises(VolumesAPIBehaviorException):
            behavior.create_available_volume(
                self.defaults.display_name, self.defaults.size,
                self.defaults.volume_type)
