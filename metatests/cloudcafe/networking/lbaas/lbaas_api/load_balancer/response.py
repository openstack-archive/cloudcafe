"""
Copyright 2014-2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@summary: Unit tests for the load balancer response models.

LoadBalancerResponseTest
LoadBalancersResponseTest

"""

import unittest

from cloudcafe.networking.lbaas.lbaas_api.load_balancer.response \
    import LoadBalancer, LoadBalancers


class BaseLoadBalancerResponseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseLoadBalancerResponseTest, cls).setUpClass()
        cls.id_ = "8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
        cls.name = "a-new-loadbalancer"
        cls.vip_subnet = "SUBNET_ID"
        cls.tenant_id = "7725fe12-1c14-4f45-ba8e-44bf01763578"
        cls.admin_state_up = True
        cls.description = "A very simple example load balancer."
        cls.vip_address = "1.2.3.4"
        cls.status = "ACTIVE"

        cls.load_balancer_obj = LoadBalancer(
            id_=cls.id_, name=cls.name, vip_subnet=cls.vip_subnet,
            tenant_id=cls.tenant_id, admin_state_up=cls.admin_state_up,
            description=cls.description, vip_address=cls.vip_address,
            status=cls.status)
        load_balancer_list = [cls.load_balancer_obj]
        cls.load_balancers_obj = LoadBalancers(load_balancer_list)

        cls.lb_attribute_kwargs = {
            "id_": cls.id_,
            "name": cls.name,
            "vip_subnet": cls.vip_subnet,
            "tenant_id": cls.tenant_id,
            "admin_state_up": str(cls.admin_state_up).lower(),
            "description": cls.description,
            "vip_address": cls.vip_address,
            "status": cls.status
        }
        cls.actual_json_base = """
                    "id": "{id_}",
                    "name":"{name}",
                    "vip_subnet":"{vip_subnet}",
                    "tenant_id": "{tenant_id}",
                    "admin_state_up": {admin_state_up},
                    "description": "{description}",
                    "vip_address": "{vip_address}",
                    "status": "{status}"
        """.format(**cls.lb_attribute_kwargs)


class LoadBalancerResponseTest(BaseLoadBalancerResponseTest):

    def setUp(self):
        super(LoadBalancerResponseTest, self).setUp()
        self.ROOT_TAG = LoadBalancer.ROOT_TAG
        self.expected_obj = self.load_balancer_obj

    def test_load_balancer_json(self):
        actual_json = """
            {{ "{root_tag}":
                {{
                    {actual_json_base}
                }}
            }}
            """.format(root_tag=self.ROOT_TAG,
                       actual_json_base=self.actual_json_base,
                       **self.lb_attribute_kwargs)
        actual_obj = LoadBalancer.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)


class LoadBalancersResponseTest(BaseLoadBalancerResponseTest):

    def setUp(self):
        super(LoadBalancersResponseTest, self).setUp()
        self.ROOT_TAG = LoadBalancers.ROOT_TAG
        self.expected_obj = self.load_balancers_obj

    def test_load_balancers_json(self):
        actual_json = """
                        {{ "{root_tag}":
                            [{{
                                {actual_json_base}
                            }}]
                        }}
                        """.format(root_tag=self.ROOT_TAG,
                                   actual_json_base=self.actual_json_base,
                                   **self.lb_attribute_kwargs)
        actual_obj = LoadBalancers.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)


if __name__ == "__main__":
    unittest.main()
