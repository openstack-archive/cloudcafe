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
from cloudcafe.cloudkeep.barbican.secrets.models.secret \
    import Secret, SecretGroup, SecretRef, SecretMetadata


class SecretsClient(AutoMarshallingRestClient):
    def __init__(self, url, api_version, tenant_id, serialize_format=None,
                 deserialize_format=None):
        super(SecretsClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.url = url
        self.api_version = api_version
        self.tenant_id = tenant_id

    def _get_base_url(self):
        return '{base}/{api_version}/{tenant_id}'.format(
            base=self.url, api_version=self.api_version,
            tenant_id=self.tenant_id)

    def _get_secret_url(self, secret_id):
        remote_url = '{base}/secrets/{secret_id}'.format(
            base=self._get_base_url(),
            secret_id=secret_id)
        return remote_url

    def create_secret(self, name=None, expiration=None, algorithm=None,
                      bit_length=None, cypher_type=None, plain_text=None,
                      mime_type=None):
        """
        POST http://.../v1/{tenant_id}/secrets
        Allows a user to create a new secret
        """
        remote_url = '{base}/secrets'.format(base=self._get_base_url())
        req_obj = Secret(name=name, mime_type=mime_type,
                         expiration=expiration, algorithm=algorithm,
                         bit_length=bit_length, cypher_type=cypher_type,
                         plain_text=plain_text)

        resp = self.request('POST', remote_url, request_entity=req_obj,
                            response_entity_type=SecretRef)

        return resp

    def add_secret_plain_text(self, secret_id, mime_type, plain_text):
        """
        PUT http://.../v1/{tenant_id}/secrets/{secret_uuid}
        Allows the user to upload secret data for a specified secret if
        the secret doesn't already exist
        """
        remote_url = self._get_secret_url(secret_id)
        headers = {'Content-Type': mime_type}
        resp = self.request('PUT', remote_url, headers=headers,
                            data=plain_text)

        return resp

    def get_secret(self, secret_id=None, mime_type=None, ref=None):
        """
        GET http://.../v1/{tenant_id}/secrets/{secret_uuid}
        @param mime_type: if not set, it'll only retrieve the metadata
        for the secret.
        """
        resp_type = None
        if mime_type is None:
            resp_type = SecretMetadata
            mime_type = 'application/json'

        remote_url = ref or self._get_secret_url(secret_id)
        headers = {'Accept': mime_type}
        resp = self.request('GET', remote_url, headers=headers,
                            response_entity_type=resp_type)
        return resp

    def get_secrets(self, limit=None, offset=None, ref=None):
        """
        GET http://.../v1/secrets?limit={limit}&offset={offset} or {ref}
        Gets a list of secrets
        """
        remote_url = ref or '{base}/secrets'.format(base=self._get_base_url())
        resp = self.request('GET', remote_url,
                            params={'limit': limit, 'offset': offset},
                            response_entity_type=SecretGroup)
        return resp

    def delete_secret(self, secret_id):
        """
        DELETE http://.../v1/{tenant_id}/secrets/{secret_uuid}
        """
        remote_url = self._get_secret_url(secret_id)
        return self.request('DELETE', remote_url)
