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

from xml.etree import ElementTree as ET

from cloudcafe.identity.common.models.base import BaseIdentityModel


class Auth(BaseIdentityModel):

    def __init__(
            self, username=None, password=None, tenant_name=None,
            tenant_id=None, token=None):
        super(Auth, self).__init__()

        self.token = token
        self.tenant_name = tenant_name
        self.tenant_id = tenant_id
        self.password_credentials = PasswordCredentials(username, password)

    def _obj_to_dict(self):
        attrs = {
            "tenantName": self.tenant_name,
            "tenantId": self.tenant_id,
            "passwordCredentials": self.password_credentials._obj_to_dict()}
        return {'auth': self._remove_empty_values(attrs)}

    def _obj_to_xml_ele(self):
        element = ET.Element('auth')
        element = self._set_xml_etree_element(
            element, {"tenantName": self.tenant_name,
                      "tenantId": self.tenant_id})
        element.append(self.password_credentials._obj_to_xml_ele())
        return element


class PasswordCredentials(BaseIdentityModel):

    def __init__(self, username=None, password=None):
        super(PasswordCredentials, self).__init__()

        self.username = username
        self.password = password

    def _obj_to_dict(self):
        attrs = {
            "username": self.username,
            "password": self.password}
        return self._remove_empty_values(attrs)

    def _obj_to_xml_ele(self):
        element = ET.Element('passwordCredentials')
        attrs = {
            "username": self.username,
            "password": self.password}
        return self._set_xml_etree_element(element, attrs)
