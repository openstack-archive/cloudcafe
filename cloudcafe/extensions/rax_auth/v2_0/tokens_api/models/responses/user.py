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
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.base import \
    BaseIdentityModel, BaseIdentityListModel
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.responses.role import \
    Roles, Role


class Users(BaseIdentityListModel):

    ROOT_TAG = 'users'

    def __init__(self, users=None):
        super(Users, self).__init__()
        self.extend(users)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        ret[cls.ROOT_TAG] = [User._dict_to_obj(user)
                             for user in ret.get(cls.ROOT_TAG)]
        return Users(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(User.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [User._xml_ele_to_obj(ele)
                                 for ele in xml_list]}
        return Users(**kwargs)


class User(BaseIdentityModel):

    ROOT_TAG = 'user'

    def __init__(self, id=None, enabled=None, username=None, updated=None,
                 created=None, email=None, domainId=None, defaultRegion=None,
                 password=None, roles=None, name=None, display_name=None):
        '''An object that represents an users response object.
        Keyword arguments:
        '''
        super(User, self).__init__()
        self.id = id
        self.enabled = enabled
        self.username = username
        self.updated = updated
        self.created = created
        self.email = email
        self.domainId = domainId
        self.defaultRegion = defaultRegion
        self.password = password
        self.roles = roles
        self.name = name
        self.display_name = display_name

    def get_role(self, id=None, name=None):
        '''Returns the role object if it matches all provided criteria'''
        for role in self.roles:
            if id and not name:
                if role.id == id:
                    return role
            if name and not id:
                if role.name == name:
                    return role
            if name and id:
                if (role.name == name) and (role.id == id):
                    return role

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        user = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return user

    @classmethod
    def _dict_to_obj(cls, json_dict):
        if 'RAX-AUTH:defaultRegion' in json_dict:
            json_dict['defaultRegion'] = \
                json_dict['RAX-AUTH:defaultRegion']
            del json_dict['RAX-AUTH:defaultRegion']
        if 'RAX-AUTH:domainId' in json_dict:
            json_dict['domainId'] = json_dict['RAX-AUTH:domainId']
            del json_dict['RAX-AUTH:domainId']
        if 'OS-KSADM:password' in json_dict:
            json_dict['password'] = json_dict['OS-KSADM:password']
            del json_dict['OS-KSADM:password']
        if 'display-name' in json_dict:
            json_dict['display_name'] = json_dict['display-name']
            del json_dict['display-name']
        if Roles.ROOT_TAG in json_dict:
            json_dict[Roles.ROOT_TAG] = Roles. \
                _list_to_obj(json_dict[Roles.ROOT_TAG])
        return User(**json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'username': xml_ele.get('username'),
                  'updated': xml_ele.get('updated'),
                  'created': xml_ele.get('created'),
                  'email': xml_ele.get('email'),
                  'domainId': xml_ele.get('domainId'),
                  'defaultRegion': xml_ele.get('defaultRegion'),
                  'password': xml_ele.get('password'),
                  'name': xml_ele.get('name'),
                  'display_name': xml_ele.get('display-name')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        if xml_ele.get('enabled') is not None:
            kwargs['enabled'] = json.loads(xml_ele.get('enabled').lower())
        roles = xml_ele.find(Roles.ROOT_TAG)
        if roles is not None:
            #if roles is not a list it is a single element with a list of
            #role elements
            roles = roles.findall(Role.ROOT_TAG)
        if roles is not None:
            kwargs['roles'] = Roles._xml_list_to_obj(roles)
        return User(**kwargs)
