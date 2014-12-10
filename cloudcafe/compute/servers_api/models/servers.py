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
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel, \
    AutoMarshallingListModel
from cafe.engine.models.base import BaseModel
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.types import ComputeTaskStates
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.compute.common.models.link import Links
from cloudcafe.compute.common.models.metadata import Metadata
from cloudcafe.compute.flavors_api.models.flavor import Flavor, FlavorMin
from cloudcafe.compute.images_api.models.image import Image, ImageMin


class Server(AutoMarshallingModel):

    def __init__(self, id=None, disk_config=None, power_state=None,
                 progress=None, task_state=None, vm_state=None, name=None,
                 tenant_id=None, status=None, updated=None, created=None,
                 host_id=None, user_id=None, accessIPv4=None, accessIPv6=None,
                 addresses=None, flavor=None, image=None, links=None,
                 metadata=None, admin_pass=None, key_name=None,
                 config_drive=None, host=None, instance_name=None,
                 hypervisor_name=None, security_groups=None, fault=None):
        super(Server, self).__init__()

        self.disk_config = disk_config
        self.config_drive = config_drive
        try:
            self.power_state = int(power_state)
        except TypeError:
            self.power_state = 0
        self.progress = progress
        self.task_state = task_state or ComputeTaskStates.NONE
        self.vm_state = vm_state
        self.name = name
        self.hypervisor_name = hypervisor_name
        self.id = id
        self.tenant_id = tenant_id
        self.status = status
        self.updated = updated
        self.created = created
        self.host_id = host_id
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
        self.key_name = key_name
        self.host = host
        self.instance_name = instance_name
        self.security_groups = security_groups
        self.fault = fault

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a Server based on the json serialized_str
        passed in
        """
        ret = None
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict['server'])
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        Returns an instance of a Server based on the xml serialized_str
        passed in
        """
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_EXTENDED_STATUS_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_DISK_CONFIG_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_ATOM_NAMESPACE)
        ret = cls._xml_ele_to_obj(element)
        return ret

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """Helper method to turn ElementTree instance to Server instance."""
        server = element.attrib

        addresses = None
        flavor = None
        image = None
        metadata = None
        fault = None
        links = Links._xml_ele_to_obj(element)

        if element.find('addresses') is not None:
            addresses = Addresses._xml_ele_to_obj(element.find('addresses'))
        if element.find('flavor') is not None:
            flavor = Flavor._xml_ele_to_obj(element.find('flavor'))
        if element.find('image'):
            image = Image._xml_ele_to_obj(element.find('image'))
        if element.find('metadata') is not None:
            metadata = Metadata._xml_ele_to_obj(element.find('metadata'))
        if element.find('fault') is not None:
            fault = Fault._xml_ele_to_obj(element.find('flavor'))

        if 'progress' in server:
            progress = (server.get('progress')
                        and int(server.get('progress')))
        else:
            progress = None

        server = Server(
            id=server.get('id'), disk_config=server.get('diskConfig'),
            power_state=server.get('power_state'), progress=progress,
            task_state=server.get('task_state').lower(),
            vm_state=server.get('vm_state'), name=server.get('name'),
            tenant_id=server.get('tenant_id'), status=server.get('status'),
            updated=server.get('updated'), created=server.get('created'),
            host_id=server.get('hostId'), user_id=server.get('userId'),
            accessIPv4=server.get('accessIPv4'),
            config_drive=server.get('config_drive'),
            accessIPv6=server.get('accessIPv6'), addresses=addresses,
            flavor=flavor, image=image, links=links, metadata=metadata,
            admin_pass=server.get('adminPass'),
            key_name=server.get('key_name'), host=server.get('host'),
            instance_name=server.get('instance_name'),
            hypervisor_name=server.get('hypervisor_hostname'),
            security_groups=server.get('security_groups'),
            fault=fault)

        return server

    @classmethod
    def _dict_to_obj(cls, server_dict):
        """Helper method to turn dictionary into Server instance."""

        addresses = None
        flavor = None
        image = None
        links = None
        metadata = None
        fault = None

        if 'links' in server_dict:
            links = Links._dict_to_obj(server_dict['links'])
        if 'addresses' in server_dict:
            addresses = Addresses._dict_to_obj(server_dict['addresses'])
        if 'flavor' in server_dict:
            flavor = FlavorMin._dict_to_obj(server_dict['flavor'])
        if 'image' in server_dict and server_dict.get('image'):
            image = ImageMin._dict_to_obj(server_dict['image'])
        if 'metadata' in server_dict:
            metadata = Metadata._dict_to_obj(server_dict['metadata'])
        if 'fault' in server_dict:
            fault = Fault._dict_to_obj(server_dict['fault'])

        server = Server(
            id=server_dict.get('id') or server_dict.get('uuid'),
            disk_config=server_dict.get('OS-DCF:diskConfig'),
            power_state=server_dict.get('OS-EXT-STS:power_state'),
            progress=server_dict.get('progress', 0),
            task_state=server_dict.get('OS-EXT-STS:task_state'),
            vm_state=server_dict.get('OS-EXT-STS:vm_state'),
            name=server_dict.get('name'),
            config_drive=server_dict.get('config_drive'),
            tenant_id=server_dict.get('tenant_id'),
            status=server_dict.get('status'),
            updated=server_dict.get('updated'),
            created=server_dict.get('created'),
            host_id=server_dict.get('hostId'),
            user_id=server_dict.get('user_id'),
            accessIPv4=server_dict.get('accessIPv4'),
            accessIPv6=server_dict.get('accessIPv6'), addresses=addresses,
            flavor=flavor, image=image, links=links, metadata=metadata,
            admin_pass=server_dict.get('adminPass'),
            key_name=server_dict.get('key_name'),
            host=server_dict.get('OS-EXT-SRV-ATTR:host'),
            instance_name=server_dict.get('OS-EXT-SRV-ATTR:instance_name'),
            hypervisor_name=server_dict.get(
                'OS-EXT-SRV-ATTR:hypervisor_hostname'),
            security_groups=server_dict.get('security_groups'),
            fault=fault)

        return server

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other,
                                               ['admin_pass', 'updated',
                                                'progress'])

    def __ne__(self, other):
        return not self == other

    def min_details(self):
        return ServerMin(name=self.name, id=self.id, links=self.links)


class Fault(AutoMarshallingModel):

    def __init__(
            self, message=None, code=None, created=None):
        self.message = message
        self.code = code
        self.created = created

    @classmethod
    def _xml_ele_to_obj(cls, element):
        fault_dict = element.attrib
        return cls._dict_to_obj(fault_dict)

    @classmethod
    def _dict_to_obj(cls, fault_dict):
        fault = Fault(
            message=fault_dict.get('message'),
            code=fault_dict.get('code'),
            created=fault_dict.get('created'))
        return fault


class ServerMin(Server):

    def __init__(self, id=None, name=None, links=None):
        super(ServerMin, self).__init__()
        self.id = id
        self.name = name
        self.links = links

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        server_dict = element.attrib
        links = Links._xml_ele_to_obj(element)
        server = ServerMin(id=server_dict.get('id'),
                           name=server_dict.get('name'), links=links)
        return server

    @classmethod
    def _dict_to_obj(cls, server_dict):
        links = Links._dict_to_obj(server_dict['links'])
        server = ServerMin(id=server_dict.get('id'),
                           name=server_dict.get('name'), links=links)
        return server


class Servers(AutoMarshallingListModel):

    server_type = Server

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('servers'))

    @classmethod
    def _list_to_obj(cls, server_dict_list):
        servers = Servers()
        for server_dict in server_dict_list:
            server = cls.server_type._dict_to_obj(server_dict)
            servers.append(server)
        return servers

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        if element.tag != 'servers':
            return None
        return cls._xml_list_to_obj(element.findall('server'))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        servers = Servers()
        for ele in xml_list:
            servers.append(cls.server_type._xml_ele_to_obj(ele))
        return servers


class ServerMins(AutoMarshallingListModel):

    server_type = ServerMin

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('servers'))

    @classmethod
    def _list_to_obj(cls, server_dict_list):
        servers = ServerMins()
        for server_dict in server_dict_list:
            server = cls.server_type._dict_to_obj(server_dict)
            servers.append(server)
        return servers

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        if element.tag != 'servers':
            return None
        return cls._xml_list_to_obj(element.findall('server'))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        servers = ServerMins()
        for ele in xml_list:
            servers.append(cls.server_type._xml_ele_to_obj(ele))
        return servers


class Addresses(AutoMarshallingModel):

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

        # Preset properties that should be expected, if not always populated
        self.public = None
        self.private = None

        if len(addr_dict) > 1:
            # adddress_type is PUBLIC/PRIVATE
            for address_type in addr_dict:
                # address_list is list of address dictionaries
                address_list = addr_dict[address_type]
                # init a network object with empty addresses list
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
                # address_list is list of address dictionaries
                address_list = addr_dict[address_type]
                # init a network object with empty addresses list
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


class InstanceAction(AutoMarshallingModel):

    def __init__(self, instance_uuid, user_id, start_time, request_id,
                 action, message, project_id):
        self.instance_uuid = instance_uuid
        self.user_id = user_id
        self.start_time = start_time
        self.request_id = request_id
        self.action = action
        self.message = message
        self.project_id = project_id

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return InstanceAction(**json_dict)

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        return not self == other


class InstanceActions(AutoMarshallingModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        json_dict = json.loads(serialized_str)
        actions_list = json_dict.get('instanceActions')

        for action in actions_list:
            ret.append(InstanceAction(**action))
        return ret
