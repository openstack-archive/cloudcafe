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
from cloudcafe.cloudkeep.barbican.secrets.models.secret import Secret
from cloudcafe.cloudkeep.barbican.orders.models.order \
    import Order, OrderRef, OrderGroup


class OrdersClient(AutoMarshallingRestClient):

    def __init__(self, url, api_version, tenant_id, serialize_format,
                 deserialize_format):
        super(OrdersClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.url = url
        self.api_version = api_version
        self.tenant_id = tenant_id

    def _get_base_url(self):
        return '{base}/{api_version}/{tenant_id}/orders'.format(
            base=self.url,
            api_version=self.api_version,
            tenant_id=self.tenant_id)

    def _get_order_url(self, order_id):
        return '{base}/{order_id}'.format(base=self._get_base_url(),
                                          order_id=order_id)

    def create_order(self, name, mime_type, algorithm, bit_length,
                     cypher_type, expiration):
        """
        POST http://.../v1/{tenant_id}/orders/{order_uuid}
        Creates an order to generate a secret
        """
        remote_url = self._get_base_url()
        secret = Secret(name=name,
                        mime_type=mime_type,
                        expiration=expiration,
                        algorithm=algorithm,
                        bit_length=bit_length,
                        cypher_type=cypher_type)
        req_obj = Order(secret=secret)

        resp = self.request('POST', remote_url, request_entity=req_obj,
                            response_entity_type=OrderRef)
        return resp

    def create_order_w_plain_text(self, name, mime_type, algorithm, bit_length,
                                  cypher_type, expiration, plain_text):
        """
        POST http://.../v1/{tenant_id}/orders/{order_uuid}
        Creates an order to generate a secret with plain text. This is
        separate from the create_order method because it is used for
        negative testing only and is expected to fail.
        """
        remote_url = self._get_base_url()
        secret = Secret(name=name,
                        mime_type=mime_type,
                        expiration=expiration,
                        algorithm=algorithm,
                        bit_length=bit_length,
                        cypher_type=cypher_type,
                        plain_text=plain_text)
        req_obj = Order(secret=secret)

        resp = self.request('POST', remote_url, request_entity=req_obj,
                            response_entity_type=OrderRef)
        return resp

    def get_order(self, order_id=None, ref=None):
        """
        GET http://.../v1/{tenant_id}/orders/{order_uuid}
        Retrieves an order
        """
        remote_url = ref or self._get_order_url(order_id)
        return self.request('GET', remote_url, response_entity_type=Order)

    def delete_order(self, order_id):
        """
        DELETE http://.../v1/{tenant_id}/orders/{order_uuid}
        Cancels an order
        """
        return self.request('DELETE', self._get_order_url(order_id))

    def get_orders(self, limit=None, offset=None, ref=None):
        """
        GET http://.../v1/orders?limit={limit}&offset={offset} or {ref}
        Gets a list of orders
        """
        remote_url = ref or self._get_base_url()
        resp = self.request('GET', remote_url,
                            params={'limit': limit, 'offset': offset},
                            response_entity_type=OrderGroup)
        return resp

    def update_order(self, order_id, mime_type, data):
        """
        PUT http://.../v1/{tenant_id}/orders/{order_uuid}
        Attempts to update order similar to how secrets are updated.
        """
        remote_url = self._get_order_url(order_id)
        headers = {'Content-Type': mime_type}
        resp = self.request('PUT', remote_url, headers=headers,
                            data=data)
        return resp
