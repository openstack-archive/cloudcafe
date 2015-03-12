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

from collections import OrderedDict
from mock import MagicMock, Mock
from requests import Response
import sys
import unittest

from cafe.common.reporting import cclogging
from cafe.configurator.managers import _lazy_property
cclogging.init_root_log_handler()
from cloudcafe.common.behaviors import StatusProgressionVerifierError
from cloudcafe.compute.volume_attachments_api.behaviors import \
    VolumeAttachmentsAPI_Behaviors
from cloudcafe.compute.volume_attachments_api.client import \
    VolumeAttachmentsAPIClient
from cloudcafe.compute.volume_attachments_api.config import \
    VolumeAttachmentsAPIConfig
from cloudcafe.blockstorage.volumes_api.v2.client import \
    VolumesClient
from cloudcafe.blockstorage.volumes_api.v2.models.responses import \
    VolumeResponse

class MockBuilder(object):

    def _mock(self, name, **defaults):
        defaults.update(**self._overrides.get(name, {}))
        setattr(self, name, Mock(**defaults))


class TestMocks(MockBuilder):

    def __init__(self, **kwargs):
        self._overrides = kwargs
        self._mock(
            'volume_model', spec=VolumeResponse, status='in-use', id_='111111')
        self._mock(
            'response', spec=Response, ok=True, entity=self.volume_model)
        self._mock(
            'volumes_client', spec=VolumesClient,
            get_volume_info=MagicMock(return_value=self.response))
        self._mock(
            'volume_attachments_client', spec=VolumeAttachmentsAPIClient)
        self._mock(
            'volume_attachments_config', spec=VolumeAttachmentsAPIConfig,
            attachment_timeout=1, api_poll_rate=1)

class BaseTestCase(object):
    mocks = TestMocks()

    def behavior_class_under_test(self):
        return VolumeAttachmentsAPI_Behaviors(
            self.mocks.volume_attachments_client,
            self.mocks.volume_attachments_config,
            self.mocks.volumes_client)

    def setUp(self):
        self.behaviors = self.behavior_class_under_test()


class MethodTests_verify_volume_status_progression_during_attachment(
        BaseTestCase, unittest.TestCase):

    def test_volume_is_attached(self):
        r = self.behaviors.verify_volume_status_progression_during_attachment(
            self.mocks.volume_model.id_)


class MethodTests_verify_volume_status_progression_during_detachment(
    BaseTestCase, unittest.TestCase):
    mocks = TestMocks(volume_model=dict(status='available'))

    def test_volume_is_detached(self):
        r = self.behaviors.verify_volume_status_progression_during_detachment(
            self.mocks.volume_model.id_)
