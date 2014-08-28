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

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.models.metadata import Metadata


class CreateServer(AutoMarshallingModel):

    def __init__(self, name, image_ref, flavor_ref, admin_pass=None,
                 disk_config=None, metadata=None, personality=None,
                 block_device_mapping=None, user_data=None, accessIPv4=None,
                 accessIPv6=None, networks=None, key_name=None,
                 config_drive=None, scheduler_hints=None,
                 security_groups=None):

        super(CreateServer, self).__init__()
        self.name = name
        self.image_ref = image_ref
        self.flavor_ref = flavor_ref
        self.disk_config = disk_config
        self.admin_pass = admin_pass
        self.metadata = metadata
        self.personality = personality
        self.block_device_mapping = block_device_mapping
        self.user_data = user_data
        self.accessIPv4 = accessIPv4
        self.accessIPv6 = accessIPv6
        self.networks = networks
        self.key_name = key_name
        self.config_drive = config_drive
        self.scheduler_hints = scheduler_hints
        self.security_groups = security_groups

    def _obj_to_json(self):

        if self.personality == []:
            self.personality = None

        body = {
            'name': self.name,
            'imageRef': self.image_ref,
            'flavorRef': self.flavor_ref,
            'OS-DCF:diskConfig': self.disk_config,
            'adminPass': self.admin_pass,
            'metadata': self.metadata,
            'accessIPv4': self.accessIPv4,
            'accessIPv6': self.accessIPv6,
            'personality': self.personality,
            'block_device_mapping': self.block_device_mapping,
            'user_data': self.user_data,
            'networks': self.networks,
            'key_name': self.key_name,
            'config_drive': self.config_drive,
            'security_groups': self.security_groups
        }

        body = self._remove_empty_values(body)
        main_body = {'server': body}

        if self.scheduler_hints:
            main_body['os:scheduler_hints'] = self.scheduler_hints

        return json.dumps(main_body)

    def _obj_to_xml(self):
        element = ET.Element('server')
        xml = Constants.XML_HEADER
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('name', self.name)
        element.set('imageRef', self.image_ref)
        element.set('flavorRef', self.flavor_ref)
        if self.admin_pass is not None:
            element.set('adminPass', self.admin_pass)
        if self.disk_config is not None:
            element.set('xmlns:OS-DCF',
                        Constants.XML_API_DISK_CONFIG_NAMESPACE)
            element.set('OS-DCF:diskConfig', self.disk_config)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        if self.networks is not None:
            networks_ele = ET.Element('networks')
            for network_id in self.networks:
                network = ET.Element('network')
                network.set('uuid', network_id['uuid'])
                networks_ele.append(network)
            element.append(networks_ele)
        if self.personality is not None:
            personality_ele = ET.Element('personality')
            personality_ele.append(Personality._obj_to_xml(self.personality))
            element.append(personality_ele)
        if self.block_device_mapping is not None:
            block_device_ele = ET.Element('block_device_mapping')
            block_device_ele.append(BlockDeviceMapping._obj_to_xml(
                self.block_device_mapping))
            element.append(block_device_ele)
        if self.user_data is not None:
            element.set('user_data', self.user_data)
        if self.accessIPv4 is not None:
            element.set('accessIPv4', self.accessIPv4)
        if self.accessIPv6 is not None:
            element.set('accessIPv6', self.accessIPv6)
        if self.key_name is not None:
            element.set('key_name', self.key_name)
        if self.config_drive is not None:
            element.set('config_drive', self.config_drive)
        if self.scheduler_hints is not None:
            hints_ele = ET.Element('OS-SCH-HNT:scheduler_hints')
            for key, value in self.metadata.iteritems():
                meta_element = ET.Element(key)
                meta_element.text = value
                hints_ele.append(meta_element)
        xml += ET.tostring(element)
        return xml


class UpdateServer(AutoMarshallingModel):

    def __init__(self, name=None, metadata=None,
                 accessIPv4=None, accessIPv6=None):
        super(UpdateServer, self).__init__()
        self.name = name
        self.metadata = metadata
        self.accessIPv4 = accessIPv4
        self.accessIPv6 = accessIPv6

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'metadata': self.metadata,
            'accessIPv4': self.accessIPv4,
            'accessIPv6': self.accessIPv6,
        }

        body = self._remove_empty_values(body)
        return json.dumps({'server': body})

    def _obj_to_xml(self):
        element = ET.Element('server')
        xml = Constants.XML_HEADER
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        if self.name is not None:
            element.set('name', self.name)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        if self.accessIPv4 is not None:
            element.set('accessIPv4', self.accessIPv4)
        if self.accessIPv6 is not None:
            element.set('accessIPv6', self.accessIPv6)
        xml += ET.tostring(element)
        return xml


class Reboot(AutoMarshallingModel):

    def __init__(self, reboot_type):
        super(Reboot, self).__init__()
        self.type = reboot_type

    def _obj_to_json(self):
        body = {'type': self.type}
        return json.dumps({'reboot': body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('reboot')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('type', self.type)
        xml += ET.tostring(element)
        return xml


class Personality(AutoMarshallingModel):
    """
    @summary: Personality Request Object for Server
    """
    ROOT_TAG = 'personality'

    def __init__(self, type):
        super(Personality, self).__init__()
        self.type = type

    @classmethod
    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    @classmethod
    def _obj_to_xml(self, list_dicts):
        for pers_dict in list_dicts:
            pers_element = ET.Element('file')
            pers_element.set('path', pers_dict.get('path'))
            pers_element.text = pers_dict.get('contents')
        return pers_element


class BlockDeviceMapping(AutoMarshallingModel):
    """
    @summary: Block Device Mapping Request Object for Server
    """
    ROOT_TAG = 'block_device_mapping'

    def __init__(self, volume_id, delete_on_termination, device_name,
                 size=None, type=None):
        super(BlockDeviceMapping, self).__init__()
        self.volume_id = volume_id
        self.delete_on_termination = delete_on_termination
        self.device_name = device_name
        self.size = size
        self.type = type

    @classmethod
    def _obj_to_json(self):
        body = {
            'volume_id': self.volume_id,
            'delete_on_termination': self.delete_on_termination,
            'device_name': self.device_name,
            'size': self.size,
            'type': self.type
        }

        body = self._remove_empty_values(body)
        return json.dumps({'block_device_mapping': body})

    @classmethod
    def _obj_to_xml(self, list_dicts):
        for pers_dict in list_dicts:
            pers_element = ET.Element('block_device_mapping')
            pers_element.set('volume_id', pers_dict.get('volume_id'))
            pers_element.set('delete_on_termination',
                             pers_dict.get('delete_on_termination'))
            pers_element.set('device_name', pers_dict.get('device_name'))
            if pers_dict.get('size') is not None:
                pers_element.set('size', pers_dict.get('size'))
            if pers_dict.get('type') is not None:
                pers_element.set('type', pers_dict.get('type'))
        return pers_element


class Rebuild(AutoMarshallingModel):
    """
    @summary: Rebuild Request Object for Server
    """

    def __init__(self, name, image_ref, admin_pass=None,
                 disk_config=None, metadata=None, personality=None,
                 block_device_mapping=None, user_data=None, accessIPv4=None,
                 accessIPv6=None, networks=None, key_name=None,
                 config_drive=None, security_groups=None):
        super(Rebuild, self).__init__()
        self.name = name
        self.image_ref = image_ref
        self.disk_config = disk_config
        self.admin_pass = admin_pass
        self.metadata = metadata
        self.personality = personality
        self.block_device_mapping = block_device_mapping
        self.user_data = user_data
        self.accessIPv4 = accessIPv4
        self.accessIPv6 = accessIPv6
        self.networks = networks
        self.key_name = key_name
        self.config_drive = config_drive
        self.security_groups = security_groups

    def _obj_to_json(self):

        if self.personality == []:
            self.personality = None

        body = {
            'name': self.name,
            'imageRef': self.image_ref,
            'OS-DCF:diskConfig': self.disk_config,
            'adminPass': self.admin_pass,
            'metadata': self.metadata,
            'accessIPv4': self.accessIPv4,
            'accessIPv6': self.accessIPv6,
            'personality': self.personality,
            'block_device_mapping': self.block_device_mapping,
            'user_data': self.user_data,
            'networks': self.networks,
            'key_name': self.key_name,
            'config_drive': self.config_drive,
            'security_groups': self.security_groups
        }

        body = self._remove_empty_values(body)
        return json.dumps({'rebuild': body})

    def _obj_to_xml(self):
        element = ET.Element('rebuild')
        xml = Constants.XML_HEADER
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('name', self.name)
        element.set('imageRef', self.image_ref)
        if self.admin_pass is not None:
            element.set('adminPass', self.admin_pass)
        if self.disk_config is not None:
            element.set('xmlns:OS-DCF',
                        Constants.XML_API_DISK_CONFIG_NAMESPACE)
            element.set('OS-DCF:diskConfig', self.disk_config)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        if self.networks is not None:
            networks_ele = ET.Element('networks')
            for network_id in self.networks:
                network = ET.Element('network')
                network.set('uuid', network_id['uuid'])
                networks_ele.append(network)
            element.append(networks_ele)
        if self.personality is not None:
            personality_ele = ET.Element('personality')
            personality_ele.append(Personality._obj_to_xml(self.personality))
            element.append(personality_ele)
        if self.block_device_mapping is not None:
            block_device_ele = ET.Element('block_device_mapping')
            block_device_ele.append(BlockDeviceMapping._obj_to_xml(
                self.block_device_mapping))
            element.append(block_device_ele)
        if self.user_data is not None:
            element.set('user_data', self.user_data)
        if self.accessIPv4 is not None:
            element.set('accessIPv4', self.accessIPv4)
        if self.accessIPv6 is not None:
            element.set('accessIPv6', self.accessIPv6)
        if self.key_name is not None:
            element.set('key_name', self.key_name)
        if self.config_drive is not None:
            element.set('config_drive', self.config_drive)
        xml += ET.tostring(element)
        return xml


class Resize(AutoMarshallingModel):
    """
    @summary: Resize Request Object for Server
    """

    def __init__(self, flavor_ref, disk_config=None):
        super(Resize, self).__init__()
        self.flavor_ref = flavor_ref
        self.disk_config = disk_config

    def _obj_to_json(self):
        body = {
            'flavorRef': self.flavor_ref,
            'diskConfig': self.disk_config
        }
        body = self._remove_empty_values(body)
        return json.dumps({'resize': body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('resize')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('flavorRef', self.flavor_ref)
        if self.disk_config is not None:
            element.set('xmlns:OS-DCF', Constants.XML_API_ATOM_NAMESPACE)
            element.set('OS-DCF:diskConfig', self.disk_config)
        xml += ET.tostring(element)
        return xml


class ResetState(AutoMarshallingModel):
    """
    @summary: Reset State Request Object for Server
    """

    def __init__(self, state):
        super(ResetState, self).__init__()
        self.state = state

    def _obj_to_json(self):
        body = {'state': self.state}
        return json.dumps({'os-resetState': body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('os-resetState')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('state', self.state)
        xml += ET.tostring(element)
        return xml


class ConfirmResize(AutoMarshallingModel):
    """
    @summary: Confirm Resize Request Object for Server
    """

    def _obj_to_json(self):
        return json.dumps({'confirmResize': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('confirmResize')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class RevertResize(AutoMarshallingModel):
    """
    @summary: Revert Resize Request Object for Server

    """

    def _obj_to_json(self):
        return json.dumps({'revertResize': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('revertResize')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class MigrateServer(AutoMarshallingModel):
    """
    @summary: Migrate Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'migrate': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('migrate')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class LiveMigrateServer(AutoMarshallingModel):
    """
    @summary: Live Migration Request Object
    """

    def __init__(self, disk_over_commit=None,
                 block_migration=None, host=None):
        super(LiveMigrateServer, self).__init__()
        self.disk_over_commit = disk_over_commit
        self.block_migration = block_migration
        self.host = host

    def _obj_to_json(self):
        body = {
            'disk_over_commit': self.disk_over_commit,
            'block_migration': self.block_migration,
            'host': self.host
        }
        return json.dumps({'os-migrateLive': body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('os-migrateLive')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('disk_over_commit', self.disk_over_commit)
        element.set('block_migration', self.block_migration)
        element.set('host', self.host)
        xml += ET.tostring(element)
        return xml


class ConfirmServerMigration(AutoMarshallingModel):
    """
    @summary: Confirm Server Migration Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'confirmResize': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('confirmResize')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Lock(AutoMarshallingModel):
    """
    @summary: Lock Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'lock': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('lock')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Unlock(AutoMarshallingModel):
    """
    @summary: Unlock Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'unlock': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('unlock')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Start(AutoMarshallingModel):
    """
    @summary: Start Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'os-start': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('os-start')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Stop(AutoMarshallingModel):
    """
    @summary: Stop Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'os-stop': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('os-stop')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Suspend(AutoMarshallingModel):
    """
    @summary: Suspend Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'suspend': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('suspend')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Resume(AutoMarshallingModel):
    """
    @summary: Resume Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'resume': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('resume')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Pause(AutoMarshallingModel):
    """
    @summary: Pause Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'pause': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('pause')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Unpause(AutoMarshallingModel):
    """
    @summary: Unpause Server Request Object
    """

    def _obj_to_json(self):
        return json.dumps({'unpause': {}})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('unpause')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class CreateImage(AutoMarshallingModel):
    """
    Create Image Server Action Request Object
    """

    def __init__(self, name, metadata=None):
        super(CreateImage, self).__init__()
        self.name = name
        self.metadata = metadata

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'metadata': self.metadata
        }
        body = self._remove_empty_values(body)
        return json.dumps({'createImage': body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('createImage')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        element.set('name', self.name)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        xml += ET.tostring(element)
        return xml


class CreateBackup(AutoMarshallingModel):
    """
    Create Backup Server Action Request Object
    """

    def __init__(self, name, backup_type, backup_rotation, metadata=None):
        super(CreateBackup, self).__init__()
        self.name = name
        self.backup_type = backup_type
        self.rotation = backup_rotation
        self.metadata = metadata

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'backup_type': self.backup_type,
            'rotation': self.rotation,
            'metadata': self.metadata
        }
        body = self._remove_empty_values(body)
        return json.dumps({'createBackup': body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        element.set('name', self.name)
        element.set('backup_type', self.backup_type)
        element.set('rotation', self.rotation)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        xml += ET.tostring(element)
        return xml


class ChangePassword(AutoMarshallingModel):

    def __init__(self, admin_password):
        super(ChangePassword, self).__init__()
        self.admin_pass = admin_password

    def _obj_to_json(self):
        body = {'adminPass': self.admin_pass}
        return json.dumps({'changePassword': body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('adminPass', self.admin_pass)
        xml += ET.tostring(element)
        return xml


class AddFixedIP(AutoMarshallingModel):
    """
    Add Fixed IP Action Request Object
    """

    def __init__(self, network_id):
        super(AddFixedIP, self).__init__()
        self.network_id = network_id

    def _obj_to_json(self):
        body = {'networkId': self.network_id}
        return json.dumps({'addFixedIp': body})


class RemoveFixedIP(AutoMarshallingModel):
    """
    Remove Fixed IP Action Request Object
    """

    def __init__(self, network_id):
        super(RemoveFixedIP, self).__init__()
        self.network_id = network_id

    def _obj_to_json(self):
        body = {'networkId': self.network_id}
        return json.dumps({'removeFixedIp': body})


class AddSecurityGroup(AutoMarshallingModel):
    """
    Add Security Group Action Request Object
    """

    def __init__(self, name):
        super(AddSecurityGroup, self).__init__()
        self.name = name

    def _obj_to_json(self):
        json_dict = {"name": self.name}
        return json.dumps({'addSecurityGroup': json_dict})

    def _obj_to_xml(self):
        element = ET.Element('addSecurityGroup')
        name_ele = ET.Element('name')
        name_ele.text = self.name
        element.append(name_ele)
        xml = ET.tostring(element)
        return xml


class AssociateFloatingIP(AutoMarshallingModel):

    def __init__(self, address):
        super(AssociateFloatingIP, self).__init__()
        self.address = address

    def _obj_to_json(self):
        json_dict = {"address": self.address}
        return json.dumps({'addFloatingIp': json_dict})


class DisassociateFloatingIP(AutoMarshallingModel):

    def __init__(self, address):
        super(DisassociateFloatingIP, self).__init__()
        self.address = address

    def _obj_to_json(self):
        json_dict = {"address": self.address}
        return json.dumps({'removeFloatingIp': json_dict})


