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
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.common.constants import NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import ResourceBuildException, NetworkIDMissingException, \
    InvalidIPException


class SubnetsBehaviors(NetworkingBaseBehaviors):

    def __init__(self, subnets_client, subnets_config, networks_client,
                 networks_config, ports_client, ports_config):
        super(SubnetsBehaviors, self).__init__(
              networks_client, networks_config, subnets_client, subnets_config,
              ports_client, ports_config)
        self.config = subnets_config
        self.client = subnets_client

    def verify_ip(self, ip_cidr, ip_range=None):
        """Verify if it is a valid CIDR or IP address
           within a range if given
        """

        try:
            res = IPy.IP(ip_cidr)

            # Check the IP/CIDR is within the range, if given
            if ip_range:
                if res not in IPy.IP(ip_range):
                    msg = '{0} not within {1} range'.format(ip_cidr, ip_range)
                    self._log.debug(msg)
                    return False
            return True
        except ValueError as e:
            self._log.error(e.message)
            return False

    def verify_private_ip(self, ip_cidr, ip_version, ip_range=None,
                           check_prefixlen=True):
        """Verify the IP/CIDR is of a private network"""
        if ip_range:
            ip_range = ip_range
        elif ip_version == 4:
            ip_range = self.config.private_ipv4_range
        elif ip_version == 6:
            ip_range = self.config.private_ipv6_range

        # This should not happen ip_version should be 4 or 6
        else:
            msg = 'Invalid IP version {0}'.format(ip_version)
            raise InvalidIPException(msg)

        ip_check = self.verify_ip(ip_cidr, ip_range)
        if check_prefixlen:
            prefixlen_check = self.verify_prefixlen(ip_cidr=ip_cidr,
                                                    ip_version=ip_version)
            return ip_check and prefixlen_check
        return ip_check

    def verify_prefixlen(self, ip_cidr, ip_version=4, suffix_max=None):
        """Verify an IP/CIDR is within the expected prefix length
           for ex. /12-/30 on IPv4 and /8-/64 on IPv6
        """

        # Valid IP/CIDR is expected starting at /12 for IPv4
        # and /8 for IPv6, if not a ValueError is raised and False returned
        try:
            prefix_length = int(IPy.IP(ip_cidr).prefixlen())
        except ValueError as e:
            self._log.error(e.message)
            return False

        # Default values are /30 for IPv4 and /64 for IPv6
        if suffix_max is None and ip_version == 4:
            suffix_max = self.config.ipv4_suffix_max
        elif suffix_max is None and ip_version == 6:
            suffix_max = self.config.ipv6_suffix_max

        suffix_max = int(suffix_max)
        if prefix_length <= suffix_max:
            return True
        else:
            msg = ('Unexpected prefix length of {prefix_length} for {ip_cidr},'
                   'expected value less than {suffix_max}').format(
                        prefix_length=prefix_length, ip_cidr=ip_cidr,
                        suffix_max=suffix_max)
            self._log.debug(msg)
            return False

    def create_ipv4_cidr(self, ipv4_suffix=None, ipv4_prefix=None):
        """Creates an IPv4 cidr with default and/or random values"""
        if ipv4_suffix is None:
            ipv4_suffix = self.config.ipv4_suffix
        if ipv4_prefix is None:
            ipv4_prefix = self.config.ipv4_prefix
        kwargs = dict()
        kwargs['mask'] = ipv4_suffix
        kwargs['ip_pattern'] = ipv4_prefix
        cidr = random_cidr(**kwargs)
        if self.verify_private_ip(ip_cidr=cidr, ip_version=4):
            return cidr
        else:
            msg = 'Invalid IPv4 cidr {0}'.format(cidr)
            raise InvalidIPException(msg)

    def create_ipv6_cidr(self, ipv6_suffix=None, ipv6_prefix=None):
        """Creates an IPv6 cidr with default or given values"""
        if ipv6_suffix is None:
            ipv6_suffix = self.config.ipv6_suffix
        if ipv6_prefix is None:
            ipv6_prefix = self.config.ipv6_prefix
        cidr = '{0}/{1}'.format(ipv6_prefix, ipv6_suffix)
        if self.verify_private_ip(ip_cidr=cidr, ip_version=6):
            return cidr
        else:
            msg = 'Invalid IPv6 cidr {0}'.format(cidr)
            raise InvalidIPException(msg)

    def create_subnet(self, network_id, ip_version=None, cidr=None, name=None,
                      tenant_id=None, gateway_ip=None, dns_nameservers=None,
                      allocation_pools=None, host_routes=None,
                      enable_dhcp=None, resource_build_attempts=None,
                      raise_exception=True, use_exact_name=False):
        """
        @summary: Creates and verifies a Subnet is created as expected
        @param name: human readable name for the subnet, may not be unique.
            (CRUD: CRU)
        @type name: string
        @param tenant_id: owner of the network. (CRUD: CR)
        @type tenant_id: string
        @param network_id: network subnet is associated with (CRUD: CR)
        @type network_id: string
        @param ip_version: IP version 4 or 6 (CRUD: CR)
        @type ip_version: int
        @param cidr: represents IP range for the subnet and should be in the
            form <network_address>/<prefix> (CRUD: CR)
        @type cidr: string
        @param gateway_ip: default gateway used by devices in the subnet
            (CRUD: CRUD)
        @type gateway_ip: string
        @param dns_nameservers: DNS name servers used by subnet hosts
            (CRUD: CRU)
        @type dns_nameservers: list(str)
        @param allocation_pools: sub range of cidr available for dynamic
            allocation to ports (CRUD: CR)
        @type allocation_pools: list(dict)
        @param host_routes: routes that should be used by devices with IPs from
            this subnet (does not includes the local route, CRUD: CRU)
        @type host_routes: list(dict)
        @param enable_dhcp: whether DHCP is enabled (CRUD:CRU)
        @type enable_dhcp: bool
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts:int
        @param raise_exception: flag to raise an exception if the Subnet was
            not created or to return None
        @type raise_exception: bool
        @param use_exact_name: flag if the exact name given should be used
        @type use_exact_name: bool
        @return: Subnet entity and failure list if created successful, or
            None and the failure list if the raise_exception flag was False
        @rtype: tuple with Subnet or None and failure list (may be empty)
        """
        if network_id is None:
            raise NetworkIDMissingException
        if cidr:
            if self.verify_ip(cidr):
                ip_version = IPy.IP(cidr).version()
            else:
                raise InvalidIPException
        else:
            if ip_version == 6:
                cidr = self.create_ipv6_cidr()
            else:
                # Setting the default create version to 4 if not given
                ip_version = 4
                cidr = self.create_ipv4_cidr()

        if name is None:
            name = rand_name(self.config.starts_with_name)
        elif not(use_exact_name):
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

            err_msg = 'Subnet Create failure'
            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.CREATE_SUBNET, label=name,
                message=err_msg, network_id=network_id)

            if resp_check == 'OK':
                return (resp.entity, failures)
            else:
                failures.append(resp_check)

        else:
            err_msg = (
                'Unable to create {0} subnet after {1} attempts: '
                '{2}').format(name, resource_build_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            else:
                return (None, failures)
