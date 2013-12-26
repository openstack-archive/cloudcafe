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
from cloudcafe.common.tools import time
from cloudcafe.cloudkeep.common.responses import CloudkeepResponse


class SecretsBehaviors(object):

    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.created_secrets = []

    def create_and_check_secret(self, name=None, expiration=None,
                                algorithm=None, bit_length=None,
                                mode=None, payload=None,
                                payload_content_type=None):
        resp = self.create_secret_overriding_cfg(
            name=name, expiration=expiration, algorithm=algorithm,
            bit_length=bit_length, mode=mode,
            payload=payload, payload_content_type=payload_content_type)
        get_resp = self.client.get_secret(resp.id)
        behavior_resp = CloudkeepResponse(resp=resp.create_resp,
                                          get_resp=get_resp)
        return behavior_resp

    def create_secret_from_config(self, use_expiration=True,
                                  use_payload=True):
        expiration = None
        data = None
        if use_expiration:
            expiration = time.get_tomorrow_timestamp()
        if use_payload:
            data = self.config.payload

        resp = self.create_secret(
            name=self.config.name,
            expiration=expiration,
            algorithm=self.config.algorithm,
            bit_length=self.config.bit_length,
            mode=self.config.mode,
            payload=data,
            payload_content_type=self.config.payload_content_type,
            payload_content_encoding=self.config.payload_content_encoding)
        return resp

    def create_secret_overriding_cfg(self, name=None, expiration=None,
                                     algorithm=None, bit_length=None,
                                     mode=None, payload=None,
                                     payload_content_type=None,
                                     payload_content_encoding=None):
        """
        Allows for testing individual parameters on creation.
        """
        resp = self.create_secret(
            name=name or self.config.name,
            algorithm=algorithm or self.config.algorithm,
            bit_length=bit_length or self.config.bit_length,
            mode=mode or self.config.mode,
            payload=payload or self.config.payload,
            payload_content_type=
            payload_content_type or self.config.payload_content_type,
            payload_content_encoding=
            payload_content_encoding or self.config.payload_content_encoding,
            expiration=expiration)
        return resp

    def create_secret(self, name=None, expiration=None, algorithm=None,
                      bit_length=None, mode=None, payload=None,
                      payload_content_type=None,
                      payload_content_encoding=None):
        resp = self.client.create_secret(
            name=name,
            expiration=expiration,
            algorithm=algorithm,
            bit_length=bit_length,
            mode=mode,
            payload=payload,
            payload_content_type=payload_content_type,
            payload_content_encoding=payload_content_encoding)

        behavior_response = CloudkeepResponse(resp=resp)
        secret_id = behavior_response.id
        if secret_id is not None:
            self.created_secrets.append(secret_id)
        return behavior_response

    def create_secret_with_no_json(self):
        """Create a secret but do not pass any JSON in POST data."""
        resp = self.client.create_secret_with_no_json()
        behavior_response = CloudkeepResponse(resp=resp)
        secret_id = behavior_response.id
        if secret_id is not None:
            self.created_secrets.append(secret_id)
        return behavior_response

    def delete_secret(self, secret_id):
        self.remove_from_created_secrets(secret_id=secret_id)
        resp = self.client.delete_secret(secret_id)
        return resp

    def delete_all_created_secrets(self):
        for secret_id in list(self.created_secrets):
            self.delete_secret(secret_id)
        self.created_secrets = []

    def remove_from_created_secrets(self, secret_id):
        if secret_id in self.created_secrets:
            self.created_secrets.remove(secret_id)

    def delete_all_secrets_in_db(self):
        secret_group = self.client.get_secrets().entity
        found_ids = []
        found_ids.extend(secret_group.get_ids())

        while secret_group.next is not None:
            query = secret_group.get_next_query_data()
            secret_group = self.client.get_secrets(
                limit=query['limit'],
                offset=query['offset']).entity
            found_ids.extend(secret_group.get_ids())

        for secret_id in found_ids:
            self.delete_secret(secret_id)

    def find_secret(self, secret_id):
        secret_group = self.client.get_secrets().entity

        ids = secret_group.get_ids()
        while secret_id not in ids and secret_group.next is not None:
            query = secret_group.get_next_query_data()
            secret_group = self.client.get_secrets(
                limit=query['limit'],
                offset=query['offset']).entity
            ids = secret_group.get_ids()

        for secret in secret_group.secrets:
            if secret.get_id() == secret_id:
                return secret
        else:
            return None
