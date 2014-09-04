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
    import ResourceBuildException, NetworkIDMissingException


class PortsAPIBehaviors(NetworksBehaviors):

    def __init__(self, ports_client, ports_config, networks_client,
                 networks_config, subnets_client, subnets_config):
        super(PortsAPIBehaviors, self).__init__(
              networks_client, networks_config, subnets_client, subnets_config,
              ports_client, ports_config)
        self.config = ports_config
        self.client = ports_client

    def create_port(self, network_id, name=None, admin_state_up=None,
                    mac_address=None, fixed_ips=None, device_id=None,
                    device_owner=None, tenant_id=None, security_groups=None,
                    resource_build_attempts=None, raise_exception=True):
        """
        @summary: Creates and verifies a Port is created as expected
        @param string network_id: network port is associated with (CRUD: CR)
        @param string name: human readable name for the port,
            may not be unique. (CRUD: CRU)
        @param bool admin_state_up: true or false (default true),
            the admin state of the port. If down, the port does not forward
            packets (CRUD: CRU)
        @param string mac_address: mac address to use on the port (CRUD: CR)
        @param list(dict) fixed_ips: ip addresses for the port associating the
            port with the subnets where the IPs come from (CRUD: CRU)
        @param string device_id: id of device using this port (CRUD: CRUD)
        @param string device_owner: entity using this port (ex. dhcp agent,
            CRUD: CRUD)
        @param string tenant_id: owner of the port (CRUD: CR)
        @param list(dict) security_groups: ids of any security groups
            associated with the port (CRUD: CRUD)
        @param int resource_build_attempts: number of API retries
        @param bool raise_exception: flag to raise an exception if the
            Port was not created or to return None
        @return: Port entity if created successful or None if not, and the
            raise_exception flag was set to False
        """
        if network_id is None:
            raise NetworkIDMissingException

        if name is None:
            name = rand_name(self.config.starts_with_name)
        else:
            name = rand_name(name)

        if resource_build_attempts is None:
            resource_build_attempts = self.config.resource_build_attempts

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

            if (resp.ok and resp.entity and
                resp.status_code == HTTPStatusCodes.CREATE_PORT):
                return resp.entity

            if (not resp.ok or
                resp.status_code != HTTPStatusCodes.CREATE_PORT):
                msg_ok = '{0} Port Create failure {1} {2} {3}'.format(
                    name, resp.status_code, resp.reason, resp.content)
                self._log.error(msg_ok)
                failures.append(msg_ok)
            elif not resp.entity:
                msg_entity = ('Unable to get {0} port create'
                              ' response entity object').format(name)
                self._log.error(msg_entity)
                failures.append(msg_entity)

        else:
            if raise_exception:
                err_msg = (
                    'Unable to create {0} port after {1} attempts: {2}'). \
                    format(name, resource_build_attempts, failures)
                raise ResourceBuildException(err_msg)
            else:
                return None
