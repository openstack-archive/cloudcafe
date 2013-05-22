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


class Endpoints(BaseIdentityListModel):
    def __init__(self, endpoints=None):
        super(Endpoints, self).__init__()
        self.extend(endpoints)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('endpoints'))

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {'endpoints': [Endpoint(**endpoint) for endpoint in list_]}
        return Endpoints(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != 'endpoints':
            return None
        return cls._xml_list_to_obj(element.findall('endpoint'))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {'endpoints': [Endpoint._xml_ele_to_obj(endpoint)
                                for endpoint in xml_list]}
        return Endpoints(**kwargs)


class Endpoint(BaseIdentityModel):
    def __init__(self, tenantId=None, region=None, id_=None, publicURL=None,
                 name=None, adminURL=None, type_=None, internalURL=None,
                 versionId=None, versionInfo=None, versionList=None):
        super(Endpoint, self).__init__()
        self.tenantId = tenantId
        self.region = region
        self.id_ = id_
        self.publicURL = publicURL
        self.name = name
        self.adminURL = adminURL
        self.type_ = type_
        self.internalURL = internalURL
        self.versionId = versionId
        self.versionInfo = versionInfo
        self.versionList = versionList
        #currently json has version attributes as part of the Endpoint
        #xml has it as a separate element.

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('endpoint'))

    @classmethod
    def _dict_to_obj(cls, dic):
        if 'version' in dic:
            dic['version'] = Version(**dic['version'])
        return Endpoint(**dic)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != 'endpoint':
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'tenantId': xml_ele.get('tenantId'),
                  'region': xml_ele.get('region'),
                  'publicURL': xml_ele.get('publicURL'),
                  'name': xml_ele.get('name'),
                  'adminURL': xml_ele.get('adminURL'),
                  'type': xml_ele.get('type'),
                  'internalURL': xml_ele.get('internalURL')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        version = xml_ele.find('version')
        if version is not None:
            kwargs['versionId'] = version.get('id')
            kwargs['versionInfo'] = version.get('info')
            kwargs['versionList'] = version.get('list')
        return Endpoint(**kwargs)


# noinspection PyMissingConstructor
class Version(BaseIdentityModel):
    def __init__(self, id_=None, info=None, list_=None):
        self.id_ = id_
        self.info = info
        self.list_ = list_