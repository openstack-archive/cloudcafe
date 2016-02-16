"""
Copyright 2014 Rackspace

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

import json

from cafe.engine.models.base \
    import AutoMarshallingListModel, AutoMarshallingModel


COMMON_ROOT_TAG = 'floatingip'


class ModelConstraints(object):
    PUBLIC_NET_UUID = '00000000-0000-0000-0000-000000000000'

    PARAM_FILTERS = ['floating_ip_address', 'router_id', 'fixed_ip_address',
                     'status', 'id_', 'floating_network_id', 'port_id',
                     'tenant_id']

    NON_FILTERED_FIELDS = ['floating_ip_address', 'router_id',
                           'floating_network_id', 'status',
                           'fixed_ip_address']

    NON_NULL_FIELDS = ['id_', 'status', 'floating_network_id',
                       'floating_ip_address']


class FloatingIPInfo(AutoMarshallingModel):

    ROOT_TAG = COMMON_ROOT_TAG

    def __init__(self, fixed_ip_address=None, floating_ip_address=None,
                 id_=None, port_id=None, router_id=None, status=None,
                 floating_network_id=None, tenant_id=None):

        """
        Floating IP Info constructor

        :param fixed_ip_address: (string) - IP Address of port
        :param floating_ip_address:  (string) - Floating IP Address
        :param id_: (UUID) UUID of floating IP address
        :param port_id: (UUID) UUID of neutron port
        :param router_id: (UUID) UUID of router
        :param status: (string) Status of the floating IP
        :param floating_network_id: (UUID) UUID of floating network
        :param tenant_id: (UUID) Tenant UUID
        :return: None
        """
        super(FloatingIPInfo, self).__init__()
        self.fixed_ip_address = fixed_ip_address
        self.floating_ip_address = floating_ip_address
        self.floating_network_id = floating_network_id
        self.id_ = id_
        self.port_id = port_id
        self.router_id = router_id
        self.status = status
        self.tenant_id = tenant_id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Deserialize JSON response into Floating IP (FLIP) object

        :param serialized_str: JSON response
        :return: Instantiated & populated FloatingIPInfo object
        """

        json_dict = json.loads(serialized_str)
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        flip_obj = None
        if cls.ROOT_TAG in json_dict:
            flip_obj = cls(**json_dict.get(cls.ROOT_TAG))
        return flip_obj


class FloatingIPInfoList(AutoMarshallingListModel):

    ROOT_TAG = COMMON_ROOT_TAG + 's'
    LIST_MODEL = FloatingIPInfo

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Deserialize JSON response into a list of Floating IP (FLIP) objects

        :param serialized_str: JSON response
        :return: Instantiated & populated FloatingIPListInfo object
        """

        json_dict = json.loads(serialized_str)
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        list_obj = cls()
        floating_ip_info_elems = json_dict.get(cls.ROOT_TAG, [])
        for floating_ip_info in floating_ip_info_elems:
            list_obj.append(cls.LIST_MODEL(**floating_ip_info))
        return list_obj
