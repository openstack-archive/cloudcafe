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
from datetime import datetime

from cafe.engine.models.base import AutoMarshallingModel, \
    AutoMarshallingListModel
from cloudcafe.compute.common.equality_tools import EqualityTools


class Image(AutoMarshallingModel):
    """@Summary Openstack Images(Glance) API 2.0 model"""

    def __init__(self, id_=None, name=None, visibility=None,
                 status=None, protected=None, tags=None, checksum=None,
                 size=None, created_at=None, updated_at=None, file_=None,
                 self_=None, schema=None, container_format=None,
                 disk_format=None, min_disk=None, min_ram=None, kernel_id=None,
                 ramdisk_id=None):
        """@Summary Construct an Image model
           @param visibility
           @type ImageVisibility
           @param status
           @type ImageStatus
           @param container_format
           @type ImageContainerFormat
           @param disk_format
           @type ImageDiskFormat
        """

        self.id_ = id_
        self.name = name
        self.visibility = visibility
        self.status = status
        self.protected = protected
        self.tags = tags
        self.checksum = checksum
        self.size = size
        self.created_at = created_at
        self.updated_at = updated_at
        self.file_ = file_
        self.self_ = self_
        self.schema = schema
        self.container_format = container_format
        self.disk_format = disk_format
        self.min_disk = min_disk
        self.min_ram = min_ram
        self.kernel_id = kernel_id
        self.ramdisk_id = ramdisk_id

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Image object to compare with
        @type other: Image
        @return: True if Image objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Image object to compare with
        @type other: Image
        @return: True if Image objects are not equal, False otherwise
        @rtype: bool
        """
        return not self.__eq__(other)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            if prop in ['created_at', 'updated_at']:
                date_property = self.__dict__[prop]
                values.append("{0}: {1}".format(
                    prop,
                    date_property.strftime('%Y-%m-%dT%H:%M:%SZ')))
            else:
                values.append("{0}: {1}".format(prop, self.__dict__[prop]))
        return '[{0}]'.format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        serialized_str.replace('false', 'False')
        serialized_str.replace('true', 'True')
        json_dict = json.loads(serialized_str)

        if 'images' in json_dict.keys():
            images = []
            for image_dict in json_dict['images']:
                images.append(cls._dict_to_obj(image_dict))
            return images
        else:
            return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        """@summary: Process the json properties appropriately"""

        for date_key in ['created_at', 'updated_at']:
            if json_dict[date_key]:
                json_dict[date_key] = datetime.strptime(json_dict[date_key],
                                                        '%Y-%m-%dT%H:%M:%SZ')
        for key in ['id', 'self', 'file']:
            json_dict['{0}_'.format(key)] = json_dict[key]
            del (json_dict[key])

        return Image(**json_dict)

    def _obj_to_json(self):
        obj_dict = {}
        if self.created_at:
            obj_dict['created_at'] = \
                self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        if self.updated_at:
            obj_dict['updated_at'] = \
                self.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        if self.self_:
            obj_dict['self'] = self.self_
        if self.file_:
            obj_dict['file'] = self.file_

        obj_dict['id'] = self.id_
        obj_dict['name'] = self.name
        obj_dict['visibility'] = self.visibility
        obj_dict['status'] = self.status
        obj_dict['protected'] = self.protected
        obj_dict['tags'] = self.tags
        obj_dict['checksum'] = self.checksum
        obj_dict['size'] = self.size
        obj_dict['container_format'] = self.container_format
        obj_dict['disk_format'] = self.disk_format
        obj_dict['min_disk'] = self.min_disk
        obj_dict['min_ram'] = self.min_ram

        obj_dict = self._remove_empty_values(obj_dict)

        return json.dumps(obj_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError("Glance does not serve XML-formatted \
                                  resources.")

    def _obj_to_xml(self):
        raise NotImplementedError("Glance does not serve XML-formatted \
                                  resources.")


class ImagePatch(AutoMarshallingModel):
    """
        JSON model for updating an image.
        http://docs.openstack.org/api/ \
        openstack-image-service/2.0/content/update-an-image.html
    """

    def __init__(self, add=None, replace=None, remove=None):
        self.add_dict = add
        self.replace_dict = replace
        self.remove_list = remove

    def _obj_to_json(self):
        replace_list = []
        if self.add_dict:
            for key, val in self.add_dict.items():
                replace_list.append(
                    {'add': '/{0}'.format(key),
                     'value': val}
                )

        if self.replace_dict:
            for key, val in self.replace_dict.items():
                replace_list.append(
                    {'replace': '/{0}'.format(key),
                     'value': val}
                )

        if self.remove_list:
            for prop in self.remove_list:
                replace_list.append(
                    {'remove': '/{0}'.format(prop)})

        return json.dumps(replace_list)


class Member(AutoMarshallingModel):
    """Image member model"""

    def __init__(self, member_id=None, status=None, created_at=None,
                 updated_at=None, image_id=None):
        self.member_id = member_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.image_id = image_id

    def _obj_to_json(self):
        json_dict = {"member": {"status": self.status,
                                "created_at": self.created_at,
                                "updated_at": self.updated_at,
                                "image_id": self.image_id}}

        return json.dumps(json_dict)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)

        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        del json_dict['schema']
        json_dict['created_at'] = datetime.strptime(json_dict['created_at'],
                                                    '%Y-%m-%dT%H:%M:%SZ')
        json_dict['updated_at'] = datetime.strptime(json_dict['updated_at'],
                                                    '%Y-%m-%dT%H:%M:%SZ')

        return Member(**json_dict)


class Members(AutoMarshallingListModel):
    """ An object that represents a members response object."""

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('members'))

    @classmethod
    def _list_to_obj(cls, dict_list):
        return [Member._dict_to_obj(member_dict) for member_dict in dict_list]
