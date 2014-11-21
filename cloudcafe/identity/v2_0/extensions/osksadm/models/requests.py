'''
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from xml.etree import ElementTree as ET

import json
from cloudcafe.identity.common.models.base import (
    BaseIdentityModel)


class CreateUser(BaseIdentityModel):
    def __init__(
        self, enabled=None, email=None, name=None, password=None,
            tenant_id=None):
        super(CreateUser, self).__init__()
        self.enabled = enabled
        self.email = email
        self.name = name
        self.password = password
        self.tenant_id = tenant_id

    def _obj_to_xml_ele(self):
        ele = ET.Element("user")
        attrs = self._obj_to_dict()
        attrs["xmlns:OS-KSADM"] = (
            "http://docs.openstack.org/identity/api/ext/OS-KSADM/v1.0")
        attrs["enabled"] = self._bool_to_string(self.enabled)
        return self._set_xml_etree_element(ele, attrs)

    def _obj_to_dict(self):
        return self._remove_empty_values({
            "name": self.name, "enabled": self.enabled, "email": self.email,
            "OS-KSADM:password": self.password, "tenantId": self.tenant_id})

    def _obj_to_json(self):
        return json.dumps({"user": self._obj_to_dict()})


class UpdateUser(BaseIdentityModel):
    def __init__(
            self, enabled=None, email=None, name=None, id_=None,
            tenant_id=None):
        super(UpdateUser, self).__init__()
        self.enabled = enabled
        self.email = email
        self.name = name
        self.id_ = id_
        self.tenant_id = tenant_id

    def _obj_to_xml_ele(self):
        ele = ET.Element("user")
        attrs = self._obj_to_dict()
        attrs["enabled"] = self._bool_to_string(self.enabled)
        return self._set_xml_etree_element(ele, attrs)

    def _obj_to_dict(self):
        return self._remove_empty_values({
            "name": self.name, "enabled": self.enabled, "email": self.email,
            "id": self.id_, "tenantId": self.tenant_id})

    def _obj_to_json(self):
        return json.dumps({"user": self._obj_to_dict()})


class CreateTenant(BaseIdentityModel):
    def __init__(self, enabled=None, description=None, name=None):
        super(CreateTenant, self).__init__()
        self.enabled = enabled
        self.description = description
        self.name = name

    def _obj_to_xml_ele(self):
        ele = ET.Element("tenant")
        description = ET.Element("description")
        ele.append(description)
        description.text = self.description
        return self._set_xml_etree_element(ele, {
            "name": self.name, "enabled": self._bool_to_string(self.enabled)})

    def _obj_to_dict(self):
        return {
            "name": self.name, "description": self.description,
            "enabled": self.enabled}

    def _obj_to_json(self):
        return json.dumps({"tenant": self._obj_to_dict()})


class UpdateTenant(BaseIdentityModel):
    def __init__(self, enabled=None, description=None, name=None, id_=None):
        super(UpdateTenant, self).__init__()
        self.enabled = enabled
        self.description = description
        self.name = name
        self.id_ = id_

    def _obj_to_xml_ele(self):
        ele = ET.Element("tenant")
        description = ET.Element("description")
        ele.append(description)
        description.text = self.description
        return self._set_xml_etree_element(ele, {
            "name": self.name, "enabled": self._bool_to_string(self.enabled),
            "id": self.id_})

    def _obj_to_dict(self):
        return {
            "name": self.name, "description": self.description,
            "enabled": self.enabled, "id": self.id_}

    def _obj_to_json(self):
        return json.dumps({"tenant": self._obj_to_dict()})


class CreateRole(BaseIdentityModel):
    def __init__(self, id_=None, name=None, description=None):
        super(CreateRole, self).__init__()
        self.id_ = id_
        self.name = name
        self. description = description

    def _obj_to_xml_ele(self):
        ele = ET.Element("role")
        return self._set_xml_etree_element(ele, self._obj_to_dict())

    def _obj_to_dict(self):
        return {
            "name": self.name, "description": self.description, "id": self.id_}

    def _obj_to_json(self):
        return json.dumps({"role": self._obj_to_dict()})


class CreateService(BaseIdentityModel):
    def __init__(self, description=None, type_=None, name=None, id_=None):
        self.description = description
        self.type_ = type_
        self.name = name
        self.id_ = id_

    def _obj_to_dict(self):
        return {
            "name": self.name, "description": self.description, "id": self.id_,
            "type": self.type_}

    def _obj_to_xml_ele(self):
        ele = ET.Element("service")
        attrs = self._obj_to_dict()
        attrs["xmlns"] = (
            "http://docs.openstack.org/identity/api/ext/OS-KSADM/v1.0")
        return self._set_xml_etree_element(ele, attrs)

    def _obj_to_json(self):
        return json.dumps({"OS-KSADM:service": self._obj_to_dict()})
