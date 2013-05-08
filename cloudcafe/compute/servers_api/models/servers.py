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

import IPy
import json
import re
import xml.etree.ElementTree as ET

from cafe.engine.models.base import BaseModel
from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.models.link import Links
from cloudcafe.compute.flavors_api.models.flavor import Flavor, FlavorMin
from cloudcafe.compute.images_api.models.image import Image, ImageMin
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.models.metadata import Metadata


class Server(AutoMarshallingModel):

    def __init__(self, id, diskConfig, power_state, progress, task_state,
                 vm_state, name, tenantId, status, updated, created, hostId,
                 user_id, accessIPv4, accessIPv6, addresses, flavor, image,
                 links, metadata, admin_pass):
        self.diskConfig = diskConfig
        try:
            self.power_state = int(power_state)
        except TypeError:
            self.power_state = 0
        self.progress = progress
        self.task_state = task_state
        self.vm_state = vm_state
        self.name = name
        self.id = id
        self.tenant_id = tenantId
        self.status = status
        self.updated = updated
        self.created = created
        self.host_id = hostId
        self.user_id = user_id
        if accessIPv4:
            self.accessIPv4 = str(IPy.IP(accessIPv4))
        else:
            self.accessIPv4 = None

        if accessIPv6:
            self.accessIPv6 = str(IPy.IP(accessIPv6))
        else:
            self.accessIPv6 = None

        self.addresses = addresses
        self.flavor = flavor
        self.image = image
        self.links = links
        self.metadata = metadata
        self.admin_pass = admin_pass

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''
        Returns an instance of a Server based on the json serialized_str
        passed in
        '''
        ret = None
        json_dict = json.loads(serialized_str)
        if 'server' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict['server'])
        if 'servers' in json_dict.keys():
            ret = []
            for server in json_dict['servers']:
                s = cls._dict_to_obj(server)
                ret.append(s)
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''
        Returns an instance of a Server based on the xml serialized_str
        passed in
        '''
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_EXTENDED_STATUS_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_DISK_CONFIG_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_ATOM_NAMESPACE)
        if element.tag == 'server':
            ret = cls._xml_ele_to_obj(element)
        if element.tag == 'servers':
            ret = []
            for server in element.findall('server'):
                s = cls._xml_ele_to_obj(server)
                ret.append(s)
        return ret

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Server instance.'''
        server_dict = element.attrib

        addresses = None
        flavor = None
        image = None
        links = None
        metadata = None

        links = Links._xml_ele_to_obj(element)
        if element.find('addresses') is not None:
            addresses = Addresses._xml_ele_to_obj(element.find('addresses'))
        if element.find('flavor') is not None:
            flavor = Flavor._xml_ele_to_obj(element.find('flavor'))
        if element.find('image') is not None:
            image = Image._xml_ele_to_obj(element.find('image'))
        if element.find('metadata') is not None:
            metadata = Metadata._xml_ele_to_obj(element)

        if 'progress' in server_dict:
            progress = server_dict.get('progress') \
                and int(server_dict.get('progress'))
        if 'tenantId' in server_dict:
            tenant_id = server_dict.get('tenantId')
        if 'userId' in server_dict:
            user_id = server_dict.get('userId')

        server = Server(server_dict['id'], server_dict['diskConfig'],
                        server_dict['power_state'], progress,
                        server_dict['task_state'],
                        server_dict['vm_state'],
                        server_dict['name'], tenant_id,
                        server_dict['status'], server_dict['updated'],
                        server_dict['created'], server_dict['hostId'],
                        user_id, server_dict['accessIPv4'],
                        server_dict['accessIPv6'], addresses, flavor,
                        image, links, metadata)
        return server

    @classmethod
    def _dict_to_obj(cls, server_dict):
        '''Helper method to turn dictionary into Server instance.'''

        addresses = None
        flavor = None
        image = None
        links = None
        metadata = None

        if 'links' in server_dict:
            links = Links._dict_to_obj(server_dict['links'])
        if 'addresses' in server_dict:
            addresses = Addresses._dict_to_obj(server_dict['addresses'])
        if 'flavor' in server_dict:
            flavor = FlavorMin._dict_to_obj(server_dict['flavor'])
        if 'image' in server_dict:
            image = ImageMin._dict_to_obj(server_dict['image'])
        if 'metadata' in server_dict:
            metadata = Metadata._dict_to_obj(server_dict['metadata'])

        server = Server(
            server_dict['id'], server_dict.get('OS-DCF:diskConfig'),
            server_dict.get('OS-EXT-STS:power_state'),
            server_dict.get('progress', 0),
            server_dict.get('OS-EXT-STS:task_state'),
            server_dict.get('OS-EXT-STS:vm_state'),
            server_dict.get('name'), server_dict.get('tenant_id'),
            server_dict.get('status'), server_dict.get('updated'),
            server_dict.get('created'), server_dict.get('hostId'),
            server_dict.get('user_id'), server_dict.get('accessIPv4'),
            server_dict.get('accessIPv6'), addresses, flavor,
            image, links, metadata, server_dict.get('adminPass'))

        for each in server_dict:
            if each.startswith("{"):
                newkey = re.split("}", each)[1]
                setattr(server, newkey, server_dict[each])
        return server

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Server object to compare with
        @type other: Server
        @return: True if Server objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other,
                                               ['admin_pass', 'updated',
                                                'progress'])

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Server object to compare with
        @type other: Server
        @return: True if Server objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    def min_details(self):
        """
        @summary: Get the Minimum details of server
        @return: Minimum details of server
        @rtype: ServerMin
        """
        return ServerMin(name=self.name, id=self.id, links=self.links)


class ServerMin(Server):
    """
    @summary: Represents minimum details of a server
    """
    def __init__(self, **kwargs):
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: ServerMin object to compare with
        @type other: ServerMin
        @return: True if ServerMin objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default equals
        @param other: ServerMin object to compare with
        @type other: ServerMin
        @return: True if ServerMin objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Server instance.'''
        if element.find('server') is not None:
            element = element.find('server')
            server_dict = element.attrib
            servermin = ServerMin(**server_dict)
            servermin.links = Links._xml_ele_to_obj(element)
        return servermin

    @classmethod
    def _dict_to_obj(cls, server_dict):
        '''Helper method to turn dictionary into Server instance.'''
        servermin = ServerMin(**server_dict)
        if hasattr(servermin, 'links'):
            servermin.links = Links._dict_to_obj(servermin.links)
        '''
        Parse for those keys which have the namespace prefixed,
        strip the namespace out
        and take only the actual values such as diskConfig,
        power_state and assign to server obj
        '''
        for each in server_dict:
            if each.startswith("{"):
                newkey = re.split("}", each)[1]
                setattr(servermin, newkey, server_dict[each])

        return servermin


#New Version
class Addresses(AutoMarshallingModel):

    ROOT_TAG = 'addresses'

    class _NetworkAddressesList(BaseModel):

        def __init__(self):
            super(Addresses._NetworkAddressesList, self).__init__()
            self.addresses = []

        def __repr__(self):
            ret = ''
            for a in self.addresses:
                ret = ret + 'Address:\n\t%s' % str(a)
            return ret

        def append(self, addr_obj):
            self.addresses.append(addr_obj)

        @property
        def ipv4(self):
            for addr in self.addresses:
                if str(addr.version) == '4':
                    return str(str(IPy.IP(addr.addr)))
            return None

        @property
        def ipv6(self):
            for addr in self.addresses:
                if str(addr.version) == '6':
                    return str(str(IPy.IP(addr.addr)))
            return None

        @property
        def count(self):
            return len(self.addresses)

    class _AddrObj(BaseModel):

        def __init__(self, version=None, addr=None):
            super(Addresses._AddrObj, self).__init__()
            self.version = version
            if addr:
                self.addr = str(str(IPy.IP(addr)))
            else:
                self.addr = None

        def __repr__(self):
            ret = ''
            ret = ret + 'version: %s' % str(self.version)
            ret = ret + 'addr: %s' % str(self.addr)
            return ret

    def __init__(self, addr_dict):
        super(Addresses, self).__init__()

        #Preset properties that should be expected, if not always populated
        self.public = None
        self.private = None

        if len(addr_dict) > 1:
            ''' adddress_type is PUBLIC/PRIVATE '''
            for address_type in addr_dict:
                ''' address_list is list of address dictionaries'''
                address_list = addr_dict[address_type]
                ''' init a network object with empty addresses list '''
                network = self._NetworkAddressesList()
                for address in address_list:
                    addrobj = self._AddrObj(
                        version=int(address.get('version')),
                        addr=address.get('addr'))
                    network.addresses.append(addrobj)
                setattr(self, address_type, network)
        # Validation in case we have nested addresses in addresses
        else:
            big_addr_dict = addr_dict
            if big_addr_dict.get('addresses') is not None:
                addr_dict = big_addr_dict.get('addresses')
            for address_type in addr_dict:
                ''' address_list is list of address dictionaries'''
                address_list = addr_dict[address_type]
                ''' init a network object with empty addresses list '''
                network = self._NetworkAddressesList()
                for address in address_list:
                    addrobj = self._AddrObj(version=address.get('version'),
                                            addr=address.get('addr'))
                    network.addresses.append(addrobj)
                setattr(self, address_type, network)

    def get_by_name(self, label):
        try:
            ret = getattr(self, label)
        except AttributeError:
            ret = None
        return ret

    def __repr__(self):
        ret = '\n'
        ret = ret + '\npublic:\n\t\t%s' % str(self.public)
        ret = ret + '\nprivate:\n\t\t%s' % str(self.private)
        return ret

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return Addresses(json_dict)

    @classmethod
    def _dict_to_obj(cls, serialized_str):
        return Addresses(serialized_str)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        addresses = {}
        if element.tag != 'network':
            networks = element.findall('network')
            for network in networks:
                network_id = network.attrib.get('id')
                addresses[network_id] = []
                for ip in network:
                    addresses[network_id].append(ip.attrib)
        else:
            networks = element
            network_id = networks.attrib.get('id')
            addresses[network_id] = []
            for ip in networks:
                addresses[network_id].append(ip.attrib)

        return Addresses(addresses)
