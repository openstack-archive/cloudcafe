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
from cloudcafe.networking.networks.common.constants \
    import NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import ResourceBuildException, NetworkIDMissingException


class PortsBehaviors(NetworkingBaseBehaviors):

    def __init__(self, ports_client, ports_config, networks_client,
                 networks_config, subnets_client, subnets_config):
        super(PortsBehaviors, self).__init__(
              networks_client, networks_config, subnets_client, subnets_config,
              ports_client, ports_config)
        self.config = ports_config
        self.client = ports_client

    def create_port(self, network_id, name=None, admin_state_up=None,
                    mac_address=None, fixed_ips=None, device_id=None,
                    device_owner=None, tenant_id=None, security_groups=None,
                    resource_build_attempts=None, raise_exception=True,
                    use_exact_name=False):
        """
        @summary: Creates and verifies a Port is created as expected
        @param network_id: network port is associated with (CRUD: CR)
        @type network_id: string
        @param name: human readable name for the port, may not be unique.
            (CRUD: CRU)
        @type name: string
        @param admin_state_up: true or false (default true), the admin state
            of the port. If down, the port does not forward packets (CRUD: CRU)
        @type admin_state_up: bool
        @param mac_address: mac address to use on the port (CRUD: CR)
        @type mac_address: string
        @param fixed_ips: ip addresses for the port associating the
            port with the subnets where the IPs come from (CRUD: CRU)
        @type fixed_ips: list(dict)
        @param device_id: id of device using this port (CRUD: CRUD)
        @type device_id: string
        @param device_owner: entity using this port (ex. dhcp agent,CRUD: CRUD)
        @type device_owner: string
        @param tenant_id: owner of the port (CRUD: CR)
        @type tenant_id: string
        @param security_groups: ids of any security groups associated with the
            port (CRUD: CRUD)
        @type security_groups: list(dict)
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts: int
        @param raise_exception: flag to raise an exception if the Port was not
            created or to return None
        @type raise_exception: bool
        @param use_exact_name: flag if the exact name given should be used
        @type use_exact_name: bool
        @return: Port entity if created successful and the failure list, or
            None and the failure list if the raise_exception flag was False
        @rtype: tuple with Port or None and failure list (may be empty)
        """
        if not network_id:
            raise NetworkIDMissingException

        if name is None:
            name = rand_name(self.config.starts_with_name)
        elif not use_exact_name:
            name = rand_name(name)

        resource_build_attempts = (resource_build_attempts or
            self.config.resource_build_attempts)

        failures = []
        for attempt in range(resource_build_attempts):
            self._log.debug('Attempt {0} of {1} building port {2}'.format(
                attempt + 1, resource_build_attempts, name))

            resp = self.client.create_port(
                network_id=network_id, name=name,
                admin_state_up=admin_state_up, mac_address=mac_address,
                fixed_ips=fixed_ips, device_id=device_id,
                device_owner=device_owner, tenant_id=tenant_id,
                security_groups=security_groups)

            err_msg = 'Port Create failure'
            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.CREATE_PORT, label=name,
                message=err_msg, network_id=network_id)

            # Failures will be an empty list if the create was successful the
            # first time
            if not resp_check:
                return (resp.entity, failures)
            else:
                failures.append(resp_check)

        else:
            err_msg = (
                'Unable to create {0} port after {1} attempts: '
                '{2}').format(name, resource_build_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            return (None, failures)
