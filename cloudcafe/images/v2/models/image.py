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

import dateutil.parser
import json

from cafe.engine.models.base import (
    AutoMarshallingListModel, AutoMarshallingModel)
from cloudcafe.compute.common.equality_tools import EqualityTools


class Image(AutoMarshallingModel):
    """@summary: Image v2 model"""

    def __init__(self, checksum=None, container_format=None, created_at=None,
                 disk_format=None, file_=None, id_=None, image_type=None,
                 min_disk=None, min_ram=None, name=None, protected=None,
                 schema=None, self_=None, size=None, status=None, tags=None,
                 updated_at=None, visibility=None, additional_properties=None):
        # TODO: 'direct_url' and 'locations' should be added at a later date
        self.checksum = checksum
        self.container_format = container_format
        self.created_at = created_at
        self.disk_format = disk_format
        self.file_ = file_
        self.id_ = id_
        self.image_type = image_type
        self.min_disk = min_disk
        self.min_ram = min_ram
        self.name = name
        self.protected = protected
        self.schema = schema
        self.self_ = self_
        self.size = size
        self.status = status
        self.tags = tags
        self.updated_at = updated_at
        self.visibility = visibility
        self.additional_properties = additional_properties

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))
        return '[{0}]'.format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
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
        additional_properties = {}
        """When adding user specified or "additional" properties to an image,
        they are added to the root of the image object as opposed to a
        separate metadata dicionary.  The following loop needed to be
        implemented in order to catch all of these additional properties
        and filter out the core properties so that they were not repeated.
        """
        for key, value in json_dict.items():
            if key not in ['checksum', 'container_format', 'created_at',
                           'disk_format', 'file', 'id', 'image_type',
                           'min_disk', 'min_ram', 'name', 'protected',
                           'schema', 'self', 'size', 'status', 'tags',
                           'updated_at', 'visibility']:
                additional_properties.update({key: value})
        created_at = dateutil.parser.parse(json_dict.get('created_at'))
        updated_at = dateutil.parser.parse(json_dict.get('updated_at'))
        image = Image(checksum=json_dict.get('checksum'),
                      container_format=json_dict.get('container_format'),
                      created_at=created_at,
                      disk_format=json_dict.get('disk_format'),
                      file_=json_dict.get('file'), id_=json_dict.get('id'),
                      image_type=json_dict.get('image_type'),
                      min_disk=json_dict.get('min_disk'),
                      min_ram=json_dict.get('min_ram'),
                      name=json_dict.get('name'),
                      protected=json_dict.get('protected'),
                      schema=json_dict.get('schema'),
                      self_=json_dict.get('self'), size=json_dict.get('size'),
                      status=json_dict.get('status'),
                      tags=json_dict.get('tags'), updated_at=updated_at,
                      visibility=json_dict.get('visibility'),
                      additional_properties=additional_properties)
        return image

    def _obj_to_json(self):
        obj_dict = {}
        obj_dict['checksum'] = self.checksum
        obj_dict['container_format'] = self.container_format
        obj_dict['created_at'] = self.created_at
        obj_dict['disk_format'] = self.disk_format
        obj_dict['file'] = self.file_
        obj_dict['id'] = self.id_
        obj_dict['image_type'] = self.image_type
        obj_dict['min_disk'] = self.min_disk
        obj_dict['min_ram'] = self.min_ram
        obj_dict['name'] = self.name
        obj_dict['protected'] = self.protected
        obj_dict['schema'] = self.schema
        obj_dict['self_'] = self.self_
        obj_dict['size'] = self.size
        obj_dict['status'] = self.status
        obj_dict['tags'] = self.tags
        obj_dict['updated_at'] = self.updated_at
        obj_dict['visibility'] = self.visibility
        obj_dict = self._remove_empty_values(obj_dict)
        return json.dumps(obj_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')

    def _obj_to_xml(self):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')


class Images(AutoMarshallingListModel):
    """@summary: Images v2 model"""

    def __init__(self, images=None):
        super(Images, self).__init__()
        self.extend(images or [])

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('images'))

    @classmethod
    def _list_to_obj(cls, dict_list):
        images = Images()
        for image_dict in dict_list:
            images.append(Image._dict_to_obj(image_dict))
        return images


class ImageUpdate(AutoMarshallingModel):
    """@summary: ImageUpdate v2 model"""

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
                     'value': val})

        if self.replace_dict:
            for key, val in self.replace_dict.items():
                replace_list.append(
                    {'replace': '/{0}'.format(key),
                     'value': val})

        if self.remove_list:
            for prop in self.remove_list:
                replace_list.append(
                    {'remove': '/{0}'.format(prop)})
        return json.dumps(replace_list)


class Member(AutoMarshallingModel):
    """@summary: Member v2 model"""

    def __init__(self, created_at=None, image_id=None, member_id=None,
                 schema=None, status=None, updated_at=None):
        self.created_at = created_at
        self.image_id = image_id
        self.member_id = member_id
        self.schema = schema
        self.status = status
        self.updated_at = updated_at

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        member = Member(created_at=json_dict.get('created_at'),
                        image_id=json_dict.get('image_id'),
                        member_id=json_dict.get('member_id'),
                        schema=json_dict.get('schema'),
                        status=json_dict.get('status'),
                        updated_at=json_dict.get('updated_at'))
        return member

    def _obj_to_json(self):
        obj_dict = {}
        obj_dict['created_at'] = self.created_at
        obj_dict['image_id'] = self.image_id
        obj_dict['member'] = self.member_id
        obj_dict['schema'] = self.schema
        obj_dict['status'] = self.status
        obj_dict['updated_at'] = self.updated_at
        obj_dict = self._remove_empty_values(obj_dict)
        return json.dumps(obj_dict)


class Members(AutoMarshallingListModel):
    """@summary: Members v2 model"""

    def __init__(self, members=None):
        super(Members, self).__init__()
        self.extend(members or [])

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        dict_list = json_dict.get('members')
        return cls._list_to_obj(dict_list)

    @classmethod
    def _list_to_obj(cls, dict_list):
        members = Members()
        for member_dict in dict_list:
            member = Member._dict_to_obj(member_dict)
            members.append(member)
        return members
