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
from cloudcafe.identity.v2_0.tokens_api.models.base import \
    BaseIdentityModel, BaseIdentityListModel


class Roles(BaseIdentityListModel):
    def __init__(self, roles=None):
        """
        An object that represents a roles response object.
        Keyword arguments:
        """
        super(Roles, self).__init__()
        self.extend(roles or [])

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('roles'))

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {'roles': [Role(**role) for role in list_]}
        return Roles(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != 'roles':
            return None
        return cls._xml_list_to_obj(element.findall('role'))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {'roles': [Role._xml_ele_to_obj(role) for role in xml_list]}
        return Roles(**kwargs)


class Role(BaseIdentityModel):
    def __init__(self, id_=None, name=None, description=None):
        super(Role, self).__init__()
        self.id_ = id_
        self.name = name
        self.description = description

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return Role(**json_dict.get('role'))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != 'role':
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'name': xml_ele.get('name'),
                  'description': xml_ele.get('description')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        return Role(**kwargs)
