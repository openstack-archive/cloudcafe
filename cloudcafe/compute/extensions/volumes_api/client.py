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
from cloudcafe.blockstorage.v1.volumes_api.models.responses.volumes_api import _VolumesAPIBaseModel
from cloudcafe.compute.extensions.volumes_api.models.requests import CreateVolume


class VolumeClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(VolumeClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_volume(self, display_name, display_description,
                      size, volume_type, metadata, availability_zone,
                        requestslib_kwargs=None):
        """
        @summary: Creates a volume
        @param display_name: The display name of the volume
        @type display_name: str
        @param display_description: Description about volume
        @type display_description: String
        @param size: Size of the volume
        @type size: int
        @param volume_type: Type of Volume, ex: SATA
        @type volume_type: str
        @param metadata: Metadata for volume
        @type metadata: dict
        @param availability_zone: Zone in which the volume is available
        @type availability_zone: str
        @return: A Volume repsonse
        @rtype: Requests.response
        """
        request = CreateVolume(display_name, display_description,
                               size, volume_type, metadata,
                               availability_zone)

        url = '{base_url}/os-volumes'.format( base_url=self.url)
        resp = self.request('POST', url,
                            response_entity_type=_VolumesAPIBaseModel,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

