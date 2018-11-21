"""
Copyright 2018 Rackspace

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

from cafe.engine.models.base import AutoMarshallingModel


class VirtualInterface(AutoMarshallingModel):

    def __init__(self, id=None, mac_address=None, ip_addresses=None):

        """
        An object that represents the data of a Virtual Interface.
        """
        super(VirtualInterface, self).__init__()
        self.id = id
        self.mac_address = mac_address
        self.ip_addresses = ip_addresses or []

    def get_ipv4_address(self, network_id):
        ret = None
        for ip_address in self.ip_addresses:
            if (ip_address.network_id == network_id and
                    ip_address.address.find('.') > 0):
                ret = ip_address
                break
        return ret

    def get_ipv6_address(self, network_id):
        ret = None
        for ip_address in self.ip_addresses:
            if (ip_address.network_id == network_id and
                    ip_address.address.find(':') > 0):
                ret = ip_address
                break
        return ret

    @property
    def network_label(self):
        for ip_address in self.ip_addresses:
            if ip_address.network_label is not None:
                return ip_address.network_label

    @property
    def network_id(self):
        for ip_address in self.ip_addresses:
            if ip_address.network_id is not None:
                return ip_address.network_id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        vif = 'virtual_interface'
        vifs = 'virtual_interfaces'
        if vif in json_dict:
            interface_dict = json_dict.get(vif)
            ip_addrs = IPAddress._dict_to_obj(interface_dict)
            interface_dict['ip_addresses'] = ip_addrs
            ret = VirtualInterface(**interface_dict)
        if vifs in json_dict:
            ret = []
            for interface_dict in json_dict.get(vifs):
                ip_addrs = IPAddress._dict_to_obj(interface_dict)
                interface_dict['ip_addresses'] = ip_addrs
                ret.append(VirtualInterface(**interface_dict))
        return ret


class IPAddress(AutoMarshallingModel):

    def __init__(self, network_id=None, network_label=None, address=None):
        super(IPAddress, self).__init__()
        self.network_id = network_id
        self.network_label = network_label
        self.address = address

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        ret = []
        if 'ip_addresses' in json_dict:
            ret = [IPAddress(**addr) for addr in json_dict.get('ip_addresses')]
        return ret
