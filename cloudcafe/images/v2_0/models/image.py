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

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.equality_tools import EqualityTools
from datetime import datetime
import json

class Image(AutoMarshallingModel):
    """@Summary Complete model of an image"""

    _log = None

    def __init__(self, id_=None, name=None, visibility=None, 
            status=None, protected=None, tags=None, checksum=None, 
            size=None, created_at=None, updated_at=None, file_=None, 
            self_=None, schema=None, properties=None, links=None):

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
        self.properties = properties
        self.links = links

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
                self.__dict__[prop] = 'None' or date_property.strftime('%Y-%m-%dT%H:%M:%S')
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'


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
    
    @classmethod
    def _dict_to_obj(cls, json_dict):
      """@summary: Processing dates in converting string to date objects"""

      for date_key in ['created_at','updated_at']:
        if json_dict[date_key]:
          json_dict[date_key] = datetime.strptime(json_dict[date_key], '%Y-%m-%dT%H:%M:%S')
      return Image(**json_dict)

    def _obj_to_json(self):
        pass

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError('Openstack Image API V2.0 doesn\'t serve XML documents.')

    def _obj_to_xml(self):
        raise NotImplementedError('Openstack Image API V2.0 doesn\'t serve XML documents.')

class ImageMin(Image):
    
    def __init__(self, name=None, container_format=None, disk_format=None, 
            status=None, min_disk=None, min_ram=None):
        self.name = name
        self.container = container_format
        self.disk_format = disk_format
        self.status = status
        self.min_disk = min_disk
        self.min_ram = min_ram
        
    def __repr__(self):
        values = []
        for prop in self.__dict__:
            if self.__dict__[prop]:
                values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

