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

import random
import time

import IPy
import netaddr


from cloudcafe.common.tools.datagen import rand_name, random_cidr
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors, NetworkingResponse
from cloudcafe.networking.networks.common.constants \
    import NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import InvalidIPException, NetworkIDMissingException,\
    ResourceBuildException, ResourceDeleteException, ResourceGetException,\
    ResourceListException, ResourceUpdateException


class SubnetsBehaviors(NetworkingBaseBehaviors):

    def __init__(self, subnets_client, subnets_config):
        super(SubnetsBehaviors, self).__init__()
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
                         ip_range=None, suffix_max=None, randomize=True):
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
        @type suffix_max: int
        @param randomize: randomize 32 bits of the 40-bit global identifier in
            the routing prefix to prevent collisions when two private networks
            are interconnected
        @type randomize: bool
        @return: an IPv6 CIDR
        @rtype: string
        """
        ipv6_suffix = ipv6_suffix or self.config.ipv6_suffix
        ipv6_prefix = ipv6_prefix or self.config.ipv6_prefix

        if randomize:
            b1 = random.getrandbits(16)
            b2 = random.getrandbits(16)
            prefix_dual_octets = ipv6_prefix.split(':')
            prefix_dual_octets[1] = '{:x}'.format(b1)
            prefix_dual_octets[2] = '{:x}'.format(b2)
            ipv6_prefix = '{0}::'.format(':'.join(prefix_dual_octets))

            # To be used with /64 IPv6 networks, overwriting suffix if other
            if ipv6_suffix != 64:
                msg = ('Subnet create_ipv6_cidr behavior method using '
                       'default 64 suffix instead of {0} when creating a '
                       'random cidr').format(ipv6_suffix)
                self._log.info(msg)
                ipv6_suffix = 64

        cidr = '{0}/{1}'.format(ipv6_prefix, ipv6_suffix)
        if self.verify_private_ip(ip_cidr=cidr, ip_version=6,
                                  ip_range=ip_range, suffix_max=suffix_max):
            return cidr
        else:
            msg = 'Invalid IPv6 cidr {0}'.format(cidr)
            raise InvalidIPException(msg)

    def get_random_ip(self, cidr):
        """
        @summary: gets a random IP address within a CIDR excluding first and
            last IPs
        @param cidr: represents IP range to get the IP from and should be in
            the form <network_address>/<prefix>
        @type cidr: string
        @return: IP address
        @rtype: string
       """
        if not self.verify_ip(cidr):
            msg = 'Invalid CIDR {0}'.format(cidr)
            raise InvalidIPException(msg)

        net = netaddr.IPNetwork(cidr)
        increment = random.randint(1, net.size - 2)
        ip = str(netaddr.IPAddress(net.first + int(increment)))

        return ip

    def get_next_ip(self, cidr, num=0):
        """
        @summary: gets the IP address of a CIDR starting at the first IP
        @param cidr: represents IP range to get the IP from and should be in
            the form <network_address>/<prefix>
        @type cidr: string
        @param num: number of places from the first IP of the CIDR
        @type num: int
        @return: IP address
        @rtype: string
       """
        if not self.verify_ip(cidr):
            msg = 'Invalid CIDR {0}'.format(cidr)
            raise InvalidIPException(msg)

        net = netaddr.IPNetwork(cidr)

        if num < net.size and num >= 0:
            ip = str(netaddr.IPAddress(net.first + int(num)))
        else:
            msg = ('Invalid next value. Expected value greater than 0 and less'
                   ' than the network size of {0}').format(net.size)
            raise InvalidIPException(msg)

        return ip

    def get_previous_ip(self, cidr, num=0):
        """
        @summary: gets an IP address within a CIDR from the last IP
        @param cidr: represents IP range to get the IP from and should be in
            the form <network_address>/<prefix>
        @type cidr: string
        @param num: number of places from the last IP of the CIDR
        @type num: int
        @return: IP address
        @rtype: string
       """

        if not self.verify_ip(cidr):
            msg = 'Invalid CIDR {0}'.format(cidr)
            raise InvalidIPException(msg)

        net = netaddr.IPNetwork(cidr)

        if num < net.size and num >= 0:
            ip = str(netaddr.IPAddress(net.last - int(num)))
        else:
            msg = ('Invalid next value. Expected value greater than 0 and less'
                   ' than the network size of {0}').format(net.size)
            raise InvalidIPException(msg)

        return ip

    def get_ips(self, cidr, num=1):
        """
        @summary: get n random IPs within a cidr
        @param cidr: represents IP range to get the IPs from and should be in
            the form <network_address>/<prefix>
        @type cidr: string
        @param num: number of IPs to get
        @type num: int
        @return: IP list
        @rtype: list
        """
        ips = [self.get_random_ip(cidr) for x in range(num)]
        return ips

    def get_fixed_ip(self, subnet_id, cidr, num=1):
        """
        @summary: gets a Subnet fixed IP
        @param subnet_id: Subnet ID
        @type subnet_id: string
        @param cidr: represents IP range to get the IP from and should be in
            the form <network_address>/<prefix>
        @type cidr: string
        @param num: number of places from the first IP of the CIDR for the
            fixed IP address
        @type num: int
        @return: fixed IP
        @rtype: dict
        """
        ip = self.get_next_ip(cidr=cidr, num=num)
        return dict(subnet_id=subnet_id, ip_address=ip)

    def get_fixed_ips(self, subnet, num=1, timeout=None):
        """
        @summary: generates multiple fixed ips within a subnet
        @param subnet: subnet entity object
        @type subnet: models.response.subnet.Subnet
        @param num: number of fixed IPs to get
        @type num: int
        @param timeout: timeout for replacing duplicate IPs
        @type timeout: int
        @return: fixed IPs
        @rtype: list
        """
        cidr = subnet.cidr
        ips = self.get_ips(cidr=cidr, num=num)
        ips_count = len(ips)

        # Removing duplicate IPs in case of any and trying to replace
        ips = list(set(ips))
        if ips_count != len(ips):
            duplicate_count = ips_count - len(ips)
            timeout = timeout or self.config.resource_get_timeout
            endtime = time.time() + int(timeout)
            while duplicate_count > 0 and time.time() < endtime:
                new_ip = self.get_random_ip(cidr)
                if new_ip not in ips:
                    ips.append(new_ip)
                    duplicate_count -= 1
        fixed_ips = [dict(subnet_id=subnet.id, ip_address=ip) for ip in ips]
        return fixed_ips

    def get_allocation_pool(self, cidr, first_increment=1, last_decrement=1,
                            start_increment=None, end_increment=None):
        """
        @summary: gets default allocation pool for an IPv4/IPv6 address
        @param cidr: represents IP range for the subnet and should be in the
            form <network_address>/<prefix>
        @type cidr: string
        @param first_increment: places from the fist IP of the CIDR to the
            first IP of the allocation pool
        @type first_increment: int
        @param last_decrement: places from the last IP of the CIDR to the last
            IP of the allocation pool
        @type last_decrement: int
        @param start_increment: if given, start IP of allocation pool
        @type start_increment: int
        @param end_increment: if given, end IP of allocation pool
        @type end_increment: int
        @return: allocation pool
        @rtype: dict
       """

        if not self.verify_ip(cidr):
            raise InvalidIPException
        net = netaddr.IPNetwork(cidr)

        if start_increment and end_increment:
            first_ip = str(netaddr.IPAddress(net.first + start_increment))
            last_ip = str(netaddr.IPAddress(net.first + end_increment))
        else:
            first_ip = str(netaddr.IPAddress(net.first + first_increment))
            last_ip = str(netaddr.IPAddress(net.last - last_decrement))

        return dict(start=first_ip, end=last_ip)

    def get_allocation_pools(self, cidr, start_increment, ip_range, interval,
                             num):
        """
        @summary: Generates allocation pools subnet data
        @param cidr: cidr for allocation pools
        @type cidr: string
        @param start_increment: increment from first cidr address to first
            allocation pool IP address
        @type start_increment: int
        @param ip_range: ip addresses from start IP to end IP of allocation
            pool
        @type ip_range: int
        @param interval: ip addresses from end of allocation pool to start IP
            of the next allocation pool (if multiple)
        @type interval: int
        @param num: number of allocation pools to create within the cidr
        @type num: int
        @return: allocation pools
        @rtype: list
        """
        allocation_pools = []
        for _ in range(num):
            end_increment = start_increment + ip_range
            allocation_pool = self.get_allocation_pool(cidr=cidr,
                start_increment=start_increment, end_increment=end_increment)
            allocation_pools.append(allocation_pool)
            start_increment = end_increment + interval
        return allocation_pools

    def get_host_routes(self, cidr, ips):
        """
        @summary: create 1 or more host routes
        @param cidr: host_route destination CIDR
        @type cidr: string
        @param ips: host_routes nexthops
        @type ips: list(str)
        """
        host_routes = [dict(destination=cidr, nexthop=ip) for ip in ips]
        return host_routes

    def format_dns_nameservers(self, dns_nameservers):
        """
        @summary: formats dns_nameservers for assertions removing zeros on
            IPv6 addresses
        @param dns_nameservers: list of dns_nameservers
        @type dns_nameservers: list(str)
        @return: formated dns_nameservers
        @rtype: list(str)
        """
        dns_ns = [str(netaddr.IPAddress(svr)) for svr in dns_nameservers]
        return dns_ns

    def format_allocation_pools(self, allocation_pools):
        """
        @summary: formats allocation pools for assertions removing zeros on
            IPv6 addresses
        @param allocation_pools: list of allocation pools
        @type allocation_pools: list(dict)
        @return: formated allocation pools
        @rtype: list(dict)
        """
        formated_allocation_pools = []
        for pool in allocation_pools:
            result = dict(start=str(netaddr.IPAddress(pool['start'])),
                          end=str(netaddr.IPAddress(pool['end'])))
            formated_allocation_pools.append(result)
        return formated_allocation_pools

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
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
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

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the update was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to create {0} subnet after {1} attempts: '
                '{2}').format(name, resource_build_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            return result

    def update_subnet(self, subnet_id, name=None, gateway_ip=None,
                      dns_nameservers=None, host_routes=None,
                      enable_dhcp=None, allocation_pools=None,
                      resource_update_attempts=None, raise_exception=False,
                      poll_interval=None):
        """
        @summary: Updates and verifies a specified Subnet
        @param subnet_id: The UUID for the subnet
        @type subnet_id: string
        @param name: human readable name for the subnet, may not be unique
            (CRUD: CRU)
        @type name: string
        @param gateway_ip: default gateway used by devices in the subnet
            (CRUD: CRUD)
        @type gateway_ip: string
        @param dns_nameservers: DNS name servers used by subnet hosts
            (CRUD: CRU)
        @type dns_nameservers: list(str)
        @param host_routes: routes that should be used by devices with IPs
            from this subnet (does not includes the local route (CRUD: CRU)
        @type host_routes: list(dict)
        @param enable_dhcp: whether DHCP is enabled (CRUD:CRU)
        @type enable_dhcp: bool
        @param allocation_pools: sub range of cidr available for dynamic
            allocation to ports (CRUD: CRU)
        @type allocation_pools: list(dict)
        @param resource_update_attempts: number of API retries
        @type resource_update_attempts: int
        @param raise_exception: flag to raise an exception if the
            Subnet was not updated or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_update_attempts = (resource_update_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Subnet Update failure'
        for attempt in range(resource_update_attempts):
            self._log.debug('Attempt {0} of {1} updating subnet {2}'.format(
                attempt + 1, resource_update_attempts, subnet_id))

            resp = self.client.update_subnet(
                subnet_id=subnet_id, name=name, gateway_ip=gateway_ip,
                dns_nameservers=dns_nameservers, host_routes=host_routes,
                enable_dhcp=enable_dhcp, allocation_pools=allocation_pools)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.UPDATE_SUBNET,
                label=subnet_id, message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the update was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to update {0} subnet after {1} attempts: '
                '{2}').format(subnet_id, resource_update_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceUpdateException(err_msg)
            return result

    def get_subnet(self, subnet_id, resource_get_attempts=None,
                    raise_exception=False, poll_interval=None):
        """
        @summary: Shows and verifies a specified subnet
        @param subnet_id: The UUID for the subnet
        @type subnet_id: string
        @param resource_get_attempts: number of API retries
        @type resource_get_attempts: int
        @param raise_exception: flag to raise an exception if the get
            Subnet was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_get_attempts = (resource_get_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Subnet Get failure'
        for attempt in range(resource_get_attempts):
            self._log.debug('Attempt {0} of {1} getting subnet {2}'.format(
                attempt + 1, resource_get_attempts, subnet_id))

            resp = self.client.get_subnet(subnet_id=subnet_id)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.GET_SUBNET,
                label=subnet_id, message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the get was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to GET {0} subnet after {1} attempts: '
                '{2}').format(subnet_id, resource_get_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceGetException(err_msg)
            return result

    def list_subnets(self, subnet_id=None, network_id=None, cidr=None,
                     tenant_id=None, gateway_ip=None, ip_version=None,
                     enable_dhcp=None, name=None, limit=None, marker=None,
                     page_reverse=None, resource_list_attempts=None,
                     raise_exception=False, poll_interval=None):
        """
        @summary: Lists subnets and verifies the response is the expected
        @param subnet_id: subnet ID to filter by
        @type subnet_id: string
        @param network_id: network ID to filter by
        @type network_id: string
        @param cidr: cider to filter by
        @type cidr: string
        @param tenant_id: owner of the network to filter by
        @type tenant_id: string
        @param gateway_ip: gateway_ip to filter by
        @type gateway_ip: string
        @param ip_version: IP version 4 or 6 to filter by
        @type ip_version: int
        @param enable_dhcp: enable_dhcp status to filter by
        @type enable_dhcp: bool
        @param name: subnet name to filter by
        @type name: string
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @param resource_list_attempts: number of API retries
        @type resource_list_attempts: int
        @param raise_exception: flag to raise an exception if the list
            Subnet was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_list_attempts = (resource_list_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Subnet List failure'
        for attempt in range(resource_list_attempts):
            self._log.debug('Attempt {0} of {1} with subnet list'.format(
                attempt + 1, resource_list_attempts))

            resp = self.client.list_subnets(
                subnet_id=subnet_id, network_id=network_id, cidr=cidr,
                     tenant_id=tenant_id, gateway_ip=gateway_ip,
                     ip_version=ip_version, enable_dhcp=enable_dhcp, name=name,
                     limit=limit, marker=marker, page_reverse=page_reverse)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.LIST_SUBNETS,
                label='', message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the list was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to LIST subnets after {0} attempts: '
                '{1}').format(resource_list_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceListException(err_msg)
            return result

    def delete_subnet(self, subnet_id, resource_delete_attempts=None,
                      raise_exception=False, poll_interval=None):
        """
        @summary: Deletes and verifies a specified subnet is deleted
        @param subnet_id: The UUID for the subnet
        @type subnet_id: string
        @param resource_delete_attempts: number of API retries
        @type resource_delete_attempts: int
        @param raise_exception: flag to raise an exception if the deleted
            Subnet was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_delete_attempts = (resource_delete_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        for attempt in range(resource_delete_attempts):
            self._log.debug('Attempt {0} of {1} deleting subnet {2}'.format(
                attempt + 1, resource_delete_attempts, subnet_id))

            resp = self.client.delete_subnet(subnet_id=subnet_id)
            result.response = resp

            # Delete response is without entity so resp_check can not be used
            if (resp.ok and
                resp.status_code == NeutronResponseCodes.DELETE_SUBNET):
                return result

            err_msg = ('{subnet} Subnet Delete failure, expected status '
                'code: {expected_status}. Response: {status} {reason} '
                '{content}').format(
                subnet=subnet_id,
                expected_status=NeutronResponseCodes.DELETE_SUBNET,
                status=resp.status_code, reason=resp.reason,
                content=resp.content)
            self._log.error(err_msg)
            result.failures.append(err_msg)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to DELETE {0} subnet after {1} attempts: '
                '{2}').format(subnet_id, resource_delete_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceDeleteException(err_msg)
            return result

    def clean_subnet(self, subnet_id, timeout=None, poll_interval=None):
        """
        @summary: deletes a subnet within a time out
        @param subnet_id: The UUID for the subnet
        @type subnet_id: string
        @param timeout: seconds to wait for the subnet to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: None if delete was successful or the undeleted subnet_id
        @rtype: None or string
        """
        timeout = timeout or self.config.resource_delete_timeout
        poll_interval = poll_interval or self.config.api_poll_interval
        endtime = time.time() + int(timeout)
        log_msg = 'Deleting {0} subnet within a {1}s timeout '.format(
            subnet_id, timeout)
        self._log.info(log_msg)
        resp = None
        while time.time() < endtime:
            try:
                self.client.delete_subnet(subnet_id=subnet_id)
                resp = self.client.get_subnet(subnet_id=subnet_id)
            except Exception as err:
                err_msg = ('Encountered an exception deleting a subnet with'
                    'the clean_subnet method. Exception: {0}').format(err)
                self._log.error(err_msg)
            if (resp is not None and
                resp.status_code == NeutronResponseCodes.NOT_FOUND):
                return None
            time.sleep(poll_interval)

        err_msg = 'Unable to delete {0} subnet within a {1}s timeout'.format(
            subnet_id, timeout)
        self._log.error(err_msg)
        return subnet_id

    def clean_subnets(self, subnets_list, timeout=None, poll_interval=None):
        """
        @summary: deletes each subnet from a list calling clean_subnet
        @param subnets_list: list of subnets UUIDs
        @type subnets_list: list(str)
        @param timeout: seconds to wait for the subnet to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: list of undeleted subnets UUIDs
        @rtype: list(str)
        """
        log_msg = 'Deleting subnets: {0}'.format(subnets_list)
        self._log.info(log_msg)
        undeleted_subnets = []
        for subnet in subnets_list:
            result = self.clean_subnet(subnet_id=subnet, timeout=timeout,
                                       poll_interval=poll_interval)
            if result:
                undeleted_subnets.append(result)
        if undeleted_subnets:
            err_msg = 'Unable to delete subnets: {0}'.format(
                undeleted_subnets)
            self._log.error(err_msg)
        return undeleted_subnets
