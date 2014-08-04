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

from cloudcafe.common import BaseClient


class NetsSubnetsPortsClient(BaseClient):
    """Implements the Neutron ReST client for the following API resources:

        networks
        subnets
        ports
    """

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL for the Neutron service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(NetsSubnetsPortsClient, self).__init__(url, auth_token,
                                                     serialize_format,
                                                     deserialize_format)
        self._models_classes = {'networks': (None, None),
                                'subnets': (None, None),
                                'ports': (None, None)}
