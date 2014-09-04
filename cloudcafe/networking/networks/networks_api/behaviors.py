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

from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.networking.networks.behaviors import NetworksBehaviors
from cloudcafe.networking.networks.common.constants import HTTPStatusCodes
from cloudcafe.networking.networks.common.exceptions \
    import ResourceBuildException


class NetworksAPIBehaviors(NetworksBehaviors):

    def __init__(self, networks_client, networks_config, subnets_client,
                 subnets_config, ports_client, ports_config):
        super(NetworksAPIBehaviors, self).__init__(
              networks_client, networks_config, subnets_client, subnets_config,
              ports_client, ports_config)
        self.config = networks_config
        self.client = networks_client

    def create_network(self, name=None, admin_state_up=None, shared=None,
                       tenant_id=None, resource_build_attempts=None,
                       raise_exception=True):
        """
        @summary: Creates and verifies a Network is created as expected
        @param string name: human readable name for the network,
            may not be unique
        @param bool admin_state_up: true or false, the admin state
            of the network
        @param bool shared: specifies if the network can be accessed by any
            tenant
        @param string tenant_id: owner of the network
        @param int resource_build_attempts: number of API retries
        @param bool raise_exception: flag to raise an exception if the
            Network was not created or to return None
        @return: Network entity if created successful or None if not, and the
            raise_exception flag was set to False
        """
        if name is None:
            name = rand_name(self.config.starts_with_name)
        else:
            name = rand_name(name)

        if resource_build_attempts is None:
            resource_build_attempts = self.config.resource_build_attempts

        failures = []
        for attempt in range(resource_build_attempts):
            self._log.debug('Attempt {0} of {1} building network {2}'.format(
                attempt + 1, resource_build_attempts, name))

            resp = self.client.create_network(
                name=name, admin_state_up=admin_state_up, shared=shared,
                tenant_id=tenant_id)

            if (resp.ok and resp.entity and
                resp.status_code == HTTPStatusCodes.CREATE_NETWORK):
                return resp.entity

            if (not resp.ok or
                resp.status_code != HTTPStatusCodes.CREATE_NETWORK):
                msg_ok = '{0} Network Create failure {1} {2} {3}'.format(
                    name, resp.status_code, resp.reason, resp.content)
                self._log.error(msg_ok)
                failures.append(msg_ok)
            elif not resp.entity:
                msg_entity = ('Unable to get {0} network create'
                              ' response entity object').format(name)
                self._log.error(msg_entity)
                failures.append(msg_entity)

        else:
            if raise_exception:
                err_msg = (
                    'Unable to create {0} network after {1} attempts: {2}'). \
                    format(name, resource_build_attempts, failures)
                raise ResourceBuildException(err_msg)
            else:
                return None
