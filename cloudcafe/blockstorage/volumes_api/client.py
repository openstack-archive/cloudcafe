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
from cloudcafe.blockstorage.volumes_api.models.requests.volumes_api import \
    Volume as VolumeRequest, VolumeSnapshot as VolumeSnapshotRequest\

from cloudcafe.blockstorage.volumes_api.models.responses.volumes_api import \
    Volume as VolumeResponse, VolumeSnapshot as VolumeSnapshotResponse,\
    VolumeType, VolumeList, VolumeTypeList, VolumeSnapshotList


class VolumesClient(AutoMarshallingRestClient):
    def __init__(
            self, url, auth_token, tenant_id, serialize_format=None,
            deserialize_format=None):

        super(VolumesClient, self).__init__(
            serialize_format, deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/%s' % \
                                               self.serialize_format
        self.default_headers['Accept'] = 'application/%s' % \
                                         self.deserialize_format

    def create_volume(
            self, display_name, size, volume_type, availability_zone=None,
            metadata={}, display_description='', snapshot_id=None,
            requestslib_kwargs=None):

        '''POST v1/{tenant_id}/volumes'''

        url = '{0}/volumes'.format(self.url)

        volume_request_entity = VolumeRequest(
            display_name=display_name,
            size=size,
            volume_type=volume_type,
            display_description=display_description,
            metadata=metadata,
            availability_zone=availability_zone,
            snapshot_id=snapshot_id)

        return self.request(
            'POST', url, response_entity_type=VolumeResponse,
            request_entity=volume_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def create_volume_from_snapshot(
            self, snapshot_id, size, display_name='', volume_type=None,
            availability_zone=None, display_description='', metadata={},
            requestslib_kwargs=None):

        '''POST v1/{tenant_id}/volumes'''

        url = '{0}/volumes'.format(self.url)

        volume_request_entity = VolumeRequest(
            display_name=display_name,
            size=size,
            volume_type=volume_type,
            display_description=display_description,
            metadata=metadata,
            availability_zone=availability_zone,
            snapshot_id=snapshot_id)

        return self.request(
            'POST', url, response_entity_type=VolumeResponse,
            request_entity=volume_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_volumes(self, requestslib_kwargs=None):

        '''GET v1/{tenant_id}/volumes'''

        url = '{0}/volumes'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=VolumeList,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_volumes_info(self, requestslib_kwargs=None):

        '''GET v1/{tenant_id}/volumes/detail'''

        url = '{0}/volumes/detail'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=VolumeList,
            requestslib_kwargs=requestslib_kwargs)

    def get_volume_info(self, volume_id, requestslib_kwargs=None):

        '''GET v1/{tenant_id}/volumes/{volume_id}'''

        url = '{0}/volumes/{1}'.format(self.url, volume_id)
        return self.request(
            'GET', url, response_entity_type=VolumeResponse,
            requestslib_kwargs=requestslib_kwargs)

    def delete_volume(self, volume_id, requestslib_kwargs=None):

        '''DELETE v1/{tenant_id}/volumes/{volume_id}'''

        url = '{0}/volumes/{1}'.format(self.url, volume_id)
        return self.request(
            'DELETE', url, response_entity_type=VolumeResponse,
            requestslib_kwargs=requestslib_kwargs)

#Volume Types API
    def list_all_volume_types(self, requestslib_kwargs=None):

        '''GET v1/{tenant_id}/types '''

        url = '{0}/types'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=VolumeTypeList,
            requestslib_kwargs=requestslib_kwargs)

    def get_volume_type_info(self, volume_type_id, requestslib_kwargs=None):

        '''GET v1/{tenant_id}/types/{volume_type_id}'''

        url = '{0}/types/{1}'.format(self.url, volume_type_id)
        return self.request(
            'GET', url, response_entity_type=VolumeType,
            requestslib_kwargs=requestslib_kwargs)

#Volume Snapshot API
    def create_snapshot(
            self, volume_id, display_name=None, display_description=None,
            force_create=False, name=None, requestslib_kwargs=None):

        '''POST v1/{tenant_id}/snapshots'''

        url = '{0}/snapshots'.format(self.url)

        volume_snapshot_request_entity = VolumeSnapshotRequest(
            volume_id,
            force=force_create,
            display_name=display_name,
            name=name,
            display_description=display_description)

        return self.request(
            'POST', url, response_entity_type=VolumeSnapshotResponse,
            request_entity=volume_snapshot_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_snapshots(self, requestslib_kwargs=None):

        '''GET v1/{tenant_id}/snapshots'''

        url = '{0}/snapshots'.format(self.url)

        return self.request(
            'GET', url, response_entity_type=VolumeSnapshotList,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_snapshots_info(self, requestslib_kwargs=None):

        '''GET v1/{tenant_id}/snapshots/detail'''

        url = '{0}/snapshots/detail'.format(self.url)
        return self.request(
            'GET', url, response_entity_type=VolumeSnapshotList,
            requestslib_kwargs=requestslib_kwargs)

    def get_snapshot_info(self, snapshot_id, requestslib_kwargs=None):

        '''GET v1/{tenant_id}/snapshots/{snapshot_id}'''

        url = '{0}/snapshots/{1}'.format(self.url, snapshot_id)

        return self.request(
            'GET', url, response_entity_type=VolumeSnapshotResponse,
            requestslib_kwargs=requestslib_kwargs)

    def delete_snapshot(self, snapshot_id, requestslib_kwargs=None):

        '''DELETE v1/{tenant_id}/snapshots/{snapshot_id}'''

        url = '{0}/snapshots/{1}'.format(self.url, snapshot_id)
        return self.request(
            'DELETE', url, response_entity_type=VolumeSnapshotResponse,
            requestslib_kwargs=requestslib_kwargs)

