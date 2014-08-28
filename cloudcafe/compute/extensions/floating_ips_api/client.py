"""
Copyright 2014 Rackspace

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

from cloudcafe.compute.extensions.floating_ips_api.models.requests import \
    CreateFloatingIP
from cloudcafe.compute.extensions.floating_ips_api.models.responses import \
    FloatingIP, FloatingIPs


class FloatingIPsClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(FloatingIPsClient, self).__init__(
            serialize_format, deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_floating_ip(self, pool=None, requestslib_kwargs=None):
        """
        @summary: Creates a floating IP address from an existing pool
        @param pool: Name of the pool to allocate an IP address from
        @type pool: String
        @rtype: Requests.response
        """

        request = CreateFloatingIP(pool=pool)

        url = '{base_url}/os-floating-ips'.format(base_url=self.url)
        return self.request('POST', url, response_entity_type=FloatingIP,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_floating_ip(self, floating_ip_id, requestslib_kwargs=None):
        """
        @summary: Deletes the specified floating IP address.
        @param floating_ip_id: The id of an existing floating IP address
        @type floating_ip_id: String
        @rtype: Requests.response
        """

        url = '{base_url}/os-floating-ips/{floating_ip_id}'.format(
            base_url=self.url, floating_ip_id=floating_ip_id)
        return self.request('DELETE', url, requestslib_kwargs=requestslib_kwargs)

    def list_floating_ips(self, requestslib_kwargs=None):
        """
        @summary: Lists all floating IPs for the tenant.
        @rtype: Requests.response
        """

        url = '{base_url}/os-floating-ips'.format(base_url=self.url)
        return self.request('GET', url, response_entity_type=FloatingIPs,
                            requestslib_kwargs=requestslib_kwargs)

    def get_floating_ip(self, floating_ip_id, requestslib_kwargs=None):
        """
        @summary: Retrieves the details of a floating IP address.
        @param floating_ip_id: The id of an existing floating IP address
        @type floating_ip_id: String
        @rtype: Requests.response
        """

        url = '{base_url}/os-floating-ips/{floating_ip_id}'.format(
            base_url=self.url, floating_ip_id=floating_ip_id)
        return self.request('GET', url, requestslib_kwargs,
                            response_entity_type=FloatingIP,
                            requestslib_kwargs=requestslib_kwargs)
