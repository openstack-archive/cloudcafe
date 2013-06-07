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
from cafe.engine.models.base import AutoMarshallingListModel


class UpdateHost(AutoMarshallingModel):
    def __init__(self, hostname=None, profile_id=None, ip_address_v4=None,
                 ip_address_v6=None):
        super(UpdateHost, self).__init__()

        self.hostname = hostname
        self.ip_address_v4 = ip_address_v4
        self.ip_address_v6 = ip_address_v6
        self.profile_id = profile_id

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        body = {
            'hostname': self.hostname,
            'ip_address_v4': self.ip_address_v4,
            'ip_address_v6': self.ip_address_v6,
            'profile_id': self.profile_id
        }

        return {'host': self._remove_empty_values(body)}


# Create requires all parameters, whereas update they are optional
class CreateHost(UpdateHost):

    def __init__(self, hostname, profile_id, ip_address_v4,
                 ip_address_v6):
        super(CreateHost, self).__init__(hostname, profile_id, ip_address_v4,
                                         ip_address_v6)


class Host(AutoMarshallingModel):
    ROOT_TAG = 'host'

    def __init__(self, ip_address_v6=None, profile_id=None, ip_address_v4=None,
                 hostname=None, id=None):
        super(Host, self).__init__()
        self.ip_address_v6 = ip_address_v6
        self.ip_address_v4 = ip_address_v4
        self.profile_id = profile_id
        self.hostname = hostname
        self.id = id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        kwargs = {
            'id': json_dict.get('id'),
            'hostname': json_dict.get('hostname'),
            'profile_id': json_dict.get('profile_id'),
            'ip_address_v4': json_dict.get('ip_address_v4'),
            'ip_address_v6': json_dict.get('ip_address_v6')
        }
        return Host(**kwargs)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class HostList(AutoMarshallingListModel):
    ROOT_TAG = 'hosts'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)

        host_list = HostList()
        json_host_list = json_dict.get(cls.ROOT_TAG)

        for json_host in json_host_list:
            host = Host._dict_to_obj(json_host)
            host_list.append(host)

        return host_list
