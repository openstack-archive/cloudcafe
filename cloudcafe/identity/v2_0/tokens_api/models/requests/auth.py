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

from cloudcafe.identity.v2_0.tokens_api.models.base import BaseIdentityModel
from cloudcafe.identity.v2_0.tokens_api.models.requests.credentials import \
    PasswordCredentials


class Auth(BaseIdentityModel):

    ROOT_TAG = 'auth'

    def __init__(self, credentials=None, tenant_name=None, token=None):
        self.passwordCredentials = credentials
        self.token = token
        self.tenant_name = tenant_name

    def _obj_to_json(self):
        ret = {}
        if self.passwordCredentials is not None:
            ret[PasswordCredentials.ROOT_TAG] = \
                self.passwordCredentials._obj_to_dict()
        if self.token is not None:
            ret[Token.ROOT_TAG] = self.token._obj_to_dict()
        if self.tenant_name is not None:
            ret['tenantName'] = self.tenant_name
        ret = {self.ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        ele = self._obj_to_xml_ele()
        #ele.set('xmlns:xsi', V2_0Constants.XML_NS_XSI)
        #ele.set('xmlns', V2_0Constants.XML_NS)
        return ElementTree.tostring(ele)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.passwordCredentials is not None:
            element.append(self.passwordCredentials._obj_to_xml_ele())
        if self.token is not None:
            element.append(self.token._obj_to_xml_ele())
        if self.tenant_name is not None:
            element.set('tenantName', self.tenant_name)
        return element


class Token(BaseIdentityModel):

    ROOT_TAG = 'token'

    def __init__(self, id=None):
        super(Token, self).__init__()
        self.id = id

    def _obj_to_dict(self):
        ret = {}
        if self.id is not None:
            ret['id'] = self.id
        return ret

    def _obj_to_xml(self):
        return ElementTree.tostring(self._obj_to_xml_ele())

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.id is not None:
            element.set('id', self.id)
        return element
