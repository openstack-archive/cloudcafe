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

import IPy

from cloudcafe.common.tools.datagen import rand_name, random_cidr
from cloudcafe.networking.networks.behaviors import NetworksBehaviors
from cloudcafe.networking.networks.common.constants import HTTPStatusCodes
from cloudcafe.networking.networks.common.exceptions \
    import ResourceBuildException, NetworkIDMissingException, \
    InvalidIPException


class SubnetsAPIBehaviors(NetworksBehaviors):

    def __init__(self, subnets_client, subnets_config, networks_client,
                 networks_config, ports_client, ports_config):
        super(SubnetsAPIBehaviors, self).__init__(
              networks_client, networks_config, subnets_client, subnets_config,
              ports_client, ports_config)
        self.config = subnets_config
        self.client = subnets_client

    def verify_ip(self, cidr):
        """Verify if it is a valid IP address"""
        try:
            IPy.IP(cidr)
            return True
        except ValueError as e:
            self._log.error(e.message)
            return False

    def create_ipv4_cidr(self, ipv4_suffix='24', ipv4_prefix='192.168.*.0'):
        """Creates an IPv4 cidr with default and/or random values"""
        kwargs = dict()
        kwargs['mask'] = ipv4_suffix
        kwargs['ip_pattern'] = ipv4_prefix
        cidr = random_cidr(**kwargs)
        if self.verify_ip(cidr):
            return cidr
        else:
            msg = 'Invalid IPv4 cidr {0}'.format(cidr)
            raise InvalidIPException(msg)

    def create_ipv6_cidr(self, ipv6_suffix='64', ipv6_prefix='fc00::'):
        """Creates an IPv6 cidr with default or given values"""
        cidr = '{0}/{1}'.format(ipv6_prefix, ipv6_suffix)
        if self.verify_ip(cidr):
            return cidr
        else:
            msg = 'Invalid IPv6 cidr {0}'.format(cidr)
            raise InvalidIPException(msg)

    def create_subnet(self, network_id, ip_version=None, cidr=None, name=None,
                      tenant_id=None, gateway_ip=None, dns_nameservers=None,
                      allocation_pools=None, host_routes=None,
                      enable_dhcp=None, resource_build_attempts=None,
                      raise_exception=True):
        """
        @summary: Creates and verifies a Subnet is created as expected
        @param string name: human readable name for the subnet,
            may not be unique. (CRUD: CRU)
        @param string tenant_id: owner of the network. (CRUD: CR)
        @param string network_id: network subnet is associated with (CRUD: CR)
        @param int ip_version: IP version 4 or 6 (CRUD: CR)
        @param string cidr: represents IP range for the subnet and should be in
            the form <network_address>/<prefix> (CRUD: CR)
        @param string gateway_ip: default gateway used by devices in the subnet
            (CRUD: CRUD)
        @param list(str) dns_nameservers: DNS name servers used by subnet hosts
            (CRUD: CRU)
        @param list(dict) allocation_pools: sub range of cidr available for
            dynamic allocation to ports (CRUD: CR)
        @param list(dict) host_routes: routes that should be used by devices
            with IPs from this subnet (does not includes the local route,
            CRUD: CRU)
        @param bool enable_dhcp: whether DHCP is enabled (CRUD:CRU)
        @param int resource_build_attempts: number of API retries
        @param bool raise_exception: flag to raise an exception if the
            Subnet was not created or to return None
        @return: Subnet entity if created successful or None if not, and the
            raise_exception flag was set to False
        """
        if network_id is None:
            raise NetworkIDMissingException
        if ip_version is None and cidr is None:
            # Setting the default create version to 4
            ip_version = 4
            cidr = self.create_ipv4_cidr()
        elif ip_version == 4 and cidr is None:
            cidr = self.create_ipv4_cidr()
        elif ip_version == 6 and cidr is None:
            cidr = self.create_ipv6_cidr()
        elif ip_version is None and cidr:
            if self.verify_ip(cidr):
                ip_version = IPy.IP(cidr).version()
            else:
                raise InvalidIPException

        if name is None:
            name = rand_name(self.config.starts_with_name)
        else:
            name = rand_name(name)

        if resource_build_attempts is None:
            resource_build_attempts = self.config.resource_build_attempts

        failures = []
        for attempt in range(resource_build_attempts):
            self._log.debug('Attempt {0} of {1} building subnet {2}'.format(
                attempt + 1, resource_build_attempts, name))

            resp = self.client.create_subnet(
                network_id=network_id, ip_version=ip_version, cidr=cidr,
                name=name, tenant_id=tenant_id, gateway_ip=gateway_ip,
                dns_nameservers=dns_nameservers,
                allocation_pools=allocation_pools, host_routes=host_routes,
                enable_dhcp=enable_dhcp)

            if (resp.ok and resp.entity and
                resp.status_code == HTTPStatusCodes.CREATE_SUBNET):
                return resp.entity

            if (not resp.ok or
                resp.status_code != HTTPStatusCodes.CREATE_SUBNET):
                msg_ok = '{0} Subnet Create failure {1} {2} {3}'.format(
                    name, resp.status_code, resp.reason, resp.content)
                self._log.error(msg_ok)
                failures.append(msg_ok)
            elif not resp.entity:
                msg_entity = ('Unable to get {0} subnet create'
                              ' response entity object').format(name)
                self._log.error(msg_entity)
                failures.append(msg_entity)

        else:
            if raise_exception:
                err_msg = (
                    'Unable to create {0} subnet after {1} attempts: {2}'). \
                    format(name, resource_build_attempts, failures)
                raise ResourceBuildException(err_msg)
            else:
                return None
