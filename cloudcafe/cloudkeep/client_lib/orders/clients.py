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


class ClientLibOrdersClient():
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

    def create_order(self, name=None, expiration=None, algorithm=None,
                     bit_length=None, mode=None, payload_content_type=None):
        order = self.conn.orders.create(
            name=name, algorithm=algorithm, bit_length=bit_length,
            mode=mode, payload_content_type=payload_content_type,
            expiration=expiration)

        return order

    def list_orders(self, limit=None, offset=None):
        return self.conn.orders.list(limit=limit, offset=offset)

    def delete_order(self, href):
        return self.conn.orders.delete(order_ref=href)

    def get_order(self, href):
        return self.conn.orders.get(order_ref=href)
