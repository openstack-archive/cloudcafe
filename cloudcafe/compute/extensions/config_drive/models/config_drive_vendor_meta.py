"""
Copyright 2015 Rackspace

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
    import AutoMarshallingModel, AutoMarshallingListModel


class VendorMetadata(AutoMarshallingModel):

    def __init__(self, network_info=None, region=None,
                 ip_whitelist=None, roles=None, provider=None):
        self.network_info = network_info
        self.region = region
        self.ip_whitelist = ip_whitelist
        self.roles = roles
        self.provider = provider

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        vendor_meta = cls._dict_to_obj(json_dict)
        return vendor_meta

    @classmethod
    def _dict_to_obj(cls, json_dict):
        vendor_meta = VendorMetadata(
            region=json_dict.get('region'),
            provider=json_dict.get('provider'),
            ip_whitelist=json_dict.get('ip_whitelist'),
            roles=json_dict.get('roles'))
        if 'network_info' in json_dict:
            vendor_meta.network_info = NetworkInfo._dict_to_obj(
                json_dict['network_info'])
        return vendor_meta


class NetworkInfo(AutoMarshallingModel):

    def __init__(self, services=None, networks=None,
                 links=None):
        self.services = services
        self.networks = networks
        self.links = links

    @classmethod
    def _dict_to_obj(cls, json_dict):
        network_info = NetworkInfo()
        if 'services' in json_dict:
            network_info.services = Services._list_to_obj(
                json_dict['services'])
        if 'networks' in json_dict:
            network_info.networks = Networks._list_to_obj(
                json_dict['networks'])
        if 'links' in json_dict:
            network_info.links = Links._list_to_obj(
                json_dict['links'])
        return network_info


class Service(AutoMarshallingModel):

    def __init__(self, type=None, address=None):
        self.type = type
        self.address = address

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Service(
            type=json_dict.get('type'),
            address=json_dict.get('address'))


class Services(AutoMarshallingListModel):

    @classmethod
    def _list_to_obj(cls, service_dict_list):
        service_list = Services()
        for service_dict in service_dict_list:
            service = Service._dict_to_obj(service_dict)
            service_list.append(service)
        return service_list


class Link(AutoMarshallingModel):

    def __init__(self, ethernet_mac_address=None, mtu=None,
                 type=None, id=None, vif_id=None):
        self.ethernet_mac_address = ethernet_mac_address
        self.mtu = mtu
        self.type = type
        self.id = id
        self.vif_id = vif_id

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Link(
            ethernet_mac_address=json_dict.get('ethernet_mac_address'),
            mtu=json_dict.get('mtu'),
            type=json_dict.get('type'),
            id=json_dict.get('id'),
            vif_id=json_dict.get('vif_id'))


class Links(AutoMarshallingListModel):

    @classmethod
    def _list_to_obj(cls, link_dict_list):
        link_list = Links()
        for link_dict in link_dict_list:
            link = Link._dict_to_obj(link_dict)
            link_list.append(link)
        return link_list


class Network(AutoMarshallingModel):

    def __init__(self, network_id=None, type=None, netmask=None,
                 link=None, routes=None, ip_address=None, id=None):
        self.network_id = network_id
        self.type = type
        self.netmask = netmask
        self.link = link
        self.routes = routes
        self.ip_address = ip_address
        self.id = id

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Network(
            network_id=json_dict.get('network_id'),
            type=json_dict.get('type'),
            netmask=json_dict.get('netmask'),
            link=json_dict.get('link'),
            routes=json_dict.get('routes'),
            ip_address=json_dict.get('ip_address'),
            id=json_dict.get('id'))


class Networks(AutoMarshallingListModel):

    @classmethod
    def _list_to_obj(cls, network_dict_list):
        network_list = Networks()
        for network_dict in network_dict_list:
            network = Network._dict_to_obj(network_dict)
            network_list.append(network)
        return network_list
