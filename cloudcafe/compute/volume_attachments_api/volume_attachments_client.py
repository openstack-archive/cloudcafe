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
from cloudcafe.compute.volume_attachments_api.models.requests.volume_attachments \
    import VolumeAttachmentRequest

from cloudcafe.compute.volume_attachments_api.models.responses.volume_attachments \
    import VolumeAttachmentListResponse


class VolumeAttachmentsAPIClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, tenant_id, serialize_format=None,
                 deserialize_format=None):

        super(VolumeAttachmentsAPIClient, self).__init__(
            serialize_format, deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.tenant_id = tenant_id
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

    def attach_volume(self, server_id, volume_id, device=None,
                      requestslib_kwargs=None):
        '''POST
        v2/{tenant_id}/servers/{server_id}/os-volume_attachments
        '''

        url = '{0}/servers/{1}/os-volume_attachments'.format(
            self.url, server_id)
        va = VolumeAttachmentRequest(volume_id, device)
        return self.request(
            'POST', url, response_entity_type=VolumeAttachmentListResponse,
            request_entity=va, requestslib_kwargs=requestslib_kwargs)

    def delete_volume_attachment(self, attachment_id, server_id,
                                 requestslib_kwargs=None):
        '''DELETE
        v2/servers/{server_id}/os-volume_attachments/{attachment_id}
        '''

        url = '{0}/servers/{1}/os-volume_attachments/{2}'.format(
            self.url, server_id, attachment_id)

        params = {
            'tenant_id': self.tenant_id, 'server_id': server_id,
            'attachment_id': attachment_id}

        return self.request(
            'DELETE', url, params=params,
            requestslib_kwargs=requestslib_kwargs)

    def get_server_volume_attachments(self, server_id,
                                      requestslib_kwargs=None):
        '''GET
        v2/servers/{server_id}/os-volume_attachments/
        '''

        url = '{0}/servers/{1}/os-volume_attachments'.format(
            self.url, server_id)

        params = {'tenant_id': self.tenant_id, 'server_id': server_id}

        return self.request(
            'GET', url, params=params, requestslib_kwargs=requestslib_kwargs)

    def get_volume_attachment_details(self, attachment_id, server_id,
                                      requestslib_kwargs=None):
        url = '{0}/servers/{1}/os-volume_attachments/{2}'.format(
            self.url, server_id, attachment_id)

        params = {'tenant_id': self.tenant_id,
                  'server_id': server_id,
                  'attachment_id': attachment_id}

        return self.request(
            'GET', url, params=params, requestslib_kwargs=requestslib_kwargs)
