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


class BaseIdentityAPIClient(AutoMarshallingHTTPClient):
    def __init__(self, url=None, serialize_format=None,
                 deserialize_format=None, auth_token=None):
        super(BaseIdentityAPIClient, self).__init__(serialize_format,
                                                    deserialize_format)
        self.url = url
        self.token = auth_token
        self.default_headers.update({
            'Content-Type': 'application/{0}'.format(serialize_format),
            'Accept': 'application/{0}'.format(deserialize_format)})

    @property
    def token(self):
        return self.default_headers.get('X-Auth-Token')

    @token.setter
    def token(self, token):
        self.default_headers['X-Auth-Token'] = token

    @token.deleter
    def token(self):
        del self.default_headers['X-Auth-Token']
