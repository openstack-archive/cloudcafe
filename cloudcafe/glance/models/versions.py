"""
Copyright 2015 Rackspace

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

from cafe.engine.models.base import (
    AutoMarshallingModel, AutoMarshallingListModel)
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.images.common.models.links import Links


class Version(AutoMarshallingModel):
    """@summary: Version model"""

    def __init__(self, id_=None, links=None, status=None):
        super(Version, self).__init__()
        self.id_ = id_
        self.links = links
        self.status = status

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        links = None
        if 'links' in json_dict:
            links = Links._list_to_obj(json_dict.get('links'))
        version = Version(id_=json_dict.get('id'), links=links,
                          status=json_dict.get('status'))
        return version

    def _obj_to_json(self):
        obj_dict = {}
        obj_dict['id'] = self.id_
        obj_dict['links'] = self.links
        obj_dict['status'] = self.status
        return json.dumps(obj_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError(
            'Images does not serve XML-formatted resources')

    def _obj_to_xml(self):
        raise NotImplementedError(
            'Images does not serve XML-formatted resources')


class Versions(AutoMarshallingListModel):
    """@summary: Versions model"""

    def __init__(self, versions=None):
        self.extend(versions or [])

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('versions'))

    @classmethod
    def _list_to_obj(cls, dict_list):
        versions = Versions()
        for version_dict in dict_list:
            versions.append(Version._dict_to_obj(version_dict))
        return versions
