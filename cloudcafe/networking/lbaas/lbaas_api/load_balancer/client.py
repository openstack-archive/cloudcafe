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

from cloudcafe.networking.lbaas.common.client import BaseLoadBalancersClient
from cloudcafe.networking.lbaas.lbaas_api.load_balancer.request \
    import CreateLoadBalancer, UpdateLoadBalancer
from cloudcafe.networking.lbaas.lbaas_api.load_balancer.response \
    import LoadBalancer, LoadBalancers


class LoadBalancersClient(BaseLoadBalancersClient):
    """
    Load Balancer Client

    @summary: A load balancer is a logical device which belongs to a cloud
        account.  It is used to distribute workloads between multiple
        back-end systems or services, based on the criteria defined as part
        of its configuration.
    """
    _LOAD_BALANCERS_URL = "{base_url}/loadbalancers"
    _LOAD_BALANCER_URL = "{base_url}/loadbalancers/{load_balancer_id}"

    def create_load_balancer(self, name, vip_subnet, tenant_id,
                             admin_state_up=None, description=None,
                             vip_address=None, requestslib_kwargs=None):
        """Create Load Balancer
        @summary: Creates an instance of a load balancer given the
            provided parameters
        @param name: Name of the load balancer.
        @type name: String
        @param vip_subnet: Subnet from which to allocate a virtual IP address.
        @type vip_subnet:  String
        @param tenant_id: Tenant that will own this load balancer.
        @type tenant_id: String
        @param admin_state_up: Defines whether an active load balancer is
            functioning or not
        @type admin_state_up: Boolean
        @param description: Detailed description of the load balancer.
        @type description: String
        @param vip_address: IP address to assign to VIP.
        @type vip_address: String
        @param admin_state_up: Enabled or Disabled
            Default: "true"
        @type admin_state_up: bool
        @return: Response Object containing response code and the
            load balancer domain object
        @rtype: Requests.response
        """
        full_url = self._LOAD_BALANCERS_URL.format(base_url=self.url)
        load_balancer_request_object = CreateLoadBalancer(
            name=name, vip_subnet=vip_subnet, tenant_id=tenant_id,
            admin_state_up=admin_state_up, description=description,
            vip_address=vip_address)

        return self.request('POST', full_url,
                            response_entity_type=LoadBalancer,
                            request_entity=load_balancer_request_object,
                            requestslib_kwargs=requestslib_kwargs)

    def list_load_balancers(self, requestslib_kwargs=None):
        """List Load Balancers
        @summary: List all load balancers configured for the account.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._LOAD_BALANCERS_URL.format(base_url=self.url)
        return self.request('GET', full_url,
                            response_entity_type=LoadBalancers,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer(self, load_balancer_id, name=None,
                             description=None, admin_state_up=None,
                             requestslib_kwargs=None):
        """Update Load Balancer
        @summary: Update the properties of a load balancer given the
            provided parameters
        @param load_balancer_id: ID of the load balancer to get details from.
        @type load_balancer_id: str
        @param name: Name of the load balancer.
        @type name: str
        @param description: Detailed description of the load balancer.
        @type description: str
        @param admin_state_up: Defines whether an active load balancer is
            functioning or not
        @type admin_state_up: bool
        @return: Response Object containing response code.
        @rtype: Requests.response
        """
        update_load_balancer = UpdateLoadBalancer(
            name=name, description=description, admin_state_up=admin_state_up)
        full_url = self._LOAD_BALANCER_URL.format(
            base_url=self.url,
            load_balancer_id=load_balancer_id)
        return self.request('PUT', full_url,
                            request_entity=update_load_balancer,
                            response_entity_type=LoadBalancer,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancer(self, load_balancer_id, requestslib_kwargs=None):
        """Get Load Balancer Details
        @summary: List details of the specified load balancer.
        @param load_balancer_id: ID of the load balancer to get details from.
        @type load_balancer_id: str
        @return: Response Object containing response code and the
            load balancer domain object.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._LOAD_BALANCER_URL.format(
            base_url=self.url,
            load_balancer_id=load_balancer_id)
        return self.request('GET', full_url,
                            response_entity_type=LoadBalancer,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_load_balancer(self, load_balancer_id, requestslib_kwargs=None):
        """Delete Load Balancer
        @summary: Remove a load balancer from the account.
        @param load_balancer_id: ID of the load balancer to delete.
        @type load_balancer_id: str
        @return: Response Object containing response code.
        @rtype: Requests.response
        @note: Returns an error if it's still in use by any pools.
        """
        full_url = self._LOAD_BALANCER_URL.format(
            base_url=self.url,
            load_balancer_id=load_balancer_id)
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)
