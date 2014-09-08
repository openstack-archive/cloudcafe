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

from cloudcafe.networking.lbaas.common.behaviors import \
    BaseLoadBalancersBehaviors


class LoadBalancerBehaviors(BaseLoadBalancersBehaviors):

    OBJECT_MODEL = 'loadbalancer'

    def __init__(self, load_balancers_client, config):
        super(LoadBalancerBehaviors, self).__init__(
            lbaas_client_type=load_balancers_client, config=config)

    def create_active_load_balancer(
            self, name, vip_subnet, tenant_id,
            description=None, vip_address=None, admin_state_up=None):
        """
        @summary: Creates a load balancer and waits for it to become active
        @param name: Name of the load balancer.
        @type name: str
        @param vip_subnet: Subnet from which to allocate a virtual IP address.
        @type vip_subnet:  str
        @param tenant_id: Tenant that will own this load balancer.
        @type tenant_id: str
        @param description: Detailed description of the load balancer.
        @type description: str
        @param vip_address: IP address to assign to VIP.
        @type vip_address: str
        @param admin_state_up: Defines whether an active load balancer is
            functioning or not
        @type admin_state_up: bool
        @return: Response object containing response and the load balancer
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'name': name, 'vip_subnet': vip_subnet,
                  'tenant_id': tenant_id, 'description': description,
                  'vip_address': vip_address, 'admin_state_up': admin_state_up}
        resp = self.create_active_lbaas_object(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def update_load_balancer_and_wait_for_active(
            self, name=None, description=None, admin_state_up=None):
        """
        @summary: Updates a load balancer and waits for it to become active
        @param name: Name of the load balancer.
        @type name: str
        @param description: Detailed description of the load balancer.
        @type description: str
        @param admin_state_up: Defines whether an active load balancer is
            functioning or not
        @type admin_state_up: bool
        @return: Response object containing response and the load balancer
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'name': name,
                  'description': description,
                  'admin_state_up': admin_state_up}
        resp = self.update_lbaas_object_and_wait_for_active(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def wait_for_load_balancer_status(self, load_balancer_id, desired_status,
                                      interval_time=None, timeout=None):
        """
        @summary: Waits for a load balancer to reach a desired status
        @param load_balancer_id: The id of the load balancer
        @type load_balancer_id: String
        @param desired_status: The desired final status of the load balancer
        @type desired_status: String
        @param interval_time: The amount of time in seconds to wait
            between polling
        @type interval_time: Integer
        @param interval_time: The amount of time in seconds to wait
            before aborting
        @type interval_time: Integer
        @return: Response object containing response and the load balancer
            domain object
        @rtype: requests.Response
        """
        kwargs = {'load_balancer_id': load_balancer_id,
                  'desired_status': desired_status,
                  'interval_time': interval_time,
                  'timeout': timeout}
        resp = self.wait_for_lbaas_object_status(
            lbaas_model_type=self.OBJECT_MODEL, **kwargs)
        return resp
