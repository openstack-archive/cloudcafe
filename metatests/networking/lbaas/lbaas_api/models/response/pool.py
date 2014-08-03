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

@summary: Unit tests for the load balancer "pool" response model.

PoolResponseTest
PoolsResponseTest

"""

import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.models.response.pool \
    import Pool, Pools
from cloudcafe.networking.lbaas.lbaas_api.models.response.session_persistence \
    import SessionPersistence


class BasePoolResponseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(BasePoolResponseTest, cls).setUpClass()
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.id_ = "8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
        cls.name = "Example HTTPS Pool"
        cls.description = "A simple example of an HTTPS pool."
        cls.tenant_id = "7725fe12-1c14-4f45-ba8e-44bf01763578"
        cls.protocol = "HTTPS"
        cls.lb_algorithm = "ROUND_ROBIN"
        cls.healthmonitor_id = "8311446e-8a13-4c00-95b3-03a92f9759c7"
        cls.admin_state_up = True
        cls.status = "ACTIVE"
        cls.persistence_type = "COOKIE"
        cls.cookie_name = "session_persistence_cookie"
        cls.session_persistence_obj = SessionPersistence(
            type_=cls.persistence_type,
            cookie_name=cls.cookie_name)

        cls.pool_obj = Pool(
            id_=cls.id_, name=cls.name, description=cls.description,
            tenant_id=cls.tenant_id, protocol=cls.protocol,
            lb_algorithm=cls.lb_algorithm,
            healthmonitor_id=cls.healthmonitor_id,
            admin_state_up=cls.admin_state_up,
            status=cls.status,
            session_persistence=cls.session_persistence_obj)
        pool_list = [cls.pool_obj]
        cls.pools_obj = Pools(pool_list)

        cls.pool_attribute_kwargs = {
            "id_": cls.id_,
            "name": cls.name,
            "description": cls.description,
            "tenant_id": cls.tenant_id,
            "protocol": cls.protocol,
            "lb_algorithm": cls.lb_algorithm,
            "healthmonitor_id": cls.healthmonitor_id,
            "admin_state_up": str(cls.admin_state_up).lower(),
            "status": cls.status,
            "persistence_type": cls.persistence_type,
            "cookie_name": cls.cookie_name,
        }
        cls.actual_json_base = """
                    "id": "{id_}",
                    "name":"{name}",
                    "description":"{description}",
                    "tenant_id": "{tenant_id}",
                    "protocol": "{protocol}",
                    "lb_algorithm": "{lb_algorithm}",
                    "healthmonitor_id": "{healthmonitor_id}",
                    "admin_state_up": {admin_state_up},
                    "status": "{status}",
                    "session_persistence": {{
                        "type": "{persistence_type}",
                        "cookie_name": "{cookie_name}"
                    }}
        """.format(**cls.pool_attribute_kwargs)

        cls.actual_xml_base = """
                    id="{id_}"
                    name="{name}"
                    description="{description}"
                    tenant_id="{tenant_id}"
                    protocol="{protocol}"
                    lb_algorithm="{lb_algorithm}"
                    healthmonitor_id="{healthmonitor_id}"
                    admin_state_up="{admin_state_up}"
                    status="{status}" >
                    <session_persistence
                        type="{persistence_type}"
                        cookie_name="{cookie_name}"
                    />
        """.format(**cls.pool_attribute_kwargs)


class PoolResponseTest(BasePoolResponseTest):

    def setUp(self):
        super(PoolResponseTest, self).setUp()
        self.ROOT_TAG = Pool.ROOT_TAG
        self.expected_obj = self.pool_obj

    def test_pool_json(self):
        actual_json = """
            {{ "{root_tag}":
                {{
                    {actual_json_base}
                }}
            }}
            """.format(root_tag=self.ROOT_TAG,
                       actual_json_base=self.actual_json_base,
                       **self.pool_attribute_kwargs)
        actual_obj = Pool.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_pool_xml(self):
        actual_xml = """{xml_header}
                            <{root_tag}
                                {actual_xml_base}
                                xmlns="{xmlns}"
                            </{root_tag}>""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            actual_xml_base=self.actual_xml_base,
            **self.pool_attribute_kwargs)
        actual_obj = Pool.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)


class PoolsResponseTest(BasePoolResponseTest):

    def setUp(self):
        super(PoolsResponseTest, self).setUp()
        self.ROOT_TAG = Pools.ROOT_TAG
        self.CHILD_TAG = Pool.ROOT_TAG
        self.expected_obj = self.pools_obj

    def test_pools_json(self):
        actual_json = """
                        {{ "{root_tag}":
                            [{{
                                {actual_json_base}
                            }}]
                        }}
                        """.format(root_tag=self.ROOT_TAG,
                                   actual_json_base=self.actual_json_base,
                                   **self.pool_attribute_kwargs)
        actual_obj = Pools.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_pools_xml(self):
        actual_xml = """{xml_header}
                            <{root_tag} xmlns="{xmlns}">
                                <{child_tag}
                                    {actual_xml_base}
                                </{child_tag}>
                            </{root_tag}>""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            child_tag=self.CHILD_TAG,
            actual_xml_base=self.actual_xml_base,
            **self.pool_attribute_kwargs)
        actual_obj = Pools.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)


if __name__ == "__main__":
    unittest.main()
