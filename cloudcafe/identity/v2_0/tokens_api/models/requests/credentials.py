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
    BaseIdentityModel, V2_0Constants


class PasswordCredentials(BaseIdentityModel):

    ROOT_TAG = 'passwordCredentials'

    def __init__(self, username=None, password=None):

        super(PasswordCredentials, self).__init__()
        self.username = username
        self.password = password

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        if self.username is not None:
            ret['username'] = self.username
        if self.password is not None:
            ret['password'] = self.password
        return ret

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        element.set('xmlns', V2_0Constants.XML_NS)
        element.set('xmlns:xsi', V2_0Constants.XML_NS_XSI)
        return ElementTree.tostring(element)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.username is not None:
            element.set('username', self.username)
        if self.password is not None:
            element.set('password', self.password)
        return element

