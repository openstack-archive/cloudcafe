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

from cafe.engine.http.client import AutoMarshallingHTTPClient
from cloudcafe.compute.extensions.ip_associations_api.models.response \
    import IPAssociation, IPAssociations


class IPAssociationsClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @summary: Rackspace Compute API IP Associations extension client
        @param url: Base URL for the compute service
        @type url: string
        @param auth_token: Auth token to be used for all requests
        @type auth_token: string
        @param serialize_format: Format for serializing requests
        @type serialize_format: string
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: string
        """
        super(IPAssociationsClient, self).__init__(serialize_format,
                                                   deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.serialize_format)
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_ip_associations(self, server_id, ip_address_id=None,
                             address=None, limit=None, marker=None,
                             page_reverse=None, requestslib_kwargs=None):
        """
        @summary: Lists IP associations by server, filtered by params if given
        @param server_id: server UUID to get shared IP associations
        @type server_id: str
        @param ip_address_id: shared IP UUID to filter by
        @type ip_address_id: str
        @param address: IPv4 or IPv6 shared IP address to filter by
        @type address: str
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @return: IP associations list response
        @rtype: Requests.response
        """

        params = {'id': ip_address_id, 'address': address,
                  'limit': limit, 'marker': marker,
                  'page_reverse': page_reverse}

        url = '{base_url}/servers/{server_id}/ip_associations'.format(
            base_url=self.url, server_id=server_id)

        resp = self.request('GET', url, params=params,
                            response_entity_type=IPAssociations,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_ip_association(self, server_id, ip_address_id,
                           requestslib_kwargs=None):
        """
        @summary: Shows a specific IP association
        @param server_id: server UUID to get shared IP association
        @type server_id: str
        @param ip_address_id: shared IP UUID
        @type ip_address_id: str
        @return: IP association get response
        @rtype: Requests.response
        """

        url = ('{base_url}/servers/{server_id}/ip_associations/'
               '{ip_address_id}').format(base_url=self.url,
                                         server_id=server_id,
                                         ip_address_id=ip_address_id)

        resp = self.request('GET', url,
                            response_entity_type=IPAssociation,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_ip_association(self, server_id, ip_address_id,
                              requestslib_kwargs=None):
        """
        @summary: Creates a shared IP association with a server instance
        @param server_id: server UUID to create shared IP association
        @type server_id: str
        @param ip_address_id: shared IP UUID to associate with server
        @type ip_address_id: str
        @return: IP association get response
        @rtype: Requests.response
        """

        url = ('{base_url}/servers/{server_id}/ip_associations/'
               '{ip_address_id}').format(base_url=self.url,
                                         server_id=server_id,
                                         ip_address_id=ip_address_id)

        # Currently this call does NOT requires a request body
        resp = self.request('PUT', url,
                            response_entity_type=IPAssociation,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_ip_association(self, server_id, ip_address_id,
                              requestslib_kwargs=None):
        """
        @summary: Deletes a shared IP association with a server instance
        @param server_id: server UUID to remove shared IP association
        @type server_id: str
        @param ip_address_id: shared IP UUID to disassociate from server
        @type ip_address_id: str
        @return: IP association delete response
        @rtype: Requests.response
        """

        url = ('{base_url}/servers/{server_id}/ip_associations/'
               '{ip_address_id}').format(base_url=self.url,
                                         server_id=server_id,
                                         ip_address_id=ip_address_id)

        # Currently this call does NOT requires a request body
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
