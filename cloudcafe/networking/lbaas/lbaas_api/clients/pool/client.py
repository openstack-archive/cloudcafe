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
from cloudcafe.networking.lbaas.lbaas_api.models.request.pool import \
    CreatePool, UpdatePool
from cloudcafe.networking.lbaas.lbaas_api.models.response.pool import \
    Pool, Pools


class PoolsClient(BaseLoadBalancersClient):
    """
    Pools Client

    @summary: Pools are groupings of backend member servers to which client
        requests are forwarded.
    """
    _POOLS_URL = "{base_url}/pools"
    _POOL_URL = "{base_url}/pools/{pool_id}"

    def create_pool(self, name, tenant_id, protocol, lb_algorithm,
                    description=None, session_persistence=None,
                    healthmonitor_id=None, admin_state_up=None,
                    requestslib_kwargs=None):
        """Create Pool
        @summary: Creates an instance of a pool given the
            provided parameters
        @param name: Name of the Pool that will be created
        @type name: str
        @param tenant_id:  Tenant that will own the pool.
        @type tenant_id: str
        @param protocol: Protocol use to connect to members: HTTP, HTTPS, TCP
        @type protocol: str
        @param lb_algorithm: round-robin, least-connections, etc. (load
            balancing provider dependent, but round-robin must be supported).
        @type lb_algorithm: str
        @param description: Description of a pool.
        @type description: str
        @param session_persistence: Session persistence algorithm that should
            be used (if any). This is a dictionary that has keys of
            "type" and "cookie_name".
                Default: {}
        @type session_persistence: dict
        @param healthmonitor_id: ID of existing health monitor.
            Default: null
        @type healthmonitor_id: str
        @param admin_state_up: Enabled or Disabled
            Default: "true"
        @type admin_state_up: bool
        @return: Response Object containing response code and the
            load balancer domain object
        @rtype: Requests.response
        """
        full_url = self._POOLS_URL.format(base_url=self.url)
        pool_request_object = CreatePool(
            name=name, tenant_id=tenant_id, protocol=protocol,
            lb_algorithm=lb_algorithm, description=description,
            session_persistence=session_persistence,
            healthmonitor_id=healthmonitor_id, admin_state_up=admin_state_up)
        return self.request('POST', full_url,
                            response_entity_type=Pool,
                            request_entity=pool_request_object,
                            requestslib_kwargs=requestslib_kwargs)

    def list_pools(self, requestslib_kwargs=None):
        """List Pools
        @summary: List all pools configured for the account.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._POOLS_URL.format(base_url=self.url)
        return self.request('GET', full_url,
                            response_entity_type=Pools,
                            requestslib_kwargs=requestslib_kwargs)

    def update_pool(self, pool_id, name=None, description=None,
                    session_persistence=None, lb_algorithm=None,
                    healthmonitor_id=None, admin_state_up=None,
                    requestslib_kwargs=None):
        """Update Pool
        @summary: Update the properties of a pool given the
            provided parameters
        @param name: Name of the Pool that will be created
        @type name: str
        @param description: Description of a pool.
        @type description: str
        @param session_persistence: Session persistence algorithm that should
            be used (if any). This is a dictionary that has keys of
            "type" and "cookie_name".
                Default: {}
        @type session_persistence: dict

        @param lb_algorithm: round-robin, least-connections, etc. (load
            balancing provider dependent, but round-robin must be supported).
        @type lb_algorithm: str
        @param healthmonitor_id: ID of existing health monitor.
            Default: null
        @type healthmonitor_id: str
        @param admin_state_up: Enabled or Disabled
            Default: "true"
        @type admin_state_up: bool
        @return: Response Object containing response code.
        @rtype: Requests.response
        """
        update_pool = UpdatePool(
            name=name, description=description,
            session_persistence=session_persistence,
            lb_algorithm=lb_algorithm, healthmonitor_id=healthmonitor_id,
            admin_state_up=admin_state_up)
        full_url = self._POOL_URL.format(base_url=self.url, pool_id=pool_id)
        return self.request('PUT', full_url,
                            request_entity=update_pool,
                            response_entity_type=Pool,
                            requestslib_kwargs=requestslib_kwargs)

    def get_pool(self, pool_id, requestslib_kwargs=None):
        """Get Pool Details
        @summary: List details of the specified pool.
        @param pool_id: ID of the pool to get details from.
        @type pool_id: str
        @return: Response Object containing response code and the
            pool domain object.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._POOL_URL.format(base_url=self.url, pool_id=pool_id)
        return self.request('GET', full_url,
                            response_entity_type=Pool,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_pool(self, pool_id, requestslib_kwargs=None):
        """Delete Pool
        @summary: Deletes an orphaned pool. Will return an error if pool is
            still in use by any listeners.  Upon successful deletion,
            any child primitives that this pool is using will be detached but
            not deleted.
        @param pool_id: ID of the pool to delete.
        @type pool_id: str
        @return: Response Object containing response code.
        @rtype: Requests.response
        @note: Returns an error if it's still in use by any pools.
        """
        full_url = self._POOL_URL.format(base_url=self.url, pool_id=pool_id)
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)
