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
from datetime import datetime, timedelta
from httplib import BadStatusLine
from requests.exceptions import ConnectionError
from time import sleep

from cloudcafe.common.tools import time
from cloudcafe.cloudkeep.common.responses import CloudkeepResponse


class OrdersBehavior(object):

    def __init__(self, orders_client, secrets_client, config):
        super(OrdersBehavior, self).__init__()
        self.orders_client = orders_client
        self.secrets_client = secrets_client
        self.config = config
        self.created_orders = []

    def _wait_for_order_to_activate(self, create_resp):
        """ Recheck the order every second to see if it's active yet."""
        if not create_resp.entity or not create_resp.entity.reference:
            # We only care about orders that have been created
            return

        stop_time = datetime.now() + timedelta(seconds=30)
        order_ref = create_resp.entity.reference
        order_id = CloudkeepResponse.get_id_from_ref(order_ref)

        while datetime.now() < stop_time:
            order = self.orders_client.get_order(order_id).entity

            if not order:
                raise Exception('Couldn\'t properly retrieve or parse order')

            if order.status == 'ACTIVE':
                # Early return if order has gone active
                return

            # Moderate the calls a little so we don't get rate-limited
            sleep(0.1)

    def create_and_check_order(self, name=None, payload_content_type=None,
                               algorithm=None, bit_length=None, mode=None):
        """Creates order, gets order, and gets secret made by order."""
        resp = self.create_order_overriding_cfg(
            name=name, algorithm=algorithm, bit_length=bit_length,
            mode=mode, payload_content_type=payload_content_type)
        get_order_resp = self.orders_client.get_order(order_id=resp.id)
        behavior_response = CloudkeepResponse(resp=resp.create_resp,
                                              get_resp=get_order_resp)
        return behavior_response

    def create_order_from_config(self, use_expiration=False):
        """Creates order from configuration."""
        expiration = None
        if use_expiration:
            expiration = time.get_tomorrow_timestamp()

        resp = self.create_order(
            name=self.config.name,
            payload_content_type=self.config.payload_content_type,
            algorithm=self.config.algorithm,
            bit_length=self.config.bit_length,
            mode=self.config.mode,
            expiration=expiration,
            order_type='key')
        return resp

    def create_order_overriding_cfg(
            self, name=None, expiration=None, algorithm=None, bit_length=None,
            payload_content_type=None, payload_content_encoding=None,
            mode=None, headers=None, order_type='key'):
        """Creates order using provided parameters or default configurations.
        Allows for testing individual parameters on creation.
        """
        content_type = payload_content_type or self.config.payload_content_type
        resp = self.create_order(
            name=name or self.config.name,
            payload_content_type=content_type,
            payload_content_encoding=payload_content_encoding,
            algorithm=algorithm or self.config.algorithm,
            bit_length=bit_length or self.config.bit_length,
            mode=mode or self.config.mode,
            expiration=expiration,
            order_type=order_type,
            headers=headers)

        return resp

    def create_order(
            self, name=None, algorithm=None, bit_length=None, mode=None,
            payload_content_type=None, payload_content_encoding=None,
            expiration=None, headers=None, order_type='key'):
        try:
            resp = self.orders_client.create_order(
                name=name,
                payload_content_type=payload_content_type,
                payload_content_encoding=payload_content_encoding,
                algorithm=algorithm,
                bit_length=bit_length,
                mode=mode,
                expiration=expiration,
                order_type=order_type,
                headers=headers)
        except ConnectionError as e:
            # Gracefully handling when Falcon doesn't properly handle our req
            if type(e.message.reason) is BadStatusLine:
                return {'status_code': 0}
            raise e

        # Make sure we wait for the order to activate
        self._wait_for_order_to_activate(resp)

        behavior_response = CloudkeepResponse(resp=resp)
        order_id = behavior_response.id
        if order_id is not None:
            self.created_orders.append(behavior_response.id)
        return behavior_response

    def create_order_w_payload(
            self, name=None, algorithm=None, bit_length=None, mode=None,
            payload_content_type=None, payload_content_encoding=None,
            expiration=None, payload=None, order_type='key'):
        """Creates an order with a plain_text value. Separate from
        standard create order method because it is used for negative
        testing only and is expected to fail.
        """
        try:
            resp = self.orders_client.create_order_w_payload(
                name=name or self.config.name,
                algorithm=algorithm or self.config.algorithm,
                bit_length=bit_length or self.config.bit_length,
                mode=mode or self.config.mode,
                expiration=expiration,
                payload_content_type=payload_content_type,
                payload_content_encoding=payload_content_encoding,
                payload=payload,
                order_type=order_type)
        except ConnectionError as e:
            # Gracefully handling when Falcon doesn't properly handle our req
            if type(e.message.reason) is BadStatusLine:
                return {'status_code': 0}
            raise e

        # Make sure we wait for the order to activate
        self._wait_for_order_to_activate(resp)

        behavior_response = CloudkeepResponse(resp=resp)
        order_id = behavior_response.id
        if order_id is not None:
            self.created_orders.append(behavior_response.id)
        return behavior_response

    def delete_order(self, order_id, delete_secret=True):
        if delete_secret:
            resp = self.orders_client.get_order(order_id)
            order = resp.entity
            assert resp.status_code == 200, (
                'Could not get order {id} to delete'.format(id=order_id))

            secret_id = order.get_secret_id()
            self.secrets_client.delete_secret(secret_id)

        resp = self.orders_client.delete_order(order_id)
        if order_id in self.created_orders:
            self.created_orders.remove(order_id)
        return resp

    def delete_all_orders_in_db(self):
        order_group = self.orders_client.get_orders().entity
        found_ids = []
        found_ids.extend(order_group.get_ids())

        while order_group.next is not None:
            query = order_group.get_next_query_data()
            order_group = self.orders_client.get_orders(
                limit=query['limit'],
                offset=query['offset']).entity
            found_ids.extend(order_group.get_ids())

        for order_id in found_ids:
            self.delete_order(order_id)

    def delete_all_created_orders_and_secrets(self):
        for order_id in list(self.created_orders):
            self.delete_order(order_id, delete_secret=True)
        self.created_orders = []

    def remove_from_created_orders(self, order_id):
        if order_id in self.created_orders:
            self.created_orders.remove(order_id)

    def find_order(self, order_id):
        order_group = self.orders_client.get_orders().entity

        ids = order_group.get_ids()
        while order_id not in ids and order_group.next is not None:
            query = order_group.get_next_query_data()
            order_group = self.orders_client.get_orders(
                limit=query['limit'],
                offset=query['offset']).entity
            ids = order_group.get_ids()

        for order in order_group.orders:
            if order.get_id() == order_id:
                return order
        else:
            return None
