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
from cloudcafe.blockstorage.volumes_api.v2.client import VolumesClient
from cloudcafe.blockstorage.volumes_api.v2.config import VolumesAPIConfig
from cloudcafe.blockstorage.volumes_api.v2.models import statuses


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

        resp = self.client.create_volume(
            size, volume_type, name=name, description=description,
            availability_zone=availability_zone, metadata=metadata,
            bootable=bootable, image_ref=image_ref, snapshot_id=snapshot_id,
            source_volid=source_volid)

        return resp

    @behavior(VolumesClient)
    def create_snapshot(
            self, volume_id, name=None, description=None,
            force_create=False, requestslib_kwargs=None):

        resp = self.client.create_snapshot(
            volume_id, name=name, description=description,
            force_create=force_create)

        return resp

    @behavior(VolumesClient)
    def get_volume_status(self, volume_id):
        return super(VolumesAPI_Behaviors, self).get_volume_status(volume_id)

    @behavior(VolumesClient)
    def wait_for_volume_status(
            self, volume_id, expected_status, timeout, poll_rate=None):
        return super(VolumesAPI_Behaviors, self).wait_for_volume_status(
            volume_id, expected_status, timeout, poll_rate)

    @behavior(VolumesClient)
    def get_snapshot_status(self, snapshot_id):
        return super(VolumesAPI_Behaviors, self).get_snapshot_status(
            snapshot_id)

    @behavior(VolumesClient)
    def wait_for_snapshot_status(
            self, snapshot_id, expected_status, timeout, poll_rate=None):
        return super(VolumesAPI_Behaviors, self).wait_for_snapshot_status(
            snapshot_id, expected_status, timeout, poll_rate)

    @behavior(VolumesClient)
    def create_available_volume(
            self, size, volume_type, name=None, description=None,
            availability_zone=None, metadata=None, bootable=None,
            image_ref=None, snapshot_id=None, source_volid=None, timeout=None):
        return super(VolumesAPI_Behaviors, self).create_available_volume(
            size, volume_type, name=name, description=description,
            availability_zone=availability_zone, metadata=metadata,
            bootable=bootable, image_ref=image_ref, snapshot_id=snapshot_id,
            source_volid=source_volid, timeout=timeout)

    @behavior(VolumesClient)
    def create_available_snapshot(
            self, volume_id, name=None, description=None, force_create=True,
            timeout=None):
        return super(VolumesAPI_Behaviors, self).create_available_snapshot(
            volume_id, name, description, force_create, timeout)

    @behavior(VolumesClient)
    def list_volume_snapshots(self, volume_id):
        return super(VolumesAPI_Behaviors, self).list_volume_snapshots(
            volume_id)

    @behavior(VolumesClient)
    def delete_volume_confirmed(
            self, volume_id, size=None, timeout=None, poll_rate=None):
        return super(VolumesAPI_Behaviors, self).delete_volume_confirmed(
            volume_id, size, timeout, poll_rate)

    @behavior(VolumesClient)
    def delete_snapshot_confirmed(
            self, snapshot_id, vol_size=None, timeout=None, poll_rate=None):
        return super(VolumesAPI_Behaviors, self).delete_snapshot_confirmed(
            snapshot_id, vol_size, timeout, poll_rate)

    @behavior(VolumesClient)
    def delete_volume_with_snapshots_confirmed(self, volume_id):
        return super(VolumesAPI_Behaviors, self)\
            .delete_volume_with_snapshots_confirmed(volume_id)
