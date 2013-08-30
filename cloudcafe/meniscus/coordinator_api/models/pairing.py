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
from json import dumps as json_to_str, loads as str_to_json
from cafe.engine.models.base import AutoMarshallingModel


class WorkerRegistration(AutoMarshallingModel):

    def __init__(self, hostname=None, ip_v4=None, ip_v6=None,
                 personality=None, status=None, system_info=None):
        super(WorkerRegistration, self).__init__()

        self.hostname = hostname
        self.ip_address_v4 = ip_v4
        self.ip_address_v6 = ip_v6
        self.personality = personality
        self.status = status
        self.system_info = system_info

    def _obj_to_json(self):
        return json_to_str({'worker_registration': self._obj_to_dict()})

    def _obj_to_dict(self):
        return {
            'hostname': self.hostname,
            'ip_address_v4': self.ip_address_v4,
            'ip_address_v6': self.ip_address_v6,
            'personality': self.personality,
            'status': self.status,
            'system_info': self.system_info._obj_to_dict()
        }


class WorkerPairing(AutoMarshallingModel):
    ROOT_TAG = 'worker_identity'

    def __init__(self, personality_module, worker_id, worker_token):
        super(WorkerPairing, self).__init__()

        self.personality_module = personality_module
        self.worker_id = worker_id
        self.worker_token = worker_token

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return WorkerPairing(**json_dict)
