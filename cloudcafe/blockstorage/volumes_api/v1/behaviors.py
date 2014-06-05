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
from cafe.engine.behaviors import behavior
from cloudcafe.blockstorage.volumes_api.common.behaviors import \
    VolumesAPI_CommonBehaviors
from cloudcafe.blockstorage.volumes_api.v1.client import VolumesClient
from cloudcafe.blockstorage.volumes_api.v1.config import VolumesAPIConfig
from cloudcafe.blockstorage.volumes_api.v1.models import statuses


class VolumesAPI_Behaviors(VolumesAPI_CommonBehaviors):
    statuses = statuses

    def __init__(self, volumes_api_client=None, volumes_api_config=None):
        super(VolumesAPI_Behaviors, self).__init__()
        self.client = volumes_api_client
        self.config = volumes_api_config or VolumesAPIConfig()

    @behavior(VolumesClient)
    def create_volume(
            self, size, volume_type, name=None, description=None,
            availability_zone=None, metadata=None, bootable=None,
            image_ref=None, snapshot_id=None, source_volid=None):
        """Normalizes call to accept name and description so that
        v1 and v2 behaviors are the same
        """

        resp = self.client.create_volume(
            size, volume_type, display_name=name, metadata=metadata,
            display_description=description, bootable=bootable,
            image_ref=image_ref, availability_zone=availability_zone,
            snapshot_id=snapshot_id, source_volid=source_volid)

        return resp

    @behavior(VolumesClient)
    def create_snapshot(
            self, volume_id, name=None, description=None,
            force_create=False, requestslib_kwargs=None):
        """Normalizes call to accept name and description so that
        v1 and v2 behaviors are the same
        """

        resp = self.client.create_snapshot(
            volume_id, display_name=name, display_description=description,
            force_create=force_create)

        return resp
