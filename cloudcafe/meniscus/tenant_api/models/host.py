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


class UpdateHost(AutoMarshallingModel):
    def __init__(self, hostname=None, profile_id=None, ip_address_v4=None,
                 ip_address_v6=None):
        super(UpdateHost, self).__init__()

        self.hostname = hostname
        self.ip_address_v4 = ip_address_v4
        self.ip_address_v6 = ip_address_v6
        self.profile_id = profile_id

    def _obj_to_json(self):
        body = self._auto_to_dict()
        return json_to_str(body)


# Create requires all parameters, whereas update they are optional
class CreateHost(UpdateHost):

    def __init__(self, hostname, profile_id, ip_address_v4,
                 ip_address_v6):
        super(CreateHost, self).__init__(hostname, profile_id, ip_address_v4,
                                         ip_address_v6)


class Host(AutoMarshallingModel):
    ROOT_TAG = 'host'

    def __init__(self, ip_address_v6=None, profile=None, ip_address_v4=None,
                 hostname=None, id=None):
        super(Host, self).__init__()
        self.ip_address_v6 = ip_address_v6
        self.ip_address_v4 = ip_address_v4
        self.profile = profile
        self.hostname = hostname
        self.id = id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Host(**json_dict)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class AllHosts(AutoMarshallingModel):
    ROOT_TAG = 'hosts'

    def __init__(self):
        super(AllHosts, self).__init__()

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)

        converted = []
        json_producer_list = json_dict.get(cls.ROOT_TAG)

        for json_producer in json_producer_list:
            producer = Host._dict_to_obj(json_producer)
            converted.append(producer)

        return converted
