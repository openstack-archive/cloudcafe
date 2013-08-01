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
import re
from os import path
from json import dumps as dict_to_str, loads as str_to_dict
from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.cloudkeep.barbican.secrets.models.secret import Secret


class Order(AutoMarshallingModel):

    def __init__(self, secret, secret_href=None, status=None, order_ref=None):
        super(Order, self).__init__()
        self.secret = secret
        self.secret_href = secret_href
        self.status = status
        self.order_ref = order_ref

    def get_id_from_ref(self, ref):
        """Returns id from reference."""
        ref_id = None
        if ref is not None and len(ref) > 0:
            ref_id = path.split(ref)[1]
        return ref_id

    def get_id(self):
        """Returns order id."""
        return self.get_id_from_ref(ref=self.order_ref)

    def get_secret_id(self):
        """Returns id of secret created by order."""
        return self.get_id_from_ref(ref=self.secret_href)

    def _obj_to_json(self):
        secret_dict = self.secret._obj_to_dict()
        return dict_to_str({'secret': secret_dict})

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        args = {
            'order_ref': json_dict.get('order_ref'),
            'status': json_dict.get('status'),
            'secret_href': json_dict.get('secret_ref'),
            'secret': Secret._dict_to_obj(json_dict.get('secret'))
        }
        return Order(**args)


class OrderRef(AutoMarshallingModel):

    def __init__(self, reference):
        super(OrderRef, self).__init__()
        self.reference = reference

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return OrderRef(reference=json_dict.get('order_ref'))


class OrderGroup(AutoMarshallingModel):

    def __init__(self, orders, next_list=None, previous_list=None):
        super(OrderGroup, self).__init__()

        self.orders = orders
        self.next = next_list
        self.previous = previous_list

    def get_ids(self):
        return [order.get_id() for order in self.orders]

    def get_next_query_data(self):
        matches = re.search('.*\?(.*?)\=(\d*)&(.*?)\=(\d*)', self.next)
        return {
            'limit': matches.group(2),
            'offset': matches.group(4)
        }

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        orders, next_list, prev_list = [], None, None

        for order_dict in json_dict.get('orders'):
            orders.append(Order._dict_to_obj(order_dict))

        if 'next' in json_dict:
            next_list = json_dict.get('next')
        if 'previous' in json_dict:
            prev_list = json_dict.get('previous')
        return OrderGroup(orders, next_list, prev_list)
