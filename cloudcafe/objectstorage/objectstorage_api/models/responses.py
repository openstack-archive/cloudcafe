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


class AccountContainersList(AutoMarshallingModel):
    pass

    class _Container(object):
        def __init__(self, name=None, count=None, bytes=None):
            self.name = None
            self.count = None
            self.bytes = None

    def __init__(self):
        '''This is a deserializing object only'''
        pass

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        ret = []
        root = ElementTree.fromstring(serialized_str)
        setattr(cls, 'name', root.attrib['name'])
        for child in root:
            container_dict = {}
            for sub_child in child:
                container_dict[sub_child.tag] = sub_child.text
            ret.append(cls._StorageObject(**container_dict))
        return ret

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        data = json.loads(serialized_str)
        for container in data:
            ret.append(
                cls._Container(
                    name=container.get('name'),
                    bytes=container.get('bytes'),
                    count=container.get('count')))
        return ret


class ContainerObjectsList(AutoMarshallingModel):
    #TODO: make this not use *args and **kwargs
    class _StorageObject(dict):
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', None)
            self.bytes = kwargs.get('bytes', None)
            self.hash = kwargs.get('hash', None)
            self.last_modified = kwargs.get('last_modified', None)
            self.content_type = kwargs.get('content_type', None)

    def __init__(self):
        '''This is a deserializing object only'''
        pass

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        ret = []
        root = ElementTree.fromstring(serialized_str)
        setattr(cls, 'name', root.attrib['name'])
        for child in root:
            storage_object_dict = {}
            for sub_child in child:
                storage_object_dict[sub_child.tag] = sub_child.text
            ret.append(cls._StorageObject(**storage_object_dict))
        return ret

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        data = json.loads(serialized_str)
        for storage_object in data:
            storage_obj = cls._StorageObject(
                name=storage_object.get('name'),
                bytes=storage_object.get('bytes'),
                hash=storage_object.get('hash'))
            ret.append(
                storage_obj,
                last_modified=storage_object.get('last_modified'),
                content_type=storage_object.get('content_type'))
        return ret
