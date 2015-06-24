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

from cafe.engine.models.base import AutoMarshallingListModel, \
    AutoMarshallingModel


class IPAddress(AutoMarshallingModel):
    """
    @summary: IP Address model response object for the Shared IPs Rackspace
        Networking v2.0 API extension.
    @param id_: shared IP UUID
    @type id_: str
    @param network_id: network UUID where the IP address belongs to
    @type network_id: str
    @param address: IP address
    @type address: str
    @param port_ids: list of port UUIDs where the shared IP will be associated
    @type port_ids: list(str)
    @param subnet_id: subnet UUID where the IP address belongs to
    @type subnet_id: str
    @param tenant_id: tenant ID of the shared IP user
    @type tenant_id: str
    @param version: IP address version 4 or 6
    @type version: str
    @param type_: IP address type, for ex. fixed
    @type type_: str
    """

    IP_ADDRESS = 'ip_address'

    def __init__(self, id_=None, network_id=None, address=None, port_ids=None,
                 subnet_id=None, tenant_id=None, version=None, type_=None,
                 **kwargs):

        # kwargs is to be used for checking unexpected attrs
        super(IPAddress, self).__init__()
        self.id = id_
        self.network_id = network_id
        self.address = address
        self.port_ids = port_ids
        self.subnet_id = subnet_id
        self.tenant_id = tenant_id
        self.version = version
        self.type = type_
        self.kwargs = kwargs

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Return IP address object from a JSON serialized string
        """

        ret = None
        json_dict = json.loads(serialized_str)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)
        json_dict = cls._replace_dict_key(
            json_dict, 'type', 'type_', recursion=True)

        if cls.IP_ADDRESS in json_dict:
            ip_address_dict = json_dict.get(cls.IP_ADDRESS)
            ret = IPAddress(**ip_address_dict)
        return ret


class IPAddresses(AutoMarshallingListModel):

    IP_ADDRESSES = 'ip_addresses'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Return a list of IP address objects from a JSON
            serialized string
        """
        ret = cls()
        json_dict = json.loads(serialized_str)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)
        json_dict = cls._replace_dict_key(
            json_dict, 'type', 'type_', recursion=True)

        if cls.IP_ADDRESSES in json_dict:
            ip_addresses = json_dict.get(cls.IP_ADDRESSES)
            for ip_address in ip_addresses:
                result = IPAddress(**ip_address)
                ret.append(result)
        return ret
