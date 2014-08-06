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


class BaseLoadBalancersClient(AutoMarshallingHTTPClient):
    """
    Base Load Balancer Client

    @summary:  Base class for use of load balancer type clients.

    """
    def __init__(self, url, auth_token, serialize_format,
                 deserialize_format=None):
        """Base Load Balancers Client Initializer
        @summary: Initializes BaseLoadBalancersClient
        @param url: Base URL for the Neutron-LBaaS service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for deserializing responses
        @type deserialize_format: String
        """
        super(BaseLoadBalancersClient, self).__init__(serialize_format,
                                                      deserialize_format)
        self.url = '{url}'.format(url=url)
        self.default_headers['X-Auth-Token'] = auth_token

        media_type = 'application/{content_subtype}'
        content_type = media_type.format(content_subtype=self.serialize_format)
        self.default_headers['Content-Type'] = content_type
        accept = media_type.format(content_subtype=self.deserialize_format)
        self.default_headers['Accept'] = accept
