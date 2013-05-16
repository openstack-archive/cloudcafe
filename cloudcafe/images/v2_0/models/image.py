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

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.images.common.types import ImageStatus, ImageVisibility, \
    ImageContainerFormat, ImageDiskFormat


class Image(AutoMarshallingModel):
    """@Summary Openstack Images(Glance) API 2.0 model"""

    def __init__(self, id_=None, name=None, visibility=None,
                 status=None, protected=None, tags=None, checksum=None,
                 size=None, created_at=None, updated_at=None, file_=None,
                 self_=None, schema=None, container_format=None,
                 disk_format=None, min_disk=None, min_ram=None):
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
        return not self == other

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
        return str(values)

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
            del(json_dict[key])

        json_dict['status'] = getattr(ImageStatus, json_dict['status'].upper())
        json_dict['visibility'] = getattr(ImageVisibility,
                                          json_dict['visibility'].upper())
        json_dict['container_format'] = getattr(ImageContainerFormat,
                                                json_dict['container_format']
                                                .upper())
        json_dict['disk_format'] = getattr(ImageDiskFormat,
                                           json_dict['disk_format'].upper())

        return Image(**json_dict)

    def _obj_to_json(self):
        obj_dict = {}
        obj_dict['id'] = self.id_
        obj_dict['name'] = self.name
        obj_dict['visibility'] = self.visibility.lower()
        obj_dict['status'] = self.status.lower()
        obj_dict['protected'] = self.protected
        obj_dict['tags'] = self.tags
        obj_dict['checksum'] = self.checksum
        obj_dict['size'] = self.size
        obj_dict['created_at'] = self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        obj_dict['updated_at'] = self.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        obj_dict['file'] = self.file_
        obj_dict['self'] = self.self_
        obj_dict['schema'] = self.schema
        obj_dict['container_format'] = self.container_format.lower()
        obj_dict['disk_format'] = self.disk_format.lower()
        obj_dict['min_disk'] = self.min_disk
        obj_dict['min_ram'] = self.min_ram

        return json.dumps(obj_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError("Glance does not serve XML-formatted \
                                  resources.")

    def _obj_to_xml(self):
        raise NotImplementedError("Glance does not serve XML-formatted \
                                  resources.")
