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


class Roles(BaseIdentityListModel):

    ROOT_TAG = 'roles'

    def __init__(self, roles=None):
        '''
        An object that represents an users response object.
        Keyword arguments:
        '''
        super(Roles, self).__init__()
        self.extend(roles)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {cls.ROOT_TAG: [Role(**role) for role in list_]}
        return Roles(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Role.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [Role._xml_ele_to_obj(role)
                                 for role in xml_list]}
        return Roles(**kwargs)


class Role(BaseIdentityModel):

    ROOT_TAG = 'role'

    def __init__(self, id=None, name=None, description=None, serviceId=None,
                 tenantId=None, propagate = None, weight = None):
        super(Role, self).__init__()
        self.id = id
        self.name = name
        self.description = description
        self.serviceId = serviceId
        self.tenantId = tenantId
        self.weight = weight
        self.propagate = propagate

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        json_dict['role']['propagate'] = json_dict['role'].pop('RAX-AUTH:propagate')
        json_dict['role']['weight'] = json_dict['role'].pop('RAX-AUTH:Weight')
        return Role(**json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'name': xml_ele.get('name'),
                  'description': xml_ele.get('description'),
                  'serviceId': xml_ele.get('serviceId'),
                  'tenantId': xml_ele.get('tenantId')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        return Role(**kwargs)
