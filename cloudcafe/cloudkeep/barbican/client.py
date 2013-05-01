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
from cloudcafe.cloudkeep.barbican.models.version import Version


class VersionClient(AutoMarshallingRestClient):
    def __init__(self, url, serialize_format=None, deserialize_format=None):
        """
        @param url: Base URL of meniscus api
        @type url: String
        """
        super(VersionClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.url = url

    def get_version(self):
        """
        @summary: Retrieves the version information from the API
        """
        resp = self.request('GET', self.url, response_entity_type=Version)
        return resp
