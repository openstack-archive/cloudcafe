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
from barbicanclient.client import Connection


class ClientLibOrdersClient():
    def __init__(self, url, api_version, tenant_id, auth_endpoint=None,
                 user=None, key=None, token=None, authenticate=None,
                 request=None, **kwargs):
        self.url = url
        self.api_version = api_version
        self.tenant_id = tenant_id
        self.endpoint = '{base}/{api_version}'.format(
            base=self.url, api_version=self.api_version)
        self.conn = Connection(
            endpoint=self.endpoint, auth_endpoint=auth_endpoint,
            user=user, key=key, tenant=tenant_id, token=token,
            authenticate=authenticate, request=request, **kwargs)

    def create_order(self, name=None, expiration=None, algorithm=None,
                     bit_length=None, cypher_type=None, mime_type=None):
        order = self.conn.create_order(
            name=name, algorithm=algorithm, bit_length=bit_length,
            cypher_type=cypher_type, mime_type=mime_type)

        return order

    def list_orders(self, limit=None, offset=None):
        if limit is not None and offset is not None:
            return self.conn.list_orders(limit=limit, offset=offset)
        else:
            return self.conn.list_orders()

    def list_orders_by_href(self, href=None):
        if href is None:
            href = '{endpoint}/{tenant_id}/orders'.format(
                endpoint=self.endpoint,
                tenant_id=self.tenant_id)

        return self.conn.list_orders_by_href(href=href)

    def delete_order_by_id(self, order_id):
        return self.conn.delete_order_by_id(order_id=order_id)

    def delete_order(self, href):
        return self.conn.delete_order(href=href)

    def get_order_by_id(self, order_id):
        return self.conn.get_order_by_id(order_id=order_id)

    def get_order(self, href):
        return self.conn.get_order(href=href)
