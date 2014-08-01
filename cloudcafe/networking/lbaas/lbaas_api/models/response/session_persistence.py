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

SessionPersistence Response Model

@note: Session persistence is a feature of the load balancing service that
    forces multiple requests, of the same protocol, from clients to be
    directed to the same node.  This is common with many web applications that
    do not inherently share application state between back-end servers.

    Two session persistence modes are available, as described:

    HTTP_COOKIE: A session persistence mechanism that inserts an HTTP cookie
        and is used to determine the destination back-end node.  This is
        supported for HTTP load balancing only.

    SOURCE_IP: A session persistence mechanism that will keep track of the
        source IP address that is mapped and is able to determine the
        destination back-end node.  This is supported for HTTPS pass-through
        and non-HTTP load balancing only.
"""

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.networking.lbaas.common.constants import Constants


class SessionPersistence(AutoMarshallingModel):
    """ Session Persistence Response Model
    @summary: An object that represents the the response data of a
        Session Persistence.  This is used with Pools.

    json ex:
        {
            "session_persistence": {
                "type": "COOKIE",
                "cookie_name": "session_persistence_cookie",
            }
        }

    xml ex:
        <session_persistence xmlns=""
            type="COOKIE"
            cookie_name="session_persistence_cookie"
        />

    """

    ROOT_TAG = 'session_persistence'

    def __init__(self, type_=None, cookie_name=None):
        """
        @summary: Session Persistence Response Object Model
        @param type_: Type of session persistence that is set.
        @type type_: str
        @param cookie_name: Name of cookie that is set.
        @type cookie_name: str
        @return: Session Persistence Response Object
        @rtype: SessionPersistence
        """
        super(SessionPersistence, self).__init__()
        self.type_ = type_
        self.cookie_name = cookie_name
        self.attr_dict = {
            'type': self.type_,
            'cookie_name': self.cookie_name
        }

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._dict_to_obj(json_dict[cls.ROOT_TAG])

    @classmethod
    def _dict_to_obj(cls, session_persistence_dict):
        session_persistence = SessionPersistence(
            type_=session_persistence_dict.get('type'),
            cookie_name=session_persistence_dict.get('cookie_name'))
        return session_persistence

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        session_persistence = cls._xml_ele_to_obj(element)
        return session_persistence

    @classmethod
    def _xml_ele_to_obj(cls, element):
        session_persistence_dict = element.attrib
        session_persistence = SessionPersistence(
            type_=session_persistence_dict.get('type'),
            cookie_name=session_persistence_dict.get('cookie_name'))
        return session_persistence
