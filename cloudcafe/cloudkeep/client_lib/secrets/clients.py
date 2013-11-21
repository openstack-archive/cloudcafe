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
from barbicanclient.common.auth import KeystoneAuthV2
from barbicanclient.client import Client


class ClientLibSecretsClient():
    def __init__(self, url, api_version, auth_endpoint=None,
                 user=None, password=None, tenant_name=None, authenticate=None,
                 request=None, **kwargs):
        self.url = url
        self.api_version = api_version
        self.endpoint = '{base}/{api_version}'.format(
            base=self.url, api_version=self.api_version)
        self.keystone = KeystoneAuthV2(auth_url=auth_endpoint,
                                       username=user,
                                       password=password,
                                       tenant_name=tenant_name)
        # Fix: We need to create an auth plugin for Keystone and CloudCAFE
        self.keystone._barbican_url = self.endpoint
        self.conn = Client(auth_plugin=self.keystone)

        self.tenant_id = self.keystone.tenant_id
        self.tenant_token = self.keystone.auth_token

    def create_secret(self, name=None, expiration=None, algorithm=None,
                      bit_length=None, mode=None, payload=None,
                      payload_content_type=None,
                      payload_content_encoding=None):
        secret = self.conn.secrets.store(
            name=name, expiration=expiration, algorithm=algorithm,
            bit_length=bit_length, mode=mode, payload=payload,
            payload_content_encoding=payload_content_encoding,
            payload_content_type=payload_content_type)

        return secret

    def list_secrets(self, limit=None, offset=None):
        if limit is not None and offset is not None:
            return self.conn.secrets.list(limit=limit, offset=offset)
        else:
            return self.conn.secrets.list()

    def delete_secret(self, href):
        return self.conn.secrets.delete(secret_ref=href)

    def get_secret(self, href):
        return self.conn.secrets.get(secret_ref=href)

    def get_raw_secret(self, href, content_type):
        return self.conn.secrets.decrypt(secret_ref=href,
                                         content_type=content_type)
