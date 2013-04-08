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

from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.base \
    import BaseIdentityModel
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.constants \
    import V2_0Constants
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.requests.credentials \
    import ApiKeyCredentials


class Auth(BaseIdentityModel):

    ROOT_TAG = 'auth'

    def __init__(self, apiKeyCredentials=None,
                 tenantId=None, token=None):
        self.apiKeyCredentials = apiKeyCredentials
        self.token = token
        self.tenantId = tenantId

    def _obj_to_json(self):
        ret = {}

        ret[ApiKeyCredentials.JSON_ROOT_TAG] = \
            self.apiKeyCredentials._obj_to_dict()
        if self.token is not None:
            ret[Token.ROOT_TAG] = self.token._obj_to_dict()
        if self.tenantId is not None:
            ret['tenantId'] = self.tenantId
        ret = {self.ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        ele = self._obj_to_xml_ele()
        if self.apiKeyCredentials is not None:
            ele.find(ApiKeyCredentials.ROOT_TAG).set(
                'xmlns',
                V2_0Constants.XML_NS_RAX_KSKEY)
        else:
            ele.set('xmlns:xsi', V2_0Constants.XML_NS_XSI)
            ele.set('xmlns', V2_0Constants.XML_NS)
        return ElementTree.tostring(ele)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.apiKeyCredentials is not None:
            element.append(self.apiKeyCredentials._obj_to_xml_ele())
        if self.token is not None:
            element.append(self.token._obj_to_xml_ele())
        if self.tenantId is not None:
            element.set('tenantId', self.tenantId)
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
