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
from json import dumps as dict_to_str, loads as str_to_dict
from cafe.engine.models.base import AutoMarshallingModel


class SecretRef(AutoMarshallingModel):

    def __init__(self, name, ref):
        super(SecretRef, self).__init__()
        self.name = name
        self.ref = ref

    def _obj_to_dict(self):
        return {'name': self.name, 'secret_ref': self.ref}

    def _obj_to_json(self):
        return dict_to_str(self._obj_to_dict())

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        args = {
            'name': json_dict.get('name'),
            'ref': json_dict.get('secret_ref')
        }
        return SecretRef(**args)


class Container(AutoMarshallingModel):

    def __init__(self, name, container_type=None, secret_refs=None,
                 status=None, updated=None, created=None, container_ref=None):
        super(Container, self).__init__()
        self.name = name
        self.status = status
        self.created = created
        self.updated = updated
        self.container_type = container_type
        self.secret_refs = secret_refs
        self.container_ref = container_ref

    def _obj_to_dict(self):
        return {
            'name': self.name,
            'type': self.container_type,
            'secret_refs': [ref._obj_to_dict() for ref in self.secret_refs]
        }

    def _obj_to_json(self):
        return dict_to_str(self._obj_to_dict())

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        refs = [SecretRef._dict_to_obj(ref) for ref in
                json_dict.get('secret_refs')]

        args = {
            'name': json_dict.get('name'),
            'container_type': json_dict.get('container_type'),
            'secret_refs': refs,
            'status': json_dict.get('status'),
            'updated': json_dict.get('updated'),
            'created': json_dict.get('created'),
            'container_ref': json_dict.get('container_ref')
        }
        return Container(**args)


class ContainerRef(AutoMarshallingModel):

    def __init__(self, reference):
        super(ContainerRef, self).__init__()
        self.reference = reference

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return ContainerRef(reference=json_dict.get('container_ref'))


class ContainerGroup(AutoMarshallingModel):

    def __init__(self, containers, next_list=None, previous_list=None):
        super(ContainerGroup, self).__init__()
        self.containers = containers
        self.next = next_list
        self.previous = previous_list

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        containers = [Container._dict_to_obj(item)
                      for item in json_dict.get('containers')]
        args = {
            'containers': containers,
            'next_list': json_dict.get('next'),
            'previous_list': json_dict.get('previous')
        }

        return ContainerGroup(**args)
