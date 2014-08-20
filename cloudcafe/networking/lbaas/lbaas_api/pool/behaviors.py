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


class PoolBehaviors(BaseLoadBalancersBehaviors):

    OBJECT_MODEL = 'pool'

    def __init__(self, pools_client, config):
        super(PoolBehaviors, self).__init__(
            lbaas_client_type=pools_client, config=config)

    def create_active_pool(
            self, name, tenant_id, protocol, lb_algorithm,
            description=None, session_persistence=None,
            pool_id=None, admin_state_up=None):
        """
        @summary: Creates a pool and waits for it to become active
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
        @param pool_id: ID of existing pool.
            Default: null
        @type pool_id: str
        @param admin_state_up: Enabled or disabled.
        @type admin_state_up: bool
        @return: Response object containing response and the pool
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'name': name, 'tenant_id': tenant_id, 'protocol': protocol,
                  'lb_algorithm': lb_algorithm, 'description': description,
                  'session_persistence': session_persistence,
                  'pool_id': pool_id,
                  'admin_state_up': admin_state_up}
        resp = self.create_active_lbaas_object(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def update_pool_and_wait_for_active(
            self, name=None, description=None,
            session_persistence=None, lb_algorithm=None,
            pool_id=None, admin_state_up=None):
        """
        @summary: Updates a pool and waits for it to become active
        @param name: Name of the Pool that will be created
        @type name: str
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
        @param pool_id: ID of existing pool.
            Default: null
        @type pool_id: str
        @param admin_state_up: Enabled or disabled.
        @type admin_state_up: bool
        @return: Response object containing response and the pool
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'name': name, 'description': description,
                  'session_persistence': session_persistence,
                  'lb_algorithm': lb_algorithm,
                  'pool_id': pool_id,
                  'admin_state_up': admin_state_up}
        resp = self.update_lbaas_object_and_wait_for_active(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def wait_for_pool_status(self, pool_id, desired_status,
                             interval_time=None, timeout=None):
        """
        @summary: Waits for a pool to reach a desired status
        @param pool_id: The id of the pool
        @type pool_id: String
        @param desired_status: The desired final status of the pool
        @type desired_status: String
        @param interval_time: The amount of time in seconds to wait
            between polling
        @type interval_time: Integer
        @param interval_time: The amount of time in seconds to wait
            before aborting
        @type interval_time: Integer
        @return: Response object containing response and the pool
            domain object
        @rtype: requests.Response
        """
        kwargs = {'pool_id': pool_id,
                  'desired_status': desired_status,
                  'interval_time': interval_time,
                  'timeout': timeout}
        resp = self.wait_for_lbaas_object_status(
            lbaas_model_type=self.OBJECT_MODEL, **kwargs)
        return resp
