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
from cloudcafe.networking.lbaas.lbaas_api.health_monitor.request \
    import CreateHealthMonitor, UpdateHealthMonitor
from cloudcafe.networking.lbaas.lbaas_api.health_monitor.response \
    import HealthMonitor, HealthMonitors


class HealthMonitorsClient(BaseLoadBalancersClient):
    """
    Health Monitor Client

    @summary: Health monitors describe the probes that are used to
        determine the health of pool members.
    """
    _HEALTH_MONITORS_URL = "{base_url}/healthmonitors"
    _HEALTH_MONITOR_URL = "{base_url}/healthmonitors/{health_monitor_id}"

    def create_health_monitor(self, type_, tenant_id, delay, timeout,
                              max_retries, http_method=None,
                              url_path=None, expected_codes=None,
                              admin_state_up=None, requestslib_kwargs=None):
        """Create Health Monitor
        @summary: Creates an instance of a health monitor given the
            provided parameters
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
        @return: Response Object containing response code and the
            health monitor domain object
        @rtype: Requests.response
        """
        full_url = self._HEALTH_MONITORS_URL.format(
            base_url=self.url)
        health_monitor_request_object = CreateHealthMonitor(
            type_=type_, tenant_id=tenant_id, delay=delay,
            timeout=timeout, max_retries=max_retries,
            http_method=http_method, url_path=url_path,
            expected_codes=expected_codes,
            admin_state_up=admin_state_up)

        return self.request('POST', full_url,
                            response_entity_type=HealthMonitor,
                            request_entity=health_monitor_request_object,
                            requestslib_kwargs=requestslib_kwargs)

    def list_health_monitors(self, requestslib_kwargs=None):
        """List Health Monitors
        @summary: List all health monitors configured for the account.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._HEALTH_MONITORS_URL.format(base_url=self.url)
        return self.request('GET', full_url,
                            response_entity_type=HealthMonitors,
                            requestslib_kwargs=requestslib_kwargs)

    def update_health_monitor(self, health_monitor_id, delay=None,
                              timeout=None, max_retries=None, http_method=None,
                              url_path=None, expected_codes=None,
                              admin_state_up=None, requestslib_kwargs=None):
        """Update Health Monitor
        @summary: Update the properties of a health monitor given the
            provided parameters
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
        @return: Response Object containing response code.
        @rtype: Requests.response
        """
        update_health_monitor = UpdateHealthMonitor(
            delay=delay, timeout=timeout, max_retries=max_retries,
            http_method=http_method, url_path=url_path,
            expected_codes=expected_codes, admin_state_up=admin_state_up)
        full_url = self._HEALTH_MONITOR_URL.format(
            base_url=self.url,
            health_monitor_id=health_monitor_id)
        return self.request('PUT', full_url,
                            request_entity=update_health_monitor,
                            response_entity_type=HealthMonitor,
                            requestslib_kwargs=requestslib_kwargs)

    def get_health_monitor(self, health_monitor_id, requestslib_kwargs=None):
        """Get Health Monitor Details
        @summary: List details of the specified health monitor.
        @param health_monitor_id: ID of the health monitor to get details from.
        @type health_monitor_id: str
        @return: Response Object containing response code and the
            health monitor domain object.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._HEALTH_MONITOR_URL.format(
            base_url=self.url,
            health_monitor_id=health_monitor_id)
        return self.request('GET', full_url,
                            response_entity_type=HealthMonitor,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_health_monitor(self, health_monitor_id,
                              requestslib_kwargs=None):
        """Delete Health Monitor
        @summary: Remove a health monitor from the account.
        @param health_monitor_id: ID of the health monitor to delete.
        @type health_monitor_id: str
        @return: Response Object containing response code.
        @rtype: Requests.response
        @note: Returns an error if it's still in use by any pools.
        """
        full_url = self._HEALTH_MONITOR_URL.format(
            base_url=self.url,
            health_monitor_id=health_monitor_id)
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)
