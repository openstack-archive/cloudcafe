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

from cafe.engine.clients.rest import AutoMarshallingRestClient

from cloudcafe.blockstorage.volumes_api.v1.models.requests import (
    VolumeRequest, VolumeSnapshotRequest)

from cloudcafe.blockstorage.volumes_api.v1.models.responses import (
    VolumeResponse, VolumeSnapshotResponse, VolumeTypeResponse,
    VolumeListResponse, VolumeTypeListResponse, VolumeSnapshotListResponse)


class VolumesClient(AutoMarshallingRestClient):
    def __init__(
            self, url, auth_token, serialize_format=None,
            deserialize_format=None):

        super(VolumesClient, self).__init__(
            serialize_format, deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

    def create_volume(
            self, size, volume_type, display_name=None,
            display_description=None, name=None, description=None,
            availability_zone=None, metadata=None, bootable=None,
            image_ref=None, snapshot_id=None, source_volid=None,
            requestslib_kwargs=None):

        """POST /volumes"""

        url = '{0}/volumes'.format(self.url)

        display_name = display_name or name
        display_description = display_description or description

        volume_request_entity = VolumeRequest(
            size=size, volume_type=volume_type, display_name=display_name,
            display_description=display_description, metadata=metadata,
            bootable=bootable, snapshot_id=snapshot_id,
            availability_zone=availability_zone, source_volid=source_volid,
            image_ref=image_ref)

        return self.request(
            'POST', url,
            response_entity_type=VolumeResponse,
            request_entity=volume_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_volumes(self, requestslib_kwargs=None):

        """GET /volumes"""

        url = '{0}/volumes'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=VolumeListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_volumes_info(self, requestslib_kwargs=None):

        """GET /volumes/detail"""

        url = '{0}/volumes/detail'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=VolumeListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def get_volume_info(self, volume_id, requestslib_kwargs=None):

        """GET /volumes/{volume_id}"""

        url = '{0}/volumes/{1}'.format(self.url, volume_id)
        return self.request(
            'GET', url, response_entity_type=VolumeResponse,
            requestslib_kwargs=requestslib_kwargs)

    def delete_volume(self, volume_id, requestslib_kwargs=None):

        """DELETE /volumes/{volume_id}"""

        url = '{0}/volumes/{1}'.format(self.url, volume_id)
        return self.request(
            'DELETE', url, response_entity_type=VolumeResponse,
            requestslib_kwargs=requestslib_kwargs)

    # Volume Types API
    def list_all_volume_types(self, requestslib_kwargs=None):

        """GET /types """

        url = '{0}/types'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=VolumeTypeListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def get_volume_type_info(self, volume_type_id, requestslib_kwargs=None):

        """GET /types/{volume_type_id}"""

        url = '{0}/types/{1}'.format(self.url, volume_type_id)
        return self.request(
            'GET', url, response_entity_type=VolumeTypeResponse,
            requestslib_kwargs=requestslib_kwargs)

    # Volume Snapshot API
    def create_snapshot(
            self, volume_id, display_name=None, display_description=None,
            name=None, description=None, force_create=False,
            requestslib_kwargs=None):

        """POST /snapshots"""

        url = '{0}/snapshots'.format(self.url)

        display_name = display_name or name
        display_description = display_description or description

        volume_snapshot_request_entity = VolumeSnapshotRequest(
            volume_id,
            force=force_create,
            display_name=display_name,
            display_description=display_description)

        return self.request(
            'POST', url,
            response_entity_type=VolumeSnapshotResponse,
            request_entity=volume_snapshot_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_snapshots(self, requestslib_kwargs=None):

        """GET /snapshots"""

        url = '{0}/snapshots'.format(self.url)

        return self.request(
            'GET', url, response_entity_type=VolumeSnapshotListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_snapshots_info(self, requestslib_kwargs=None):

        """GET /snapshots/detail"""

        url = '{0}/snapshots/detail'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=VolumeSnapshotListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def get_snapshot_info(self, snapshot_id, requestslib_kwargs=None):

        """GET /snapshots/{snapshot_id}"""

        url = '{0}/snapshots/{1}'.format(self.url, snapshot_id)

        return self.request(
            'GET', url, response_entity_type=VolumeSnapshotResponse,
            requestslib_kwargs=requestslib_kwargs)

    def delete_snapshot(self, snapshot_id, requestslib_kwargs=None):

        """Delete /snapshots/{snapshot_id} """

        url = '{0}/snapshots/{1}'.format(self.url, snapshot_id)
        return self.request(
            'DELETE', url, response_entity_type=VolumeSnapshotResponse,
            requestslib_kwargs=requestslib_kwargs)
