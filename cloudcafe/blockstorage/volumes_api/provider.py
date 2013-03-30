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

from cafe.engine.provider import BaseProvider

from cloudcafe.blockstorage.volumes_api.config import VolumesAPIConfig
from cloudcafe.blockstorage.volumes_api.behaviors import VolumesBehaviors
from cloudcafe.blockstorage.volumes_api.client import VolumesClient


class VolumesProvider(BaseProvider):

    def __init__(self, url, auth_token, tenant_id):

        volumes_config = VolumesAPIConfig()
        serialize_format = volumes_config.serialize_format
        deserialize_format = volumes_config.deserialize_format

        self.client = VolumesClient(
            url, auth_token, tenant_id, serialize_format=serialize_format,
            deserialize_format=deserialize_format)
        self.behaviors = VolumesBehaviors(self.client)
