"""
Copyright 2014 Rackspace

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
from cafe.engine.models.base \
    import AutoMarshallingModel, AutoMarshallingListModel


class Extension(AutoMarshallingModel):

    def __init__(
            self, name=None, summary=None, alias=None, updated=None):
        super(Extension, self).__init__()
        self.name = name
        self.summary = summary
        self.alias = alias
        self.updated = updated

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):

        return Extension(
            name=json_dict.get('name'),
            summary=json_dict.get('summary'),
            alias=json_dict.get('alias'),
            updated=json_dict.get('updated'))


class Extensions(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('extensions'))

    @classmethod
    def _list_to_obj(cls, extension_dict_list):
        extension_list = Extensions()
        for extension_dict in extension_dict_list:
            extension = Extension._dict_to_obj(extension_dict)
            extension_list.append(extension)
        return extension_list
