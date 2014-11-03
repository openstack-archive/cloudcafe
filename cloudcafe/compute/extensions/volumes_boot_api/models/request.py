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
from cloudcafe.compute.servers_api.models.requests import Personality


class CreateServerFromVolume(AutoMarshallingModel):

    def __init__(self, name, flavor_ref, block_device_mapping_v2,
                 max_count=None, min_count=None, networks=None,
                 image_ref=None, personality=None, user_data=None,
                 metadata=None, accessIPv4=None, accessIPv6=None,
                 disk_config=None, admin_pass=None, key_name=None,
                 config_drive=None, scheduler_hints=None,
                 security_groups=None):

        super(CreateServerFromVolume, self).__init__()
        self.name = name
        self.flavor_ref = flavor_ref
        self.block_device_mapping_v2 = block_device_mapping_v2
        self.max_count = max_count
        self.min_count = min_count
        self.networks = networks
        self.image_ref = image_ref
        self.personality = personality
        self.user_data = user_data
        self.metadata = metadata
        self.accessIPv4 = accessIPv4
        self.accessIPv6 = accessIPv6
        self.disk_config = disk_config
        self.admin_pass = admin_pass
        self.key_name = key_name
        self.config_drive = config_drive
        self.scheduler_hints = scheduler_hints
        self.security_groups = security_groups

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'flavorRef': self.flavor_ref,
            'block_device_mapping_v2': self.block_device_mapping_v2,
            'max_count': self.max_count,
            'min_count': self.min_count,
            'networks': self.networks,
            'imageRef': self.image_ref,
            'personality': self.personality,
            'user_data': self.user_data,
            'metadata': self.metadata,
            'accessIPv4': self.accessIPv4,
            'accessIPv6': self.accessIPv6,
            'OS-DCF:diskConfig': self.disk_config,
            'adminPass': self.admin_pass,
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
        elements_dict = {
            'name': self.name,
            'flavorRef': self.flavor_ref,
            'max_count': self.max_count,
            'min_count': self.min_count,
            'image_ref': self.image_ref,
            'user_data': self.user_data,
            'accessIPv4': self.accessIPv4,
            'accessIPv6': self.accessIPv6,
            'adminPass': self.admin_pass,
            'key_name': self.key_name,
            'config_drive': self.config_drive,
            'security_groups': self.security_groups
        }
        element = ET.Element('server')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        block_device_ele = ET.Element('block_device_mapping_v2')
        block_device_ele.append(BlockDeviceMappingV2._obj_to_xml(
            self.block_device_mapping_v2))
        element.append(block_device_ele)
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
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        if self.disk_config is not None:
            element.set('xmlns:OS-DCF',
                        Constants.XML_API_DISK_CONFIG_NAMESPACE)
            element.set('OS-DCF:diskConfig', self.disk_config)
        element = self._set_xml_etree_element(element, elements_dict)
        return ''.join([Constants.XML_HEADER, ET.tostring(element)])


class BlockDeviceMappingV2(AutoMarshallingModel):
    """
    @summary: Block Device Mapping Request Object for Version 2 Havana
     of boot from volume extension
    """
    ROOT_TAG = 'block_device_mapping_v2'

    def __init__(self, boot_index, uuid, volume_size, source_type,
                 destination_type, delete_on_termination):
        super(BlockDeviceMappingV2, self).__init__()
        self.boot_index = boot_index
        self.uuid = uuid
        self.volume_size = volume_size
        self.source_type = source_type
        self.destination_type = destination_type
        self.delete_on_termination = delete_on_termination

    @classmethod
    def _obj_to_json(self):
        body = {
            'boot_index': self.boot_index,
            'uuid': self.uuid,
            'volume_size': self.volume_size,
            'source_type': self.source_type,
            'destination_type': self.destination_type,
            'delete_on_termination': self.delete_on_termination
        }

        body = self._remove_empty_values(body)
        return json.dumps({'block_device_mapping_v2': body})

    @classmethod
    def _obj_to_xml(self, list_dicts):
        device_dict = None
        for device_dict in list_dicts:
            device_element = ET.Element('block_device_mapping_v2')
            device_element.set('boot_index', device_dict.get('boot_index'))
            device_element.set('uuid', device_dict.get('uuid'))
            device_element.set('volume_size', device_dict.get('volume_size'))
            device_element.set('source_type', device_dict.get('source_type'))
            device_element.set('destination_type',
                               device_dict.get('destination_type'))
            device_element.set('delete_on_termination',
                               device_dict.get('delete_on_termination'))
        return device_element
