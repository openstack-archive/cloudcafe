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
from cloudcafe.meniscus.tenant_api.models.producer import Producer
from cloudcafe.meniscus.tenant_api.models.profile import Profile
from cloudcafe.meniscus.tenant_api.models.host import Host


class CreateTenant(AutoMarshallingModel):
    def __init__(self, tenant_id):
        super(CreateTenant, self).__init__()
        self.tenant_id = tenant_id

    def _obj_to_json(self):
        body = self._auto_to_dict()
        return json_to_str(body)


class Tenant(AutoMarshallingModel):
    ROOT_TAG = 'tenant'

    def __init__(self, tenant_id=None, event_producers=None, hosts=None,
                 profiles=None, token=None):
        """An object that represents an tenant's response object."""
        super(Tenant, self).__init__()
        self.tenant_id = tenant_id
        self.event_producers = event_producers
        self.hosts = hosts
        self.profiles = profiles
        self.token = token

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @param serialized_str:
        @return:
        """
        result = None
        json_dict = str_to_json(serialized_str)
        if json_dict is not None:
                result = [cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))]
        return result

    @classmethod
    def _dict_to_obj(cls, dic):
        event_producers = cls._convert_dict_of_types(
            Producer, dic.get('event_producers'))
        hosts = cls._convert_dict_of_types(Host, dic.get('hosts'))
        profiles = cls._convert_dict_of_types(Profile, dic.get('profiles'))
        token = TenantToken._dict_to_obj(dic.get('token'))

        kwargs = {
            'tenant_id': str(dic.get('tenant_id')),
            'event_producers': event_producers,
            'hosts': hosts,
            'profiles': profiles,
            'token': token
        }
        return Tenant(**kwargs)

    @classmethod
    def _convert_dict_of_types(cls, c_type, dict):
        result = None
        if len(dict) > 0:
            result = []
            for item in dict:
                result.append(c_type._dict_to_obj(item))
        return result


class TenantToken(AutoMarshallingModel):

    def __init__(self, valid, previous, last_changed):
        super(TenantToken, self).__init__()
        self.valid = valid
        self.previous = previous
        self.last_changed = last_changed

    def _obj_to_json(self):
        return json_to_str(self._auto_to_dict())

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return TenantToken(**json_dict)
