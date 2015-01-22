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

@summary: Unit tests for the load balancer "session persistence" request model.

SetSessionPersistenceRequestTest
"""

import json
import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.session_persistence.request \
    import SetSessionPersistence


class SessionPersistenceRequestTestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.ROOT_TAG = SetSessionPersistence.ROOT_TAG
        cls.type_ = "COOKIE"
        cls.cookie_name = "session_persistence_cookie"
        cls.set_session_persistence_obj = SetSessionPersistence(
            type_=cls.type_,
            cookie_name=cls.cookie_name
        )


class SetSessionPersistenceRequestTest(SessionPersistenceRequestTestBase):

    def test_set_session_persistence_json(self):
        actual_json = json.loads(
            self.set_session_persistence_obj.serialize('json'))
        expected_json = json.loads(
            """
            {{
                 "{root_tag}":
                    {{
                        "type": "{type_}",
                        "cookie_name": "{cookie_name}"
                    }}
            }}
            """.format(root_tag=self.ROOT_TAG,
                       type_=self.type_,
                       cookie_name=self.cookie_name))
        self.assertEqual(expected_json, actual_json)

    def test_set_session_persistence_xml(self):
        actual_xml = self.set_session_persistence_obj.serialize('xml')
        expected_xml = (
            '{xml_header}<{root_tag} '
            'cookie_name="{cookie_name}" '
            'type="{type_}" xmlns="{xmlns}" />').format(
                xml_header=self.XML_HEADER,
                xmlns=self.XML_NS,
                root_tag=self.ROOT_TAG,
                type_=self.type_, cookie_name=self.cookie_name)
        self.assertEqual(expected_xml, actual_xml)

if __name__ == "__main__":
    unittest.main()
