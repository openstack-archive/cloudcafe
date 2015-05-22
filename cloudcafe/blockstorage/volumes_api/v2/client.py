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
from cloudcafe.blockstorage.volumes_api.common.client import BaseVolumesClient
from cloudcafe.blockstorage.volumes_api.v2.models import \
    requests as _request_models
from cloudcafe.blockstorage.volumes_api.v2.models import \
    responses as _response_models


class VolumesClient(BaseVolumesClient):

    def __init__(
            self, url, auth_token, serialize_format=None,
            deserialize_format=None):

        super(VolumesClient, self).__init__(
            url, auth_token, serialize_format, deserialize_format)

    @property
    def request_models(self):
        return _request_models

    @property
    def response_models(self):
        return _response_models

    def create_volume(
            self, size, volume_type, name=None, description=None,
            display_name=None, display_description=None,
            availability_zone=None, metadata=None, bootable=None,
            image_ref=None, snapshot_id=None, source_volid=None,
            requestslib_kwargs=None):

        """POST /volumes"""

        url = '{0}/volumes'.format(self.url)

        name = name or display_name
        description = description or display_description

        volume_request_entity = self.request_models.VolumeRequest(
            size=size, volume_type=volume_type, name=name, image_ref=image_ref,
            description=description, availability_zone=availability_zone,
            metadata=metadata, bootable=bootable, snapshot_id=snapshot_id,
            source_volid=source_volid)

        return self.request(
            'POST', url,
            response_entity_type=self.response_models.VolumeResponse,
            request_entity=volume_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def update_volume(
            self, volume_id, display_name=None, display_description=None,
            name=None, description=None, metadata=None, params=None,
            requestslib_kwargs=None):

        """PUT /volumes"""

        url = '{0}/volumes/{1}'.format(self.url, volume_id)

        name = name or display_name
        description = description or display_description

        volume_request_entity = self.request_models.VolumeRequest(
            name=name, description=description, metadata=metadata)

        return self.request(
            'PUT', url,
            response_entity_type=self.response_models.VolumeResponse,
            request_entity=volume_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def create_snapshot(
            self, volume_id, name=None, description=None,
            display_name=None, display_description=None,
            force_create=False, requestslib_kwargs=None):

        """POST /snapshots"""

        url = '{0}/snapshots'.format(self.url)

        name = name or display_name
        description = description or display_description

        volume_snapshot_request_entity = \
            self.request_models.VolumeSnapshotRequest(
                volume_id,
                force=force_create,
                name=name,
                description=description)

        return self.request(
            'POST', url,
            response_entity_type=self.response_models.VolumeSnapshotResponse,
            request_entity=volume_snapshot_request_entity,
            requestslib_kwargs=requestslib_kwargs)
