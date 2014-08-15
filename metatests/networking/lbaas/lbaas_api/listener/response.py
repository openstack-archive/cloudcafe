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

@summary: Unit tests for the load balancer "listener" response model.

ListenerResponseTest
ListenersResponseTest

"""

import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.listener.response \
    import Listener, Listeners


class BaseListenerResponseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseListenerResponseTest, cls).setUpClass()
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.id_ = "8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
        cls.name = "Example HTTPS Listener"
        cls.description = "A simple example of an HTTPS listener."
        cls.load_balancer_id = "b8a35470-f65d-11e3-a3ac-0800200c9a66"
        cls.tenant_id = "7725fe12-1c14-4f45-ba8e-44bf01763578"
        cls.default_pool_id = "8311446e-8a13-4c00-95b3-03a92f9759c7"
        cls.connection_limit = 200
        cls.protocol = "HTTPS"
        cls.protocol_port = 443
        cls.admin_state_up = True
        cls.status = "ACTIVE"

        cls.listener_obj = Listener(
            id_=cls.id_, name=cls.name, description=cls.description,
            load_balancer_id=cls.load_balancer_id,
            tenant_id=cls.tenant_id, default_pool_id=cls.default_pool_id,
            connection_limit=cls.connection_limit, protocol=cls.protocol,
            protocol_port=cls.protocol_port, admin_state_up=cls.admin_state_up,
            status=cls.status)
        listener_list = [cls.listener_obj]
        cls.listeners_obj = Listeners(listener_list)

        cls.listener_attribute_kwargs = {
            "id_": cls.id_,
            "name": cls.name,
            "description": cls.description,
            "load_balancer_id": cls.load_balancer_id,
            "tenant_id": cls.tenant_id,
            "default_pool_id": cls.default_pool_id,
            "connection_limit": cls.connection_limit,
            "protocol": cls.protocol,
            "protocol_port": cls.protocol_port,
            "admin_state_up": str(cls.admin_state_up).lower(),
            "status": cls.status
        }
        cls.actual_json_base = """
                    "id": "{id_}",
                    "name":"{name}",
                    "description":"{description}",
                    "load_balancer_id": "{load_balancer_id}",
                    "tenant_id": "{tenant_id}",
                    "default_pool_id": "{default_pool_id}",
                    "connection_limit": {connection_limit},
                    "protocol": "{protocol}",
                    "protocol_port": {protocol_port},
                    "admin_state_up": {admin_state_up},
                    "status": "{status}"
        """.format(**cls.listener_attribute_kwargs)

        cls.actual_xml_base = """
                    id="{id_}"
                    name="{name}"
                    description="{description}"
                    load_balancer_id="{load_balancer_id}"
                    tenant_id="{tenant_id}"
                    default_pool_id="{default_pool_id}"
                    connection_limit="{connection_limit}"
                    protocol="{protocol}"
                    protocol_port="{protocol_port}"
                    admin_state_up="{admin_state_up}"
                    status="{status}"
        """.format(**cls.listener_attribute_kwargs)


class ListenerResponseTest(BaseListenerResponseTest):

    def setUp(self):
        super(ListenerResponseTest, self).setUp()
        self.ROOT_TAG = Listener.ROOT_TAG
        self.expected_obj = self.listener_obj

    def test_listener_json(self):
        actual_json = """
            {{ "{root_tag}":
                {{
                    {actual_json_base}
                }}
            }}
            """.format(root_tag=self.ROOT_TAG,
                       actual_json_base=self.actual_json_base,
                       **self.listener_attribute_kwargs)
        actual_obj = Listener.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_listener_xml(self):
        actual_xml = """{xml_header}
                            <{root_tag}
                                {actual_xml_base}
                                xmlns="{xmlns}"
                            />""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            actual_xml_base=self.actual_xml_base,
            **self.listener_attribute_kwargs)
        actual_obj = Listener.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)


class ListenersResponseTest(BaseListenerResponseTest):

    def setUp(self):
        super(ListenersResponseTest, self).setUp()
        self.ROOT_TAG = Listeners.ROOT_TAG
        self.CHILD_TAG = Listener.ROOT_TAG
        self.expected_obj = self.listeners_obj

    def test_listeners_json(self):
        actual_json = """
                        {{ "{root_tag}":
                            [{{
                                {actual_json_base}
                            }}]
                        }}
                        """.format(root_tag=self.ROOT_TAG,
                                   actual_json_base=self.actual_json_base,
                                   **self.listener_attribute_kwargs)
        actual_obj = Listeners.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_listeners_xml(self):
        actual_xml = """{xml_header}
                            <{root_tag} xmlns="{xmlns}">
                                <{child_tag}
                                    {actual_xml_base}
                                />
                            </{root_tag}>""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            child_tag=self.CHILD_TAG,
            actual_xml_base=self.actual_xml_base,
            **self.listener_attribute_kwargs)
        actual_obj = Listeners.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)


if __name__ == "__main__":
    unittest.main()
