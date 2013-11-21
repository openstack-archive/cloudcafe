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
from cafe.engine.models.base import AutoMarshallingListModel


class StorageObject(object):
    def __init__(self, name, bytes_, hash_, last_modified, content_type):
        self.name = name
        self.bytes_ = bytes_
        self.hash_ = hash_
        self.last_modified = last_modified
        self.content_type = content_type


class Container(object):
    def __init__(self, name=None, count=None, bytes_=None):
        self.name = name
        self.count = count
        self.bytes_ = bytes_


class ArchiveObject(object):
    def __init__(self, num_files_created=None, errors=None, body=None,
                 status=None):
        self.num_files_created = num_files_created
        self.errors = errors
        self.body = body
        self.status = status


class AccountContainersList(AutoMarshallingListModel):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        root = ElementTree.fromstring(serialized_str)
        data = []
        for child in root:
            account_container_dict = {}
            for sub_child in child:
                account_container_dict[sub_child.tag] = sub_child.text
            data.append(account_container_dict)
        return cls._list_to_obj(data)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._list_to_obj(data)

    @classmethod
    def _list_to_obj(cls, data):
        account_containers_list = AccountContainersList()
        for obj in data:
            container = Container(
                name=obj.get('name'),
                bytes_=obj.get('bytes'),
                count=obj.get('count'))
            account_containers_list.append(container)
        return account_containers_list


class ContainerObjectsList(AutoMarshallingListModel):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        root = ElementTree.fromstring(serialized_str)
        data = []
        for child in root:
            storage_object_dict = {}
            for sub_child in child:
                storage_object_dict[sub_child.tag] = sub_child.text
            data.append(storage_object_dict)
        return cls._list_to_obj(data)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._list_to_obj(data)

    @classmethod
    def _list_to_obj(cls, data):
        container_objects_list = ContainerObjectsList()
        for obj in data:
            storage_object = StorageObject(
                name=obj.get('name'),
                bytes_=obj.get('bytes'),
                hash_=obj.get('hash'),
                last_modified=obj.get('last_modified'),
                content_type=obj.get('content_type'))
            container_objects_list.append(storage_object)
        return container_objects_list

    @classmethod
    def _text_to_obj(cls, data):
        split_data = data.split('\n')
        data_list = [obj_name for obj_name in split_data if obj_name != '']

        container_objects_list = ContainerObjectsList()
        for obj_name in data_list:
            storage_object = StorageObject(
                name=obj_name,
                bytes_=None,
                hash_=None,
                last_modified=None,
                content_type=None)
            container_objects_list.append(storage_object)
        return container_objects_list

class CreateArchiveObject(AutoMarshallingListModel):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        root = ElementTree.fromstring(serialized_str)
        data = []
        for child in root:
            archive_object_dict = {}
            for sub_child in child:
                archive_object_dict[sub_child.tag] = sub_child.text
            data.append(archive_object_dict)
        return cls._list_to_obj(data)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._list_to_obj(data)

    @classmethod
    def _list_to_obj(cls, data):
        archive_obj = ArchiveObject(
            num_files_created=data.get("Number Files Created"),
            errors=data.get("Errors"),
            body=data.get("Response Body"),
            status=data.get("Response Status"))
        return archive_obj
