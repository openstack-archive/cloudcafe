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

import mock

from cloudcafe.networking.lbaas.lbaas_api.load_balancer.client \
    import LoadBalancersClient
from cloudcafe.networking.lbaas.lbaas_api.load_balancer.request \
    import CreateLoadBalancer, UpdateLoadBalancer
from cloudcafe.networking.lbaas.lbaas_api.load_balancer.response \
    import LoadBalancer, LoadBalancers


class LoadBalancersClientFixture(unittest.TestCase):
    """
    @summary: Load Balancer Client Tests
    """
    @classmethod
    def setUpClass(cls):
        super(LoadBalancersClientFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.url = "http://fake.url.endpoint"
        cls.load_balancer_id = "12345"
        cls.name = "a-new-loadbalancer"
        cls.vip_subnet = "SUBNET_ID"
        cls.tenant_id = "7725fe12-1c14-4f45-ba8e-44bf01763578"
        cls.admin_state_up = True
        cls.description = "A very simple example load balancer."
        cls.vip_address = "1.2.3.4"
        cls.admin_state_up = False

        cls.full_url_load_balancers = (
            LoadBalancersClient._LOAD_BALANCERS_URL.format(
                base_url=cls.url))
        cls.full_url_load_balancer = (
            LoadBalancersClient._LOAD_BALANCER_URL.format(
                base_url=cls.url,
                load_balancer_id=cls.load_balancer_id))

        cls.load_balancers_client = LoadBalancersClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)


class LoadBalancersClientTests(object):

    @mock.patch.object(LoadBalancersClient, 'request', autospec=True)
    def test_create_load_balancer(self, mock_request):

        create_load_balancer_kwargs = (
            {'name': self.name,
             'vip_subnet': self.vip_subnet,
             'tenant_id': self.tenant_id,
             'description': self.description,
             'vip_address': self.vip_address,
             'admin_state_up': self.admin_state_up})
        self.load_balancers_client.create_load_balancer(
            **create_load_balancer_kwargs)
        create_load_balancer_request = CreateLoadBalancer(
            **create_load_balancer_kwargs)
        mock_request.assert_called_once_with(
            self.load_balancers_client,
            'POST',
            self.full_url_load_balancers,
            request_entity=create_load_balancer_request,
            response_entity_type=LoadBalancer,
            requestslib_kwargs=None)

    @mock.patch.object(LoadBalancersClient, 'request', autospec=True)
    def test_list_load_balancer(self, mock_request):

        self.load_balancers_client.list_load_balancers()
        mock_request.assert_called_once_with(
            self.load_balancers_client,
            'GET',
            self.full_url_load_balancers,
            response_entity_type=LoadBalancers,
            requestslib_kwargs=None)

    @mock.patch.object(LoadBalancersClient, 'request', autospec=True)
    def test_get_load_balancer(self, mock_request):

        self.load_balancers_client.get_load_balancer(
            load_balancer_id=self.load_balancer_id)
        mock_request.assert_called_once_with(
            self.load_balancers_client,
            'GET',
            self.full_url_load_balancer,
            response_entity_type=LoadBalancer,
            requestslib_kwargs=None)

    @mock.patch.object(LoadBalancersClient, 'request', autospec=True)
    def test_update_load_balancer(self, mock_request):

        update_load_balancer_kwargs = (
            {'name': self.name,
             'description': self.description,
             'admin_state_up': self.admin_state_up})
        self.load_balancers_client.update_load_balancer(
            load_balancer_id=self.load_balancer_id,
            **update_load_balancer_kwargs)
        update_load_balancer_request = UpdateLoadBalancer(
            **update_load_balancer_kwargs)
        mock_request.assert_called_once_with(
            self.load_balancers_client,
            'PUT',
            self.full_url_load_balancer,
            request_entity=update_load_balancer_request,
            response_entity_type=LoadBalancer,
            requestslib_kwargs=None)

    @mock.patch.object(LoadBalancersClient, 'request', autospec=True)
    def test_delete_load_balancer(self, mock_request):

        self.load_balancers_client.delete_load_balancer(
            load_balancer_id=self.load_balancer_id)
        mock_request.assert_called_once_with(self.load_balancers_client,
                                             'DELETE',
                                             self.full_url_load_balancer,
                                             requestslib_kwargs=None)


class LoadBalancersClientTestsXML(LoadBalancersClientFixture,
                                  LoadBalancersClientTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class LoadBalancersClientTestsJSON(LoadBalancersClientFixture,
                                   LoadBalancersClientTests):
    SERIALIZE = 'json'
    DESERIALIZE = 'json'
