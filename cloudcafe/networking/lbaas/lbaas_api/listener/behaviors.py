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


class ListenerBehaviors(BaseLoadBalancersBehaviors):

    OBJECT_MODEL = 'listener'

    def __init__(self, listeners_client, config):
        super(ListenerBehaviors, self).__init__(
            lbaas_client_type=listeners_client, config=config)

    def create_active_listener(
            self, name, load_balancer_id, tenant_id, default_pool_id,
            protocol, protocol_port, description=None,
            connection_limit=None, admin_state_up=None):
        """
        @summary: Creates a listener and waits for it to become active
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
        @return: Response object containing response and the listener
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'name': name, 'load_balancer_id': load_balancer_id,
                  'tenant_id': tenant_id, 'default_pool_id': default_pool_id,
                  'protocol': protocol, 'protocol_port': protocol_port,
                  'description': description,
                  'connection_limit': connection_limit,
                  'admin_state_up': admin_state_up}
        resp = self.create_active_lbaas_object(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def update_listener_and_wait_for_active(
            self, name=None, description=None, default_pool_id=None,
            load_balancer_id=None, admin_state_up=None):
        """
        @summary: Updates a listener and waits for it to become active
        @param name: Name of the listener that will be created
        @type name: String
        @param load_balancer_id:  ID of a load balancer.
        @type load_balancer_id: String
        @param default_pool_id: ID of default pool.  Must have compatible
            protocol with listener.
        @type default_pool_id: String
        @param description: Detailed description of the listener.
        @type description: String
        @param admin_state_up: If set to false, listener will be created in an
            administratively down state
        @type admin_state_up: Boolean
        @return: Response object containing response and the listener
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'name': name, 'description': description,
                  'default_pool_id': default_pool_id,
                  'load_balancer_id': load_balancer_id,
                  'admin_state_up': admin_state_up}
        resp = self.update_lbaas_object_and_wait_for_active(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def wait_for_listener_status(self, listener_id, desired_status,
                                 interval_time=None, timeout=None):
        """
        @summary: Waits for a listener to reach a desired status
        @param listener_id: The id of the listener
        @type listener_id: String
        @param desired_status: The desired final status of the listener
        @type desired_status: String
        @param interval_time: The amount of time in seconds to wait
            between polling
        @type interval_time: Integer
        @param interval_time: The amount of time in seconds to wait
            before aborting
        @type interval_time: Integer
        @return: Response object containing response and the listener
            domain object
        @rtype: requests.Response
        """
        kwargs = {'listener_id': listener_id,
                  'desired_status': desired_status,
                  'interval_time': interval_time,
                  'timeout': timeout}
        resp = self.wait_for_lbaas_object_status(
            lbaas_model_type=self.OBJECT_MODEL, **kwargs)
        return resp
