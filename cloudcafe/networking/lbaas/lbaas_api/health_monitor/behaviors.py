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


class HealthMonitorBehaviors(BaseLoadBalancersBehaviors):

    OBJECT_MODEL = 'health_monitor'

    def __init__(self, health_monitors_client, config):
        super(HealthMonitorBehaviors, self).__init__(
            lbaas_client_type=health_monitors_client, config=config)

    def create_active_health_monitor(
            self, type_, tenant_id, delay, timeout, max_retries,
            http_method=None, url_path=None, expected_codes=None,
            admin_state_up=None):
        """
        @summary: Creates a health monitor and waits for it to become active
        @param type_: Protocol used for health monitor.
            e.g., HTTP, HTTPS, TCP, PING
        @type type_: str
        @param tenant_id: Tenant that owns the health monitor.
        @type tenant_id: str
        @param delay: Time in seconds between probes.
        @type delay: int
        @param timeout: Time in seconds to timeout each probe.
        @type timeout: int
        @param max_retries: Maximum consecutive health probe tries.
        @type max_retries: int
        @param http_method: HTTP method monitor uses to make request.
            Default: "GET"
        @type http_method: str
        @param url_path: Path portion of URI that will be probed if
            type is HTTP(S).
                Default: "/"
        @type url_path: str
        @param expected_codes: Expected HTTP codes for a passing HTTP(S).
            Default: "200"
        @type expected_codes: str
        @param admin_state_up: Enabled or Disabled
            Default: "true"
        @type admin_state_up: bool
        @return: Response object containing response and the health monitor
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'type_': type_, 'tenant_id': tenant_id, 'delay': delay,
                  'timeout': timeout, 'max_retries': max_retries,
                  'http_method': http_method, 'url_path': url_path,
                  'expected_codes': expected_codes,
                  'admin_state_up': admin_state_up}
        resp = self.create_active_lbaas_object(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def update_health_monitor_and_wait_for_active(
            self, health_monitor_id, delay=None,
            timeout=None, max_retries=None, http_method=None,
            url_path=None, expected_codes=None,
            admin_state_up=None):
        """
        @summary: Updates a health monitor and waits for it to become active
        @param health_monitor_id: ID of the health monitor to update.
        @type health_monitor_id: str
        @param delay: Time in seconds between probes.
        @type delay: int
        @param timeout: Time in seconds to timeout each probe.
        @type timeout: int
        @param max_retries: Maximum consecutive health probe tries.
        @type max_retries: int
        @param http_method: HTTP method monitor uses to make request.
            Default: "GET"
        @type http_method: str
        @param url_path: Path portion of URI that will be probed if
            type is HTTP(S).
                Default: "/"
        @type url_path: str
        @param expected_codes: Expected HTTP codes for a passing HTTP(S).
            Default: "200"
        @type expected_codes: str
        @param admin_state_up: Enabled or Disabled
            Default: "true"
        @type admin_state_up: bool
        @return: Response object containing response and the health monitor
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'health_monitor_id': health_monitor_id,
                  'delay': delay, 'timeout': timeout,
                  'max_retries': max_retries, 'http_method': http_method,
                  'url_path': url_path, 'expected_codes': expected_codes,
                  'admin_state_up': admin_state_up}
        resp = self.update_lbaas_object_and_wait_for_active(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def wait_for_health_monitor_status(self, health_monitor_id, desired_status,
                                       interval_time=None, timeout=None):
        """
        @summary: Waits for a health monitor to reach a desired status
        @param health_monitor_id: The id of the health monitor
        @type health_monitor_id: String
        @param desired_status: The desired final status of the health monitor
        @type desired_status: String
        @param interval_time: The amount of time in seconds to wait
            between polling
        @type interval_time: Integer
        @param interval_time: The amount of time in seconds to wait
            before aborting
        @type interval_time: Integer
        @return: Response object containing response and the health monitor
            domain object
        @rtype: requests.Response
        """
        kwargs = {'health_monitor_id': health_monitor_id,
                  'desired_status': desired_status,
                  'interval_time': interval_time,
                  'timeout': timeout}
        resp = self.wait_for_lbaas_object_status(
            lbaas_model_type=self.OBJECT_MODEL, **kwargs)
        return resp
