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
from cafe.engine.clients.rest import BaseRestClient
from cloudcafe.extensions.saio_tempauth.v1_0.models.requests import AuthData


class TempauthAPI_Client(BaseRestClient):
    """
    Tempauth Client for use with Swift All In One.
    """

    def __init__(self, endpoint):
        super(TempauthAPI_Client, self).__init__()
        self.endpoint = endpoint

    def authenticate(self, username, password):
        headers = {
            'X-Storage-User': username,
            'X-Storage-Pass': password
        }

        url = '{0}/auth/v1.0'.format(self.endpoint)

        r = self.request('GET', url, headers=headers)
        if not r.ok:
            raise Exception('Could not auth')

        storage_url = r.headers['x-storage-url']
        auth_token = r.headers['x-auth-token']
        storage_token = r.headers['x-storage-token']

        data = AuthData(storage_url, auth_token, storage_token)

        return data
