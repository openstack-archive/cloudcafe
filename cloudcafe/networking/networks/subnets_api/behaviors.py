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

import IPy

from cloudcafe.common.tools.datagen import rand_name, random_cidr
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors, NetworkingResponse
from cloudcafe.networking.networks.common.constants \
    import NeutronResponseCodes
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
        """
        @summary: Verify if it is a valid CIDR or IP address within an
            IP range if given.
        @param ip_cidr: IP or CIDR to verify
        @type ip_cidr: string
        @param ip_range: IP or CIDR is expected to be within this range.
            For ex. 10.0.0.0/8, 172.16.0.0/12 or 192.168.0.0/16 for valid
            private IPv4 ranges or fd00::/8 for valid private IPv6 range
        @type ip_range: string
        @return: True if it is a valid IP (or CIDR) or False if not
        @rtype: bool
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
                          check_prefixlen=True, suffix_max=None):
        """
        @summary: Verify the IP or CIDR is of a private network
        @param ip_cidr: IP or CIDR to verify
        @type ip_cidr: string
        @param ip_version: IP version 4 or 6
        @type ip_version: int
        @param ip_range: IP or CIDR is expected to be within this range.
            For ex. 10.0.0.0/8, 172.16.0.0/12 or 192.168.0.0/16 for valid
            private IPv4 ranges or fd00::/8 for valid private IPv6 range
        @type ip_range: string
        @param check_prefixlen: flag to check or not the IP/CIDR prefix length
        @type check_prefixlen: bool
        @param suffix_max: if the check prefixlen flag set this is the prefix
            that the IP or CIDR should be less or equal than
        @type suffix_max: int
        @return: True if it is a valid private IP (or CIDR) or False if not
        @rtype: bool
        """
        if ip_version == 4:
            ip_range = ip_range or self.config.private_ipv4_range
            suffix_max = suffix_max or self.config.ipv4_suffix_max
        elif ip_version == 6:
            ip_range = ip_range or self.config.private_ipv6_range
            suffix_max = suffix_max or self.config.ipv6_suffix_max

        # This should not happen ip_version should be 4 or 6
        else:
            msg = 'Invalid IP version {0}'.format(ip_version)
            raise InvalidIPException(msg)

        ip_check = self.verify_ip(ip_cidr, ip_range)
        if check_prefixlen:
            prefixlen_check = self.verify_prefixlen(
                ip_cidr=ip_cidr, suffix_max=suffix_max)
            return ip_check and prefixlen_check
        return ip_check

    def verify_prefixlen(self, ip_cidr, suffix_max):
        """
        @summary: Verify an IP or CIDR is within the expected prefix length,
            for an IP this should be 32, for CIDRs it can be /12-/30 on IPv4
            and /8-/64 on IPv6
        @param ip_cidr: IP or CIDR to verify
        @type ip_cidr: string
        @param suffix_max: the prefix that the IP or CIDR should be less or
            equal than
        @type suffix_max: int
        @return: True/False if the IP or CIDR has the expected prefix length
        @rtype: bool
        """

        # Valid CIDR is expected starting at /12 for IPv4
        # and /8 for IPv6, if not a ValueError is raised and False returned
        try:
            prefix_length = IPy.IP(ip_cidr).prefixlen()
        except ValueError as e:
            self._log.error(e.message)
            return False

        # Default values are /32 for an IP and for CIDRs /30 for IPv4 and
        # /64 for IPv6
        suffix_max = int(suffix_max)
        if prefix_length <= suffix_max:
            return True
        else:
            msg = ('Unexpected prefix length of {prefix_length} for {ip_cidr},'
                   'expected value less or equal than {suffix_max}').format(
                       prefix_length=prefix_length, ip_cidr=ip_cidr,
                       suffix_max=suffix_max)
            self._log.debug(msg)
            return False

    def create_ipv4_cidr(self, ipv4_suffix=None, ipv4_prefix=None,
                         ip_range=None, suffix_max=None):
        """
        @summary: Creates an IPv4 cidr with given or default values
        @param ipv4_suffix: the CIDR suffix, by default 24
        @type ipv4_suffix: int
        @param ipv4_prefix: the CIDR prefix, can have * for random numbers
            between 1 and 254, by default 192.168.*.0
        @type ipv4_prefix: string
        @param ip_range: CIDR is expected to be within this range, by default
            192.168.0.0/16 for the private IPv4 range
        @type ip_range: string
        @param suffix_max: the prefix that the CIDR should be less or
            equal than, by default 30
        @return: an IPv4 CIDR
        @rtype: string
        """
        ipv4_suffix = ipv4_suffix or self.config.ipv4_suffix
        ipv4_prefix = ipv4_prefix or self.config.ipv4_prefix

        kwargs = {'mask': ipv4_suffix, 'ip_pattern': ipv4_prefix}
        cidr = random_cidr(**kwargs)
        if self.verify_private_ip(ip_cidr=cidr, ip_version=4,
                                  ip_range=ip_range, suffix_max=suffix_max):
            return cidr
        else:
            msg = 'Invalid IPv4 cidr {0}'.format(cidr)
            raise InvalidIPException(msg)

    def create_ipv6_cidr(self, ipv6_suffix=None, ipv6_prefix=None,
                         ip_range=None, suffix_max=None):
        """
        @summary: Creates an IPv6 cidr with given or default values
        @param ipv6_suffix: the CIDR suffix, by default 64
        @type ipv6_suffix: int
        @param ipv6_prefix: the CIDR prefix, by default fd00::
        @type ipv6_prefix: string
        @param ip_range: CIDR is expected to be within this range, by default
            fd00::/8 for the private IPv6 range
        @type ip_range: string
        @param suffix_max: the prefix that the CIDR should be less or
            equal than, by default 64
        @return: an IPv6 CIDR
        @rtype: string
        """
        ipv6_suffix = ipv6_suffix or self.config.ipv6_suffix
        ipv6_prefix = ipv6_prefix or self.config.ipv6_prefix

        cidr = '{0}/{1}'.format(ipv6_prefix, ipv6_suffix)
        if self.verify_private_ip(ip_cidr=cidr, ip_version=6,
                                  ip_range=ip_range, suffix_max=suffix_max):
            return cidr
        else:
            msg = 'Invalid IPv6 cidr {0}'.format(cidr)
            raise InvalidIPException(msg)

    def create_subnet(self, network_id, ip_version=None, cidr=None, name=None,
                      tenant_id=None, gateway_ip=None, dns_nameservers=None,
                      allocation_pools=None, host_routes=None,
                      enable_dhcp=None, resource_build_attempts=None,
                      raise_exception=True, use_exact_name=False,
                      poll_interval=None):
        """
        @summary: Creates and verifies a Subnet is created as expected
        @param name: human readable name for the subnet, may not be unique.
            (CRUD: CRU)
        @type name: string
        @param tenant_id: owner of the network. (CRUD: CR)
        @type tenant_id: string
        @param network_id: network subnet is associated with (CRUD: CR)
        @type network_id: string
        @param ip_version: IP version 4 or 6 (CRUD: CR), if the CIDR is given
            this is optional and the CIDR one will be taken
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
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: Subnet entity and failure list if created successful, or
            None and the failure list if the raise_exception flag was False
        @rtype: tuple with Subnet or None and failure list (may be empty)
        """
        if not network_id:
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
        elif not use_exact_name:
            name = rand_name(name)

        poll_interval = poll_interval or self.config.api_poll_interval
        resource_build_attempts = (resource_build_attempts or
            self.config.api_retries)

        failures = []
        result = NetworkingResponse()
        err_msg = 'Subnet Create failure'
        for attempt in range(resource_build_attempts):
            self._log.debug('Attempt {0} of {1} building subnet {2}'.format(
                attempt + 1, resource_build_attempts, name))

            resp = self.client.create_subnet(
                network_id=network_id, ip_version=ip_version, cidr=cidr,
                name=name, tenant_id=tenant_id, gateway_ip=gateway_ip,
                dns_nameservers=dns_nameservers,
                allocation_pools=allocation_pools, host_routes=host_routes,
                enable_dhcp=enable_dhcp)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.CREATE_SUBNET, label=name,
                message=err_msg, network_id=network_id)

            if not resp_check:
                result.response = resp
                result.failures = failures
                return result
            failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to create {0} subnet after {1} attempts: '
                '{2}').format(name, resource_build_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            result.failures = failures
            return result
