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
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.common.constants import NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import ResourceBuildException


class NetworksBehaviors(NetworkingBaseBehaviors):

    def __init__(self, networks_client, networks_config, subnets_client,
                 subnets_config, ports_client, ports_config):
        super(NetworksBehaviors, self).__init__(
              networks_client, networks_config, subnets_client, subnets_config,
              ports_client, ports_config)
        self.config = networks_config
        self.client = networks_client

    def create_network(self, name=None, admin_state_up=None, shared=None,
                       tenant_id=None, resource_build_attempts=None,
                       raise_exception=True, use_exact_name=False):
        """
        @summary: Creates and verifies a Network is created as expected
        @param name: human readable name for the network, may not be unique
        @type name: string
        @param admin_state_up: true or false, the admin state of the network
        @type admin_stape_up: bool
        @param shared: specifies if the network can be accessed by any tenant
        @type shared: bool
        @param tenant_id: owner of the network
        @type tenant_id: string
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts: int
        @param raise_exception: flag to raise an exception if the
            Network was not created or to return None
        @type raise_exception: bool
        @param use_exact_name: flag if the exact name given should be used
        @type use_exact_name: bool
        @return: Network entity if created successful or None if not, and the
            raise_exception flag was set to False
        """
        if name is None:
            name = rand_name(self.config.starts_with_name)
        elif not(use_exact_name):
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

            err_msg = 'Network Create failure'
            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.CREATE_NETWORK, label=name,
                message=err_msg)

            if resp_check == 'OK':
                return resp.entity
            else:
                failures.append(resp_check)

        else:
            err_msg = (
                'Unable to create {0} network after {1} attempts: '
                '{2}').format(name, resource_build_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
