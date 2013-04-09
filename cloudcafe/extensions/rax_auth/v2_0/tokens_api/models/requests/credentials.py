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
    BaseIdentityModel, V2_0Constants


class ApiKeyCredentials(BaseIdentityModel):

    ROOT_TAG = 'apiKeyCredentials'
    JSON_ROOT_TAG = 'RAX-KSKEY:{0}'.format(ROOT_TAG)

    def __init__(self, username=None, apiKey=None):
        super(ApiKeyCredentials, self).__init__()
        self.username = username
        self.apiKey = apiKey

    def _obj_to_json(self):
        ret = {self.JSON_ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        if self.username is not None:
            ret['username'] = self.username
        if self.apiKey is not None:
            ret['apiKey'] = self.apiKey
        return ret

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        element.set('xmlns', V2_0Constants.XML_NS_RAX_KSKEY)
        return ElementTree.tostring(element)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.username is not None:
            element.set('username', self.username)
        if self.apiKey is not None:
            element.set('apiKey', self.apiKey)
        return element