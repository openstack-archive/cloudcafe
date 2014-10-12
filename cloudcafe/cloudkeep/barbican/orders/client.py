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
from cloudcafe.cloudkeep.barbican.client import BarbicanRestClient
from cloudcafe.cloudkeep.barbican.secrets.models.secret import Secret
from cloudcafe.cloudkeep.barbican.orders.models.order \
    import Order, OrderRef, OrderGroup


class OrdersClient(BarbicanRestClient):

    def __init__(self, url, api_version, token=None,
                 serialize_format=None, deserialize_format=None):
        super(OrdersClient, self).__init__(
            token=token, serialize_format=serialize_format,
            deserialize_format=deserialize_format)
        self.url = url
        self.api_version = api_version

    def _get_base_url(self):
        return '{base}/{api_version}/orders'.format(
            base=self.url,
            api_version=self.api_version)

    def _get_order_url(self, order_id):
        return '{base}/{order_id}'.format(base=self._get_base_url(),
                                          order_id=order_id)

    def create_order(self, name, algorithm, bit_length, mode, expiration,
                     order_type, payload_content_type,
                     payload_content_encoding, headers=None):
        """
        POST http://.../v1/orders/{order_uuid}
        Creates an order to generate a secret
        """
        remote_url = self._get_base_url()
        secret = Secret(name=name,
                        payload_content_type=payload_content_type,
                        payload_content_encoding=payload_content_encoding,
                        expiration=expiration,
                        algorithm=algorithm,
                        bit_length=bit_length,
                        mode=mode)
        req_obj = Order(meta=secret, order_type=order_type)

        resp = self.request('POST', remote_url, request_entity=req_obj,
                            response_entity_type=OrderRef, headers=headers)
        return resp

    def create_order_w_payload(self, name, algorithm, bit_length, mode,
                               expiration, payload, payload_content_type,
                               payload_content_encoding, order_type):
        """
        POST http://.../v1/orders/{order_uuid}
        Creates an order to generate a secret with plain text. This is
        separate from the create_order method because it is used for
        negative testing only and is expected to fail.
        """
        remote_url = self._get_base_url()
        secret = Secret(name=name,
                        payload_content_type=payload_content_type,
                        payload_content_encoding=payload_content_encoding,
                        expiration=expiration,
                        algorithm=algorithm,
                        bit_length=bit_length,
                        mode=mode,
                        payload=payload)
        req_obj = Order(meta=secret, order_type=order_type)

        resp = self.request('POST', remote_url, request_entity=req_obj,
                            response_entity_type=OrderRef)
        return resp

    def get_order(self, order_id=None, ref=None):
        """
        GET http://.../v1/orders/{order_uuid}
        Retrieves an order
        """
        remote_url = ref or self._get_order_url(order_id)
        return self.request('GET', remote_url, response_entity_type=Order)

    def delete_order(self, order_id):
        """
        DELETE http://.../v1/orders/{order_uuid}
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

    def update_order(self, order_id, payload_content_type=None, data=None):
        """
        PUT http://.../v1/orders/{order_uuid}
        Attempts to update order similar to how secrets are updated.
        """
        remote_url = self._get_order_url(order_id)
        headers = {'Content-Type': payload_content_type}
        resp = self.request('PUT', remote_url, headers=headers,
                            data=data)
        return resp
