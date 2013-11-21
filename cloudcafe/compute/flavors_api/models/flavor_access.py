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
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cafe.engine.models.base import AutoMarshallingListModel
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.equality_tools import EqualityTools


class FlavorAccess(AutoMarshallingModel):

    def __init__(self, flavor_id=None, tenant_id=None):
            super(FlavorAccess, self).__init__()
            self.flavor_id = flavor_id
            self.tenant_id = tenant_id

    @classmethod
    def _json_to_obj(cls, json_dict):
        access = FlavorAccess(flavor_id=json_dict.get('flavor_id'),
                              tenant_id=json_dict.get('tenant_id'))
        return access

    @classmethod
    def _xml_to_obj(cls, element):
        access_dict = element.attrib
        access = FlavorAccess(flavor_id=access_dict.get('flavor_id'),
                              tenant_id=access_dict.get('tenant_id'))
        return access

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        return not self == other


class FlavorAccessList(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('flavor_access'))

    @classmethod
    def _list_to_obj(cls, access_dict_list):
        access_list = FlavorAccessList()
        for flavor_dict in access_dict_list:
            access = FlavorAccess._json_to_obj(flavor_dict)
            access_list.append(access)
        return access_list

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        return cls._xml_list_to_obj(element.findall('access'))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        flavors = FlavorAccessList()
        for ele in xml_list:
            flavors.append(FlavorAccess._xml_to_obj(ele))
        return flavors


class AddTenantFlavorAccess(AutoMarshallingModel):

    def __init__(self, tenant=None):
        super(AddTenantFlavorAccess, self).__init__()
        self.tenant = tenant

    def _obj_to_json(self):
        ret = {'addTenantAccess': {'tenant': self.tenant}}
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('addTenantAccess')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('tenant', self.tenant)
        xml += ET.tostring(element)
        return xml


class RemoveTenantFlavorAccess(AutoMarshallingModel):

    def __init__(self, tenant=None):
        super(RemoveTenantFlavorAccess, self).__init__()
        self.tenant = tenant

    def _obj_to_json(self):
        ret = {'removeTenantAccess': {'tenant': self.tenant}}
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('removeTenantAccess')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('tenant', self.tenant)
        xml += ET.tostring(element)
        return xml
