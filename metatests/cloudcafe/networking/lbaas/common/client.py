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

import unittest

from lbaascafe.lbaas.lbaas_api.clients.base_load_balancers_client \
    import BaseLoadBalancersClient


class BaseLoadBalancersClientFixture(unittest.TestCase):
    """
    @summary: Base Load Balancers Client for Load Balancer Client Tests
    """
    SERIALIZE = None
    DESERIALIZE = None

    @classmethod
    def setUpClass(cls):
        super(BaseLoadBalancersClientFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.load_balancer_id = "12345"
        cls.url = "http://fake.url.endpoint"
        cls.load_balancers_url = '{url}/{suffix}'.format(
            url=cls.url, suffix=BaseLoadBalancersClient._SUFFIX)
