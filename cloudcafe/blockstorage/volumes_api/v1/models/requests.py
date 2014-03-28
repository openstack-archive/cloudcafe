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
from xml.etree import ElementTree

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.blockstorage.volumes_api.common.models.automarshalling import \
    CommonModelProperties


class VolumeRequest(CommonModelProperties, AutoMarshallingModel):

    def __init__(
            self, size=None, volume_type=None, display_name=None,
            display_description=None, metadata=None, availability_zone=None,
            snapshot_id=None, bootable=None, source_volid=None,
            image_ref=None):

        super(VolumeRequest, self).__init__()
        self._name = None
        self._description = None
        self.size = size
        self.volume_type = volume_type
        self.display_name = display_name
        self.display_description = display_description
        self.metadata = metadata or dict()
        self.availability_zone = availability_zone
        self.snapshot_id = snapshot_id
        self.bootable = bootable
        self.source_volid = source_volid
        self.image_ref = image_ref

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_dict(self):
        volume_attrs = {
            "size": self.size,
            "volume_type": self.volume_type,
            "display_name": self.name,
            "display_description": self.description,
            "metadata": self.metadata,
            "availability_zone": self.availability_zone,
            "bootable": self.bootable,
            "imageRef": self.image_ref,
            "source_volid": self.source_volid,
            "snapshot_id": self.snapshot_id}

        return {'volume': self._remove_empty_values(volume_attrs)}

    def _obj_to_xml_ele(self):
        element = ElementTree.Element('volume')
        volume_attrs = {
            "size": self.size,
            "volume_type": self.volume_type,
            "display_name": self.name,
            "display_description": self.description,
            "availability_zone": self.availability_zone,
            "bootable": self.bootable,
            "imageRef": self.image_ref,
            "source_volid": self.source_volid,
            "snapshot_id": self.snapshot_id}
        element = self._set_xml_etree_element(element, volume_attrs)

        if len(self.metadata.keys()) > 0:
            metadata_element = ElementTree.Element('metadata')
            for key in self.metadata.keys():
                meta_element = ElementTree.Element('meta')
                meta_element.set('key', key)
                meta_element.text = self.metadata[key]
                metadata_element.append(meta_element)
            element.append(metadata_element)

        return element

    def _obj_to_xml(self):
        return ElementTree.tostring(self._obj_to_xml_ele())


class VolumeSnapshotRequest(CommonModelProperties, AutoMarshallingModel):

    def __init__(
            self, volume_id, force=True, display_name=None,
            display_description=None):

        super(VolumeSnapshotRequest, self).__init__()
        self._name = None
        self._description = None
        self.volume_id = volume_id
        self.display_name = display_name
        self.display_description = display_description
        self.force = force

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_dict(self):
        snapshot_attrs = {
            "volume_id": self.volume_id,
            "display_name": self.name,
            "display_description": self.description,
            "force": self.force}

        return {"snapshot": self._remove_empty_values(snapshot_attrs)}

    def _obj_to_xml(self):
        return ElementTree.tostring(self._obj_to_xml_ele())

    def _obj_to_xml_ele(self):
        element = ElementTree.Element('snapshot')
        snapshot_attrs = {
            "volume_id": self.volume_id,
            "display_name": self.name,
            "display_description": self.description,
            "force": str(self.force)}
        return self._set_xml_etree_element(element, snapshot_attrs)
