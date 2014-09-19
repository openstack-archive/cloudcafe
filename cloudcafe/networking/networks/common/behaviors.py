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

import requests
import time

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.networking.networks.common.config import NetworkingBaseConfig
from cloudcafe.networking.networks.common.exceptions \
    import UnsupportedTypeException, UnhandledMethodCaseException
from cloudcafe.networking.networks.common.models.response.network \
    import Network
from cloudcafe.networking.networks.common.models.response.port \
    import Port


class NetworkingBaseBehaviors(BaseBehavior):
    """Behaviors parent class

    To be inherited by all networks api behaviors and can be called for ex.

    net = NetworkingComposite()
    net.common.behaviors.wait_for_status(port, 'ACTIVE')

    or
    net.ports.behaviors.wait_for_status_status(port, 'ACTIVE')

    in this last call methods and config values will be overwritten if present
    in the ports config
    """

    def __init__(self, networks_client, networks_config, subnets_client,
                 subnets_config, ports_client, ports_config):
        super(NetworkingBaseBehaviors, self).__init__()
        self.config = NetworkingBaseConfig()
        self.networks_config = networks_config
        self.networks_client = networks_client
        self.subnets_client = subnets_client
        self.subnets_config = subnets_config
        self.ports_client = ports_client
        self.ports_config = ports_config

    def check_response(self, resp, status_code, label, message,
                       network_id=None):
        """
        @summary: Checks the API response object
        @param resp: API call response object
        @type resp: requests.models.Response
        @param status_code: HTTP expected response code
        @type status_code: int
        @param label: resource identifier like name, label, ID, etc.
        @type label: string
        @param message: error message like Network Get failure for ex.
        @type message: string
        @param network_id: related Network ID (optional)
        @type network_id: string
        @return: None if the response is the expected or the error message
        @rtype: None or string
        """
        response_msg = None
        if network_id:
            label = '{label} at network {network}'.format(
                label=label, network=network_id)

        resp_type = type(resp)
        if not resp_type == requests.models.Response:
            err_msg = ('{label} {message}: Unexpected response object '
                       'type {resp_type}').format(label=label, message=message,
                                                  resp_type=resp_type)
            self._log.error(err_msg)
            response_msg = err_msg

        elif resp.ok and resp.entity and resp.status_code == status_code:
            response_msg = None

        elif not resp.ok or resp.status_code != status_code:
            err_msg = ('{label} {message}: {status} {reason} '
                '{content}. Expected status code {expected_status}').format(
                label=label, message=message, status=resp.status_code,
                reason=resp.reason, content=resp.content,
                expected_status=status_code)
            self._log.error(err_msg)
            response_msg = err_msg
        elif not resp.entity:
            err_msg = ('{label} {message}: Unable to get response'
                       ' entity object').format(label=label, message=message)
            self._log.error(err_msg)
            response_msg = err_msg
        else:

            # This should NOT happen, scenarios should be covered by the elifs
            err_msg = 'Unhandled check response base behavior case'
            raise UnhandledMethodCaseException(err_msg)
        return response_msg

    def wait_for_status(self, resource_entity, new_status, timeout=None,
                       poll_rate=None):
        """
        @summary: Check a new status is reached by an entity object
        @param resource_entity: entity object like Network and Port
        @type resource_entity: Network or Port entity object (may be extended
            to other types with the status attribute)
        @param new_status: expected new status, like ACTIVE for ex.
        @type new_status: string
        @param timeout: seconds to wait for the new status
        @type timeout: int
        @param poll_rate: seconds between API calls
        @type poll_rate: int
        @return: True or False depending if the new status was reached
            within the expected timeout
        @rtype: bool
        """

        resource_type = type(resource_entity)

        # Subnets do NOT have a status attribute
        if resource_type == Network:
            client_call = self.networks_client.get_network
        elif resource_type == Port:
            client_call = self.ports_client.get_port
        else:
            msg = 'Entity type {0} NOT supported'.format(resource_type)
            raise UnsupportedTypeException(msg)

        entity_id = resource_entity.id
        initial_status = resource_entity.status
        timeout = timeout or self.config.resource_change_status_timeout
        poll_rate = poll_rate or self.config.api_poll_rate
        endtime = time.time() + int(timeout)

        log_msg = ('Checking {0} entity type initial {1} status is updated '
                   'to {2} status within a timeout of {3}').format(
                    resource_type, initial_status, new_status, timeout)
        self._log.info(log_msg)

        while time.time() < endtime:
            resp = client_call(entity_id)
            if resp.ok and resp.entity and resp.entity.status == new_status:
                return True
            time.sleep(poll_rate)
        return False


class NetworkingResponse(object):
    """
    @summary:
    @param response: response object for client calls done by behavior methods,
        can also be set to None (for ex. there was no entity obj.),
        True (for ex. the delete was successful) or False
    @type response: Requests.response, None or bool
    @param failures: list with error messages created by the check_response
        method. Empty list if no errors were found while checking the response
    @type failures: list
    """
    def __init__(self):
        self.response = None
        self.failures = list()
