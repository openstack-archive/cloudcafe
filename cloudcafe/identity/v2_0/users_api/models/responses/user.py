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

from cloudcafe.identity.v2_0.common.models.base import \
    BaseIdentityModel, BaseIdentityListModel
from cloudcafe.identity.v2_0.tenants_api.models.responses.tenant import Tenants


class Users(BaseIdentityListModel):
    def __init__(self, users=None):
        """
        Models a users list returned by keystone
        """
        super(Users, self).__init__()
        self.extend(users or [])

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('users'))

    @classmethod
    def _list_to_obj(cls, users_dict_list):
        users = Users()
        for user_dict in users_dict_list:
            user = User._dict_to_obj(user_dict)
            users.append(user)

        return users

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != 'users':
            return None
        return cls._xml_list_to_obj(element.findall('user'))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {'users': [User._xml_ele_to_obj(ele) for ele in xml_list]}
        return Tenants(**kwargs)


class User(BaseIdentityModel):
    def __init__(self, name=None, id_=None, tenantId=None,
                 enabled=None, email=None):
        """
        Models a user returned by keystone
        """
        super(User, self).__init__()
        self.name = name
        self.id_ = id_
        self.tenantId = tenantId
        self.enabled = enabled
        self.email = email

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, user_dict):
        user = User(name=user_dict.get('name'),
                    id_=user_dict.get('id'),
                    tenantId=user_dict.get('tenantId'),
                    enabled=user_dict.get('enabled'),
                    email=user_dict.get('email'))

        return user

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != 'user':
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'enabled': xml_ele.get('enabled'),
                  'email': xml_ele.get('email'),
                  'username': xml_ele.get('username'),
                  'id_': xml_ele.get('id')}

        return User(**kwargs)
