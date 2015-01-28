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

import mock
import unittest

from cloudcafe.networking.lbaas.lbaas_api.load_balancer.behaviors import \
    LoadBalancerBehaviors
from cloudcafe.networking.lbaas.lbaas_api.load_balancer.client import \
    LoadBalancersClient


class LoadBalancerBehaviorsFixture(unittest.TestCase):
    """
    @summary: Load Balancer Behaviors Tests
    """
    @classmethod
    def setUpClass(cls):
        super(LoadBalancerBehaviorsFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.url = "http://fake.url.endpoint"
        cls.load_balancer_id = "12345"
        cls.name = "a-new-loadbalancer"
        cls.vip_subnet = "SUBNET_ID"
        cls.tenant_id = "7725fe12-1c14-4f45-ba8e-44bf01763578"
        cls.admin_state_up = True
        cls.description = "A very simple example load balancer."
        cls.vip_address = "1.2.3.4"

        cls.desired_status = "ACTIVE"
        cls.interval_time = 20
        cls.timeout = 120

        cls.load_balancers_client = LoadBalancersClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)

        cls.load_balancer_behaviors = LoadBalancerBehaviors(
            load_balancers_client=cls.load_balancers_client, config=None)


class LoadBalancerBehaviorsTests(object):

    @mock.patch.object(LoadBalancerBehaviors, 'create_active_load_balancer',
                       autospec=True)
    def test_create_active_load_balancer(self, mock_request):
        create_active_load_balancer_kwargs = (
            {'name': self.name,
             'vip_subnet': self.vip_subnet,
             'tenant_id': self.tenant_id,
             'description': self.description,
             'vip_address': self.vip_address,
             'admin_state_up': self.admin_state_up})
        self.load_balancer_behaviors.create_active_load_balancer(
            **create_active_load_balancer_kwargs)
        mock_request.assert_called_once_with(
            self.load_balancer_behaviors,
            **create_active_load_balancer_kwargs)

    @mock.patch.object(LoadBalancerBehaviors,
                       'update_load_balancer_and_wait_for_active',
                       autospec=True)
    def test_update_load_balancer_and_wait_for_active(self, mock_request):
        update_load_balancer_and_wait_for_active_kwargs = (
            {'name': self.name,
             'description': self.description,
             'admin_state_up': self.admin_state_up})
        self.load_balancer_behaviors.\
            update_load_balancer_and_wait_for_active(
                **update_load_balancer_and_wait_for_active_kwargs)
        mock_request.assert_called_once_with(
            self.load_balancer_behaviors,
            **update_load_balancer_and_wait_for_active_kwargs)

    @mock.patch.object(LoadBalancerBehaviors, 'wait_for_load_balancer_status',
                       autospec=True)
    def test_wait_for_load_balancer_status(self, mock_request):
        wait_for_load_balancer_status_kwargs = (
            {'load_balancer_id': self.load_balancer_id,
             'desired_status': self.desired_status,
             'interval_time': self.interval_time,
             'timeout': self.timeout})
        self.load_balancer_behaviors.wait_for_load_balancer_status(
            **wait_for_load_balancer_status_kwargs)
        mock_request.assert_called_once_with(
            self.load_balancer_behaviors,
            **wait_for_load_balancer_status_kwargs)


class LoadBalancersClientTestsXML(LoadBalancerBehaviorsFixture,
                                  LoadBalancerBehaviorsTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class LoadBalancersClientTestsJSON(LoadBalancerBehaviorsFixture,
                                   LoadBalancerBehaviorsTests):
    SERIALIZE = 'json'
    DESERIALIZE = 'json'
