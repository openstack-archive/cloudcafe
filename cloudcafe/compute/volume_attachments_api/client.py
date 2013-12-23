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

from cafe.engine.http.client import AutoMarshallingHTTPClient
from cloudcafe.compute.volume_attachments_api.models.requests import \
    VolumeAttachmentRequest
from cloudcafe.compute.volume_attachments_api.models.responses import \
    VolumeAttachmentResponse, VolumeAttachmentListResponse


class VolumeAttachmentsAPIClient(AutoMarshallingHTTPClient):

    def __init__(
            self, url, auth_token, serialize_format=None,
            deserialize_format=None):

        super(VolumeAttachmentsAPIClient, self).__init__(
            serialize_format, deserialize_format)

        url = url.rstrip('/')
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

        self.url = "{0}/servers/{1}/os-volume_attachments".format(
            url, "{server_id}")

    def attach_volume(self, server_id, volume_id, device=None,
                      requestslib_kwargs=None):
        """
        POST
        servers/{server_id}/os-volume_attachments
        """

        url = self.url.format(server_id=server_id)
        req_ent = VolumeAttachmentRequest(volume_id, device)
        return self.request(
            'POST', url, response_entity_type=VolumeAttachmentResponse,
            request_entity=req_ent, requestslib_kwargs=requestslib_kwargs)

    def delete_volume_attachment(self, attachment_id, server_id,
                                 requestslib_kwargs=None):
        """
        DELETE
        servers/{server_id}/os-volume_attachments/{attachment_id}
        """

        url = "{0}/{1}".format(
            self.url.format(server_id=server_id), attachment_id)

        return self.request(
            'DELETE', url, requestslib_kwargs=requestslib_kwargs)

    def get_server_volume_attachments(self, server_id,
                                      requestslib_kwargs=None):
        """
        GET
        servers/{server_id}/os-volume_attachments
        """

        url = self.url.format(server_id=server_id)
        return self.request(
            'GET', url, response_entity_type=VolumeAttachmentListResponse,
            requestslib_kwargs=requestslib_kwargs)

    def get_volume_attachment_details(self, attachment_id, server_id,
                                      requestslib_kwargs=None):
        """
        GET
        servers/{server_id}/os-volume_attachments/{attachment_id}
        """

        url = "{0}/{1}".format(
            self.url.format(server_id=server_id), attachment_id)

        return self.request(
            'GET', url, response_entity_type=VolumeAttachmentResponse,
            requestslib_kwargs=requestslib_kwargs)
