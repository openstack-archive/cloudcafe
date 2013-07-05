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
from cloudcafe.identity.v2_0.common.models.base import \
    BaseIdentityModel, BaseIdentityListModel


class Roles(BaseIdentityListModel):
    def __init__(self, roles=None):
        """
        Models a roles list returned by keystone
        """
        super(Roles, self).__init__()
        self.extend(roles or [])

    @classmethod
    def _list_to_obj(cls, role_dict_list):
        roles = Roles()
        for role_dict in role_dict_list:
            role = Role._dict_to_obj(role_dict)
            roles.append(role)
        return roles

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('roles'))


class Role(BaseIdentityModel):
    def __init__(self, id_=None, name=None):
        """
        Models a role returned by keystone
        """
        super(Role, self).__init__()
        self.id_ = id_
        self.name = name

    @classmethod
    def _dict_to_obj(cls, json_dict):
        role = Role(id_=json_dict.get('id'),
                    name=json_dict.get('name'))
        return role

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('role'))

    def _obj_to_json(self):
        json_dict = {"role": {"id": self.id_, "name": self.name}}
        return json.dumps(json_dict)
