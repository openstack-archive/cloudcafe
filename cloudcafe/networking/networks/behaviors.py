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

import time

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.networking.networks.common.exceptions \
    import UnsupportedTypeException
from cloudcafe.networking.networks.common.models.response.network \
    import Network
from cloudcafe.networking.networks.common.models.response.port \
    import Port
from cloudcafe.networking.networks.config import NetworksConfig


class NetworksBehaviors(BaseBehavior):
    """Behaviors parent class

    To be inherited by all networks api behaviors and can be called for ex.

    nets = NetworksComposite()
    nets.behaviors.updated_status(p, 'ACTIVE')

    or
    nets.ports.behaviors.updated_status(p, 'ACTIVE')

    in this last call methods and config values, if present in the ports api,
    will be overwritten and used instead of the main ones
    """

    def __init__(self, networks_client, networks_config, subnets_client,
                 subnets_config, ports_client, ports_config):
        super(NetworksBehaviors, self).__init__()
        self.config = NetworksConfig()
        self.networks_config = networks_config
        self.networks_client = networks_client
        self.subnets_client = subnets_client
        self.subnets_config = subnets_config
        self.ports_client = ports_client
        self.ports_config = ports_config

    def updated_status(self, resource_entity, new_status, timeout=None,
                       poll_rate=None):
        """
        @summary: Check a new status is reached by an entity object
        @param entity resource_entity: entity object like Network and Port
        @param string new_status: expected new status, like ACTIVE for ex.
        @param int timeout: seconds to wait for the new status
        @param int poll_rate: seconds between API calls
        @return: bool True or False depending if the new status was reached
            within the expected timeout
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
        else:
            return False
