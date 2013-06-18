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
from cloudcafe.cloudkeep.barbican.secrets.behaviors import SecretsBehaviors


class ClientLibSecretsBehaviors(SecretsBehaviors):

    def __init__(self, cl_client, barb_client, config):
        super(ClientLibSecretsBehaviors, self).__init__(client=barb_client,
                                                        config=config)
        self.barb_client = barb_client
        self.cl_client = cl_client
        self.config = config

    def create_and_check_secret(self, name=None, expiration=None,
                                algorithm=None, bit_length=None,
                                cypher_type=None, plain_text=None,
                                mime_type=None):
        secret = self.create_secret_overriding_cfg(
            name=name, expiration=expiration, algorithm=algorithm,
            bit_length=bit_length, cypher_type=cypher_type,
            plain_text=plain_text, mime_type=mime_type)
        resp = self.barb_client.get_secret(secret.id)
        return {
            'secret': secret,
            'get_resp': resp
        }

    def create_secret(self, name=None, expiration=None, algorithm=None,
                      bit_length=None, cypher_type=None, plain_text=None,
                      mime_type=None):
        secret = self.cl_client.create_secret(
            name=name,
            expiration=expiration,
            algorithm=algorithm,
            bit_length=bit_length,
            cypher_type=cypher_type,
            plain_text=plain_text,
            mime_type=mime_type)

        self.created_secrets.append(secret.id)
        return secret

    def delete_secret(self, secret_ref):
        secret_id = self.get_secret_id_from_ref(secret_ref=secret_ref)
        self.remove_from_created_secrets(secret_id=secret_id)
        resp = self.cl_client.delete_secret(href=secret_ref)
        return resp

    def delete_secret_by_id(self, secret_id):
        self.remove_from_created_secrets(secret_id=secret_id)
        resp = self.cl_client.delete_secret_by_id(secret_id=secret_id)
        return resp

    def delete_all_created_secrets(self):
        for secret_id in self.created_secrets:
            self.delete_secret_by_id(secret_id=secret_id)
        self.created_secrets = []
