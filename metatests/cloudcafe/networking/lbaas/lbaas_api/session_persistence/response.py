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

SessionPersistenceRequestTest
"""

import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.session_persistence.response \
    import SessionPersistence


class BaseSessionPersistenceResponseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseSessionPersistenceResponseTest, cls).setUpClass()

        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.ROOT_TAG = SessionPersistence.ROOT_TAG
        cls.type_ = "COOKIE"
        cls.cookie_name = "session_persistence_cookie"
        cls.session_persistence_obj = SessionPersistence(
            type_=cls.type_,
            cookie_name=cls.cookie_name
        )


class SessionPersistenceResponseTest(BaseSessionPersistenceResponseTest):

    def setUp(self):
        super(SessionPersistenceResponseTest, self).setUp()
        self.ROOT_TAG = SessionPersistence.ROOT_TAG
        self.expected_obj = self.session_persistence_obj

    def test_session_persistence_json(self):

        actual_json = """
                        {{ "{root_tag}":
                            {{
                                "type": "{type_}",
                                "cookie_name": "{cookie_name}"
                            }}
                        }}
                        """.format(root_tag=self.ROOT_TAG,
                                   type_=self.type_,
                                   cookie_name=self.cookie_name)
        actual_obj = SessionPersistence.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_session_persistence_xml(self):

        actual_xml = """{xml_header}
                            <{root_tag}
                                type="{type_}"
                                cookie_name="{cookie_name}"
                            xmlns="{xmlns}" />""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            type_=self.type_,
            cookie_name=self.cookie_name)
        actual_obj = SessionPersistence.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)

if __name__ == "__main__":
    unittest.main()
