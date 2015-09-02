"""
Copyright 2015 Rackspace

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
from cafe.engine.models.base import BaseModel
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.composites import NetworkingComposite


class ServerPersona(BaseModel, NetworkingBaseBehaviors):
    """
    @summary: Server data object for quick access to networking data and also
        tracking expected counts for ports and fixed IPs
    """
    def __init__(self, server=None, pnet=True, snet=True, inet=False,
                 network=None, subnetv4=None, portv4=None, subnetv6=None,
                 portv6=None, inet_port_count=0, snet_port_count=1,
                 pnet_port_count=1, inet_fipsv4_count=0, inet_fipsv6_count=0,
                 snet_fipsv4_count=1, snet_fipsv6_count=0,
                 pnet_fipsv4_count=1, pnet_fipsv6_count=0):
        super(ServerPersona, self).__init__()

        # Server entity object
        self.server = server

        # Server expected networks (bool value)
        self.pnet = pnet
        self.snet = snet
        self.inet = inet

        # Server isolated network, subnet and port (entity objects, if any)
        self.network = network
        self.subnetv4 = subnetv4
        self.portv4 = portv4
        self.subnetv6 = subnetv6
        self.portv6 = portv6

        # Expected server port count by network
        self.inet_port_count = inet_port_count
        self.snet_port_count = snet_port_count
        self.pnet_port_count = pnet_port_count

        # Expected server Fixed IP address count by network and version
        self.inet_fipsv4_count = inet_fipsv4_count
        self.inet_fipsv6_count = inet_fipsv6_count
        self.snet_fipsv4_count = snet_fipsv4_count
        self.snet_fipsv6_count = snet_fipsv6_count
        self.pnet_fipsv4_count = pnet_fipsv4_count
        self.pnet_fipsv6_count = pnet_fipsv6_count

        # Networking composite
        self.net = NetworkingComposite()

        # base config from networking/networks/common/config.py
        self.config = self.net.config

        # sub-composites
        self.networks = self.net.networks
        self.subnets = self.net.subnets
        self.ports = self.net.ports
        self.behaviors = self.net.behaviors

        # Other reusable values (service_network_id aka Private Network)
        self.public_network_id = self.networks.config.public_network_id
        self.service_network_id = self.networks.config.service_network_id

        # Error list for behavior method calls
        self.errors = []

        self.list_port_failure_msg = ('Unable to get server {0} ports for '
                                      'network {1}. Failures: {2}.')
        self.fixed_ips_failure_msg = ('Unable to get server {0} fixed IPs '
                                      'with IPv{1} version for network {2}')

    @property
    def pnet_ports(self):
        """
        @summary: updates server attribute with latest public net ports
        @return: public network ports
        @rtype: list of port entity objects
        """
        ports = self.ports.behaviors.list_ports(
            device_id=self.server.id, network_id=self.public_network_id)
        if ports.failures:
            msg = self.list_port_failure_msg.format(
                self.server.id, self.public_network_id, ports.failures)
            self.errors.append(msg)
            self._log.error(msg)
            return None
        return ports.response.entity

    @property
    def snet_ports(self):
        """
        @summary: updates server attribute with latest service net ports
        @return: private network ports
        @rtype: list of port entity objects
        """
        ports = self.ports.behaviors.list_ports(
            device_id=self.server.id, network_id=self.service_network_id)
        if ports.failures:
            msg = self.list_port_failure_msg.format(
                self.server.id, self.service_network_id, ports.failures)
            self.errors.append(msg)
            self._log.error(msg)
            return None
        return ports.response.entity

    @property
    def inet_ports(self):
        """
        @summary: updates server attribute with latest isolated net ports
        @return: isolated network ports
        @rtype: list of port entity objects
        """
        ports = self.ports.behaviors.list_ports(
            device_id=self.server.id, network_id=self.network.id)
        if ports.failures:
            msg = self.list_port_failure_msg.format(
                self.server.id, self.network.id, ports.failures)
            self.errors.append(msg)
            self._log.error(msg)
            return None
        return ports.response.entity

    @property
    def inet_fipsv4(self):
        """
        @summary: updates server attribute with latest isolated fixed IPs
        @return: isolated network fixed IPv4 addresses
        @rtype: list of strings
        """
        ip_version = 4
        addresses = self._get_fixed_ips(port_type='inet_ports',
                                        ip_version=ip_version)
        if addresses is not None:
            return addresses
        else:
            msg = self.fixed_ips_failure_msg.format(
                self.server.id, ip_version, self.network.id)
            self.errors.append(msg)
            self._log.error(msg)
            return None

    @property
    def inet_fipsv6(self):
        """
        @summary: updates server attribute with latest isolated fixed IPs
        @return: isolated network fixed IPv6 addresses
        @rtype: list of strings
        """
        ip_version = 6
        addresses = self._get_fixed_ips(port_type='inet_ports',
                                        ip_version=ip_version)
        if addresses is not None:
            return addresses
        else:
            msg = self.fixed_ips_failure_msg.format(
                self.server.id, ip_version, self.network.id)
            self.errors.append(msg)
            self._log.error(msg)
            return None

    @property
    def snet_fipsv4(self):
        """
        @summary: updates server attribute with latest private fixed IPs
        @return: service (private) network fixed IPv4 addresses
        @rtype: list of strings
        """
        ip_version = 4
        addresses = self._get_fixed_ips(port_type='snet_ports',
                                        ip_version=ip_version)
        if addresses is not None:
            return addresses
        else:
            msg = self.fixed_ips_failure_msg.format(
                self.server.id, ip_version, self.service_network_id)
            self.errors.append(msg)
            self._log.error(msg)
            return None

    @property
    def snet_fipsv6(self):
        """
        @summary: updates server attribute with latest private fixed IPs
        @return: service (private) network fixed IPv6 addresses
        @rtype: list of strings
        """
        ip_version = 6
        addresses = self._get_fixed_ips(port_type='snet_ports',
                                        ip_version=ip_version)
        if addresses is not None:
            return addresses
        else:
            msg = self.fixed_ips_failure_msg.format(
                self.server.id, ip_version, self.service_network_id)
            self.errors.append(msg)
            self._log.error(msg)
            return None

    @property
    def pnet_fipsv4(self):
        """
        @summary: updates server attribute with latest public fixed IPs
        @return: public network fixed IPv4 addresses
        @rtype: list of strings
        """
        ip_version = 4
        addresses = self._get_fixed_ips(port_type='pnet_ports',
                                        ip_version=ip_version)
        if addresses is not None:
            return addresses
        else:
            msg = self.fixed_ips_failure_msg.format(
                self.server.id, ip_version, self.public_network_id)
            self.errors.append(msg)
            self._log.error(msg)
            return None

    @property
    def pnet_fipsv6(self):
        """
        @summary: updates server attribute with latest public fixed IPs
        @return: public network fixed IPv6 addresses
        @rtype: list of strings
        """
        ip_version = 6
        addresses = self._get_fixed_ips(port_type='pnet_ports',
                                        ip_version=ip_version)
        if addresses is not None:
            return addresses
        else:
            msg = self.fixed_ips_failure_msg.format(
                self.server.id, ip_version, self.public_network_id)
            self.errors.append(msg)
            self._log.error(msg)
            return None

    @property
    def pnet_port_ids(self):
        """
        @summary: gets the public network port ids
        """
        ports = self.pnet_ports
        if ports is None:
            return []
        port_ids = self._get_port_ids(ports=ports)
        return port_ids

    @property
    def snet_port_ids(self):
        """
        @summary: gets the service (private) network port ids
        """
        ports = self.snet_ports
        if ports is None:
            return []
        port_ids = self._get_port_ids(ports=ports)
        return port_ids

    @property
    def inet_port_ids(self):
        """
        @summary: gets the public network port ids
        """
        ports = self.inet_ports
        if ports is None:
            return []
        port_ids = self._get_port_ids(ports=ports)
        return port_ids

    def _get_port_ids(self, ports):
        """
        @summary: gets the port ids
        @param ports: pnet_ports, snet_ports or inet_ports
        @type port_type: list of port entities
        @return: port IDs
        @rtype: list of strings
        """
        result = []
        for port in ports:
            result.append(port.id)
        return result

    def _get_fixed_ips(self, port_type, ip_version):
        """
        @summary: gets the fixed IPs based on port type and ip_version
        @param port_type: pnet_ports, snet_ports or inet_ports
        @type port_type: str
        @param ip_version: 4 or 6 depneding on the desired IP version
        @type ip_version: int
        @return: fixed IP addresses
        @rtype: list of strings
        """
        result = []
        if hasattr(self, port_type):
            ports = getattr(self, port_type)
        else:
            ports = None
        if ports is not None:
            for port in ports:
                addresses = (
                    self.ports.behaviors.get_addresses_from_fixed_ips(
                    fixed_ips=port.fixed_ips, ip_version=ip_version))
                result.append(addresses)
            return result
        return None
