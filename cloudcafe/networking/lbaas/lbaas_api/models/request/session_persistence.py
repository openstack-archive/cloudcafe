"""
Copyright 2014 Rackspace

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
from cloudcafe.networking.lbaas.common.constants import Constants


class SetSessionPersistence(AutoMarshallingModel):
    """ Set Session Persistence Request Model
    @summary: An object that represents the the request data of a
        Session Persistence.  This is used with Pools.

    json ex:
        {
            "sessionPersistence": {
                "type": "COOKIE",
                "cookie_name": "session_persistence_cookie",
            }
        }

    xml ex:
        <sessionPersistence xmlns=""
            type="COOKIE"
            cookie_name="session_persistence_cookie"
        </sessionPersistence>

    """

    ROOT_TAG = 'session_persistence'

    def __init__(self, type_=None, cookie_name=None):
        """
        @summary: Set Session Persistence Request Object Model
        @param type_: Type of session persistence to set.
        @type type_: String
        @param cookie_name: Name of cookie to set.
        @type cookie_name: String
        @return: Set Session Persistence Request Object
        @rtype: SetSessionPersistence
        """
        self.type_ = type_
        self.cookie_name = cookie_name

    def _obj_to_json(self):
        body = {
            'type': self.type_,
            'cookie_name': self.cookie_name
        }
        body = self._remove_empty_values(body)
        main_body = {self.ROOT_TAG: body}
        return json.dumps(main_body)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        if self.type_ is not None:
            element.set('type', self.type_)
        if self.cookie_name is not None:
            element.set('cookie_name', self.cookie_name)
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml
