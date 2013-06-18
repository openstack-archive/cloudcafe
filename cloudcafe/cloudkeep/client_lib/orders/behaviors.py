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
from cloudcafe.cloudkeep.barbican.orders.behaviors import OrdersBehavior


class ClientLibOrdersBehaviors(OrdersBehavior):
    def __init__(self, barb_client, secrets_client, cl_client, config):
        super(ClientLibOrdersBehaviors, self).__init__(
            barb_client, secrets_client, config)
        self.barb_client = barb_client
        self.config = config
        self.secrets_client = secrets_client
        self.cl_client = cl_client

    def create_and_check_order(self, name=None, expiration=None,
                               algorithm=None, bit_length=None,
                               cypher_type=None, mime_type=None):
        order = self.create_order_overriding_cfg(
            name=name, expiration=expiration,
            algorithm=algorithm, bit_length=bit_length,
            cypher_type=cypher_type, mime_type=mime_type)
        resp = self.barb_client.get_order(order.id)
        return {
            'order': order,
            'get_resp': resp
        }

    def create_order(self, name=None, expiration=None, algorithm=None,
                     bit_length=None, cypher_type=None, mime_type=None):
        order = self.cl_client.create_order(
            name=name,
            expiration=expiration,
            algorithm=algorithm,
            bit_length=bit_length,
            cypher_type=cypher_type,
            mime_type=mime_type)

        self.created_orders.append(order.id)
        return order

    def delete_order(self, order_ref, delete_secret=True):
        if delete_secret:
            order = self.cl_client.get_order(order_ref)
            secret_ref = order.secret_ref
            secret_id = self.get_id_from_ref(secret_ref)
            self.secrets_client.delete_secret(secret_id)

        resp = self.cl_client.delete_order(order_ref)
        order_id = self.get_id_from_ref(order_ref)
        if order_id in self.created_orders:
            self.created_orders.remove(order_id)
        return resp

    def delete_order_by_id(self, order_id, delete_secret=True):
        if delete_secret:
            order = self.cl_client.get_order_by_id(order_id)
            secret_href = order.secret_ref
            secret_id = self.get_id_from_ref(secret_href)
            self.secrets_client.delete_secret(secret_id)

        resp = self.cl_client.delete_order_by_id(order_id)
        if order_id in self.created_orders:
            self.created_orders.remove(order_id)
        return resp

    def delete_all_created_orders_and_secrets(self):
        for order_id in self.created_orders:
            self.delete_order_by_id(order_id, delete_secret=True)

        self.created_orders = []
