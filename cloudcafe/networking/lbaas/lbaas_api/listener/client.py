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
from cloudcafe.networking.lbaas.lbaas_api.listener.request import \
    CreateListener, UpdateListener
from cloudcafe.networking.lbaas.lbaas_api.listener.response import \
    Listener, Listeners


class ListenersClient(BaseLoadBalancersClient):
    """
    Listeners Client

    @summary: Listeners represent a single listening port and can optionally
        provide TLS termination.
    """
    _LISTENERS_URL = "{base_url}/listeners"
    _LISTENER_URL = "{base_url}/listeners/{listener_id}"

    def create_listener(self, name, load_balancer_id, tenant_id,
                        default_pool_id, protocol, protocol_port,
                        description=None, connection_limit=None,
                        admin_state_up=None, requestslib_kwargs=None):
        """Create Listener
        @summary: Creates an instance of a listener given the
            provided parameters
        @param name: Name of the listener that will be created
        @type name: String
        @param load_balancer_id:  ID of a load balancer.
        @type load_balancer_id: String
        @param tenant_id: Tenant that will own the listener.
        @type tenant_id: String
        @param default_pool_id: ID of default pool.  Must have compatible
            protocol with listener.
        @type default_pool_id: String
        @param protocol: Protocol to load balance: HTTP, HTTPS, TCP, UDP
        @type protocol: String
        @param protocol_port: TCP (or UDP) port to listen on.
        @type protocol_port: Integer
        @param description: Detailed description of the listener.
        @type description: String

        @param connection_limit: Maximum connections the load balancer can
            have.  Default is infinite.
        @type connection_limit: Integer
        @param admin_state_up: If set to false, listener will be created in an
            administratively down state
        @type admin_state_up: Boolean
        @return: Response Object containing response code and the
            listener domain object
        @rtype: Requests.response
        """
        full_url = self._LISTENERS_URL.format(base_url=self.url)
        listener_request_object = CreateListener(
            name=name, load_balancer_id=load_balancer_id, tenant_id=tenant_id,
            default_pool_id=default_pool_id, protocol=protocol,
            protocol_port=protocol_port, description=description,
            connection_limit=connection_limit, admin_state_up=admin_state_up)
        return self.request('POST', full_url,
                            response_entity_type=Listener,
                            request_entity=listener_request_object,
                            requestslib_kwargs=requestslib_kwargs)

    def list_listeners(self, requestslib_kwargs=None):
        """List Listeners
        @summary: List all listeners configured for the account.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._LISTENERS_URL.format(base_url=self.url)
        return self.request('GET', full_url,
                            response_entity_type=Listeners,
                            requestslib_kwargs=requestslib_kwargs)

    def update_listener(self, listener_id, name=None, description=None,
                        default_pool_id=None, load_balancer_id=None,
                        admin_state_up=None, requestslib_kwargs=None):
        """Update Listener
        @summary: Update the properties of a listener given the
            provided parameters
        @param listener_id: ID of the listener to get details from.
        @type listener_id: str
        @param name: Name of the listener that will be created
        @type name: String
        @param description: Detailed description of the listener.
        @type description: String
        @param default_pool_id: ID of default pool.  Must have compatible
            protocol with listener.
        @type default_pool_id: String
        @param load_balancer_id:  ID of a load balancer.
        @type load_balancer_id: String
        @param admin_state_up: If set to false, listener will be created in an
            administratively down state
        @type admin_state_up: Boolean
        @return: Response Object containing response code.
        @rtype: Requests.response
        """
        update_listener = UpdateListener(
            name=name, description=description,
            default_pool_id=default_pool_id,
            load_balancer_id=load_balancer_id,
            admin_state_up=admin_state_up)
        full_url = self._LISTENER_URL.format(base_url=self.url,
                                             listener_id=listener_id)
        return self.request('PUT', full_url,
                            request_entity=update_listener,
                            response_entity_type=Listener,
                            requestslib_kwargs=requestslib_kwargs)

    def get_listener(self, listener_id, requestslib_kwargs=None):
        """Get Listener Details
        @summary: List details of the specified listener.
        @param listener_id: ID of the listener to get details from.
        @type listener_id: str
        @return: Response Object containing response code and the
            listener domain object.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._LISTENER_URL.format(base_url=self.url,
                                             listener_id=listener_id)
        return self.request('GET', full_url,
                            response_entity_type=Listener,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_listener(self, listener_id, requestslib_kwargs=None):
        """Delete Listener
        @summary: Remove a listener from the account.
        @param listener_id: ID of the listener to delete.
        @type listener_id: str
        @return: Response Object containing response code.
        @rtype: Requests.response
        @note: Returns an error if it's still in use by any pools.
        """
        full_url = self._LISTENER_URL.format(
            base_url=self.url,
            listener_id=listener_id)
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)
