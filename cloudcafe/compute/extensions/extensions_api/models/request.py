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


class CreateV2BlockServer(AutoMarshallingModel):

    def __init__(self, name, flavor_ref, block_device_mapping_v2,
                 max_count=None, min_count=None, networks=None):

        super(CreateV2BlockServer, self).__init__()
        self.name = name
        self.flavor_ref = flavor_ref
        self.block_device_mapping_v2 = block_device_mapping_v2
        self.max_count = max_count
        self.min_count = min_count
        self.networks = networks

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'flavorRef': self.flavor_ref,
            'block_device_mapping_v2': self.block_device_mapping_v2,
            'max_count': self.max_count,
            'min_count': self.min_count,
            'networks': self.networks
        }

        body = self._remove_empty_values(body)
        main_body = {'server': body}

        return json.dumps(main_body)

    def _obj_to_xml(self):
        element = ET.Element('server')
        xml = Constants.XML_HEADER
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('name', self.name)
        element.set('flavorRef', self.flavor_ref)
        block_device_ele = ET.Element('block_device_mapping_v2')
        block_device_ele.append(BlockDeviceMappingV2._obj_to_xml(
            self.block_device_mapping_v2))
        element.append(block_device_ele)
        if self.max_count is not None:
            element.set('max_count', self.max_count)
        if self.min_count is not None:
            element.set('min_count', self.min_count)
        if self.networks is not None:
            networks_ele = ET.Element('networks')
            for network_id in self.networks:
                network = ET.Element('network')
                network.set('uuid', network_id['uuid'])
                networks_ele.append(network)
            element.append(networks_ele)
        xml += ET.tostring(element)
        return xml


class BlockDeviceMappingV2(AutoMarshallingModel):
    """
    @summary: Block Device Mapping Request Object for Version 2 Havana
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
        for pers_dict in list_dicts:
            pers_element = ET.Element('block_device_mapping_v2')
            pers_element.set('boot_index', pers_dict.get('boot_index'))
            pers_element.set('uuid', pers_dict.get('uuid'))
            pers_element.set('volume_size', pers_dict.get('volume_size'))
            pers_element.set('source_type', pers_dict.get('source_type'))
            pers_element.set('destination_type',
                             pers_dict.get('destination_type'))
            pers_element.set('delete_on_termination',
                             pers_dict.get('delete_on_termination'))
        return pers_element
