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

# Import common requests
from cloudcafe.blockstorage.volumes_api.common.models.requests import \
    StatusResetRequest, VolumeTransferRequest


class VolumeRequest(CommonModelProperties, AutoMarshallingModel):

    def __init__(
            self, size=None, volume_type=None, name=None,
            description=None, metadata=None, availability_zone=None,
            snapshot_id=None, bootable=None, source_volid=None,
            image_ref=None):

        super(VolumeRequest, self).__init__()
        self._name = None
        self._description = None
        self.size = size
        self.volume_type = volume_type
        self.name = name
        self.description = description
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
            "name": self.name,
            "description": self.description,
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
            "name": self.name,
            "description": self.description,
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
            self, volume_id, force=True, name=None, description=None):

        super(VolumeSnapshotRequest, self).__init__()
        self._name = None
        self._description = None
        self.volume_id = volume_id
        self.name = name
        self.description = description
        self.force = force

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_dict(self):
        snapshot_attrs = {
            "volume_id": self.volume_id,
            "name": self.name,
            "description": self.description,
            "force": self.force}

        return {"snapshot": self._remove_empty_values(snapshot_attrs)}

    def _obj_to_xml(self):
        return ElementTree.tostring(self._obj_to_xml_ele())

    def _obj_to_xml_ele(self):
        element = ElementTree.Element('snapshot')
        snapshot_attrs = {
            "volume_id": self.volume_id,
            "name": self.name,
            "description": self.description,
            "force": str(self.force)}
        return self._set_xml_etree_element(element, snapshot_attrs)


class VolumeTypeCreateRequest(AutoMarshallingModel):

    def __init__(self, name, extra_specs=None):
        super(VolumeTypeCreateRequest, self).__init__()
        self.name = name
        self.extra_specs = extra_specs

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_dict(self):
        attrs = {
            "name": self.name,
            "extra_specs": self.extra_specs}
        return dict(volume_type=self._remove_empty_values(attrs))

    def _obj_to_xml(self):
        return ElementTree.tostring(self._obj_to_xml_ele())

    def _obj_to_xml_ele(self):
        element = ElementTree.Element('volume_type')
        attrs = {"name": self.name}

        if len(self.extra_specs.keys()) > 0:
            extra_specs = ElementTree.Element('extra_specs')
            for key in self.extra_specs.keys():
                spec = ElementTree.Element('extra_spec')
                spec.set('key', key)
                spec.text = self.extra_specs[key]
                extra_specs.append(spec)
            element.append(extra_specs)

        return self._set_xml_etree_element(element, attrs)


class VolumeTypeExtraSpecsUpdateRequest(AutoMarshallingModel):
    def __init__(self, extra_specs=None):
        super(VolumeTypeExtraSpecsUpdateRequest, self).__init__()
        self.extra_specs = extra_specs

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_dict(self):
        return dict(extra_specs=self._remove_empty_values(self.extra_specs))
