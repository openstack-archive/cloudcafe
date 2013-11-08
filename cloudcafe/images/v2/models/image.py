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

from cafe.engine.models.base import \
    AutoMarshallingListModel, AutoMarshallingModel
from cloudcafe.compute.common.equality_tools import EqualityTools


class Image(AutoMarshallingModel):
    """@summary: Image v2 model"""

    def __init__(self, checksum=None, container_format=None, created_at=None,
                 direct_url=None, disk_format=None, file=None, id=None,
                 min_disk=None, min_ram=None, name=None, protected=None,
                 schema=None, self_=None, size=None, status=None, tags=None,
                 updated_at=None, visibility=None, additional_properties=None):

        self.checksum = checksum
        self.container_format = container_format
        self.created_at = created_at
        self.direct_url = direct_url
        self.disk_format = disk_format
        self.file = file
        self.id = id
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
        for key, value in json_dict.items():
            if key not in ['checksum', 'container_format', 'created_at',
                           'direct_url', 'disk_format', 'file', 'id',
                           'min_disk', 'min_ram', 'name', 'protected',
                           'schema', 'self', 'size', 'status', 'tags',
                           'updated_at', 'visibility']:
                additional_properties.update({key: value})

        image = Image(checksum=json_dict.get('checksum'),
                      container_format=json_dict.get('container_format'),
                      created_at=json_dict.get('created_at'),
                      direct_url=json_dict.get('direct_url'),
                      disk_format=json_dict.get('disk_format'),
                      file=json_dict.get('file'), id=json_dict.get('id'),
                      min_disk=json_dict.get('min_disk'),
                      min_ram=json_dict.get('min_ram'),
                      name=json_dict.get('name'),
                      protected=json_dict.get('protected'),
                      schema=json_dict.get('schema'),
                      self_=json_dict.get('self'), size=json_dict.get('size'),
                      status=json_dict.get('status'),
                      tags=json_dict.get('tags'),
                      updated_at=json_dict.get('updated_at'),
                      visibility=json_dict.get('visibility'),
                      additional_properties=additional_properties)

        return image

    def _obj_to_json(self):

        obj_dict = {}

        obj_dict['checksum'] = self.created_at
        obj_dict['container_format'] = self.container_format
        obj_dict['created_at'] = self.created_at
        obj_dict['direct_url'] = self.direct_url
        obj_dict['disk_format'] = self.disk_format
        obj_dict['file'] = self.file
        obj_dict['id'] = self.id
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

        raise NotImplementedError("Glance does not serve XML-formatted \
                                  resources.")

    def _obj_to_xml(self):

        raise NotImplementedError("Glance does not serve XML-formatted \
                                  resources.")


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


class ImagePatch(AutoMarshallingModel):
    """@summary: ImagePatch v2 model"""

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
    """@summary: Member v2 model"""

    def __init__(self, member_id=None, status=None, created_at=None,
                  updated_at=None, image_id=None):

        self.member_id = member_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.image_id = image_id

    def _obj_to_json(self):

        json_dict = {"member": self.member_id, "status": self.status,
                     "created_at": self.created_at,
                     "updated_at": self.updated_at, "image_id": self.image_id}

        return json.dumps(json_dict)

    @classmethod
    def _json_to_obj(cls, serialized_str):

        json_dict = json.loads(serialized_str)

        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):

        del json_dict['schema']

        json_dict['created_at'] = dateutil.parser.parse(
            json_dict['created_at'])

        json_dict['updated_at'] = dateutil.parser.parse(
            json_dict['updated_at'])

        return Member(**json_dict)


class Members(AutoMarshallingListModel):
    """@summary: Members v2 model"""

    @classmethod
    def _json_to_obj(cls, serialized_str):

        json_dict = json.loads(serialized_str)

        return cls._list_to_obj(json_dict.get('members'))

    @classmethod
    def _list_to_obj(cls, dict_list):

        return [Member._dict_to_obj(member_dict) for member_dict in dict_list]
