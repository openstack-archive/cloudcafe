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
from cloudcafe.networking.networks.common.constants \
    import NetworkTypes, PortTypes
from cloudcafe.networking.networks.composites import NetworkingComposite
from cloudcafe.networking.networks.extensions.security_groups_api.composites \
    import SecurityGroupsComposite

from cloudcafe.networking.networks.common.exceptions \
    import PortUpdateException


class ServerPersona(BaseModel, NetworkingBaseBehaviors):
    """
    @summary: Server data object for quick access to networking data and also
        tracking expected counts for ports and fixed IPs
    """
    def __init__(self, server=None, pnet=True, snet=True, inet=False,
                 network=None, subnetv4=None, portv4=None, subnetv6=None,
                 portv6=None, inet_port_count=0, snet_port_count=1,
                 pnet_port_count=1, inet_fix_ipv4_count=0,
                 inet_fix_ipv6_count=0, snet_fix_ipv4_count=1,
                 snet_fix_ipv6_count=0, pnet_fix_ipv4_count=1,
                 pnet_fix_ipv6_count=1, keypair=None, ssh_username=None):
        super(ServerPersona, self).__init__()
        """
        @param server: server entity
        @type server: compute.servers_api.models.servers.Server
        @param pnet: if the server has public network flag
        @type pnet: bool
        @param snet: if the server has service (private) network flag
        @type snet: bool
        @param inet: if the server has isolated network flag
        @type inet: bool
        @param network: (optional) isolated network entity if applies
        @type network: networking.networks.common.models.response
            .network.Network
        @param subnetv4: (optional) isolated network IPv4 subnet if applies
        @type subnetv4: networking.networks.common.models.response
            .subnet.Subnet
        @param portv4: (optional) isolated network IPv4 port if applies
        @type portv4: networking.networks.common.models.response.port.Port
        @param subnetv6: (optional) isolated network IPv6 subnet if applies
        @type subnetv6: networking.networks.common.models.response
            .subnet.Subnet
        @param portv6: (optional) isolated network IPv6 port if applies
        @type portv6: networking.networks.common.models.response.port.Port
        @param inet_port_count: expected isolated network port count
        @type inet_port_count: int
        @param snet_port_count: expected service (private) network port count
        @type snet_port_count: int
        @param pnet_port_count: expected public network port count
        @type pnet_port_count: int
        @param inet_fix_ipv4_count: expected isolated network fixed IPv4s count
        @type inet_fix_ipv4_count: int
        @param inet_fix_ipv6_count: expected isolated network fixed IPv6s count
        @type inet_fix_ipv6_count: int
        @param snet_fix_ipv4_count: expected service network fixed IPv4s count
        @type snet_fix_ipv4_count: int
        @param snet_fix_ipv6_count: expected service network fixed IPv6s count
        @type snet_fix_ipv6_count: int
        @param pnet_fix_ipv4_count: expected public network fixed IPv4s count
        @type pnet_fix_ipv4_count: int
        @param pnet_fix_ipv6_count: expected public network fixed IPv6s count
        @type pnet_fix_ipv6_count: int
        @param keypair: keypair object with private_key attribute
        @type keypair: networking.networks.behaviors create_keypair response
        @param ssh_username: remote client username for SSH
        @type ssh_username: str
        """

        # Server and keypair entity object
        self.server = server
        self.keypair = keypair
        self.ssh_username = ssh_username

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
        self.inet_fix_ipv4_count = inet_fix_ipv4_count
        self.inet_fix_ipv6_count = inet_fix_ipv6_count
        self.snet_fix_ipv4_count = snet_fix_ipv4_count
        self.snet_fix_ipv6_count = snet_fix_ipv6_count
        self.pnet_fix_ipv4_count = pnet_fix_ipv4_count
        self.pnet_fix_ipv6_count = pnet_fix_ipv6_count

        # Networking composites
        self.net = NetworkingComposite()
        self.sec = SecurityGroupsComposite()

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
        self.isolated_network_id = getattr(self.network, 'id', None)

        # Error list for behavior method calls
        self.errors = []

        self.list_port_failure_msg = ('Unable to get server {0} ports for '
                                      'network {1}. Failures: {2}.')
        self.fixed_ips_failure_msg = ('Unable to get server {0} fixed IPs '
                                      'with IPv{1} version for network {2}')
        self.update_port_failure_msg = ('Unable to update server {0} ports for'
                                        ' network {1}. Failures: {2}.')

    def __str__(self):

        def build_data_str(data_list, attr=None):
            if data_list is None:
                return None

            if attr is None:
                data_str = [elem for elem in data_list]
            else:
                data_str = [getattr(elem, attr) for elem in data_list]

            return ', '.join(data_str)

        data = {'name': self.server.name, 'svr_id': self.server.id,
                'pub_net_id': self.public_network_id,
                'pub_port_ids': self.pnet_port_ids,
                'pub_sec_groups': self.pnet_security_groups,
                'pub_ipv4_addr': self.pnet_fix_ipv4,
                'pub_ipv6_addr': self.pnet_fix_ipv6,
                'svc_net_id': self.service_network_id,
                'svc_port_ids': self.snet_port_ids,
                'svc_sec_groups': self.snet_security_groups,
                'svc_ipv4_addr': self.snet_fix_ipv4,
                'svc_ipv6_addr': self.snet_fix_ipv6,
                'iso_net_id': getattr(self.network, 'id', None),
                'iso_sub_id': getattr(self.subnetv4, 'id', None),
                'iso_port_ids': self.inet_port_ids,
                'iso_sec_groups': self.inet_security_groups,
                'iso_ipv4_addr': self.inet_fix_ipv4,
                'iso_sub_v6_ids': build_data_str(self.subnetv6, 'id'),
                'iso_ipv6_addr': self.inet_fix_ipv6}

        msg = "\nServer Name: {name} ({svr_id})\n"
        msg += "Public Net:\n"
        msg += "\tNetwork Id: {pub_net_id}\n"
        msg += "\tPort Ids: {pub_port_ids}\n"
        msg += "\tSecurity Groups: {pub_sec_groups}\n"
        msg += "\tIPv4 Address: {pub_ipv4_addr}\n"
        msg += "\tIPv6 Address: {pub_ipv6_addr}\n\n"

        msg += "Service Net:"
        msg += "\tNetwork Id: {svc_net_id}\n"
        msg += "\tPort Ids: {svc_port_ids}\n"
        msg += "\tSecurity Groups: {svc_sec_groups}\n"
        msg += "\tIPv4 Address: {svc_ipv4_addr}\n"
        msg += "\tIPv6 Address: {svc_ipv6_addr}\n\n"

        msg += "Isolated Net:\n"
        msg += "\tNetwork Id: {iso_net_id}\n"
        msg += "\tSubnet Id (IPv4): {iso_sub_id}\n"
        msg += "\tPort Ids: {iso_port_ids}\n"
        msg += "\tSecurity Groups: {iso_sec_groups}\n"
        msg += "\tIPv4 Address: {iso_ipv4_addr}\n"
        msg += "\tSubnet Id (IPv6): {iso_sub_v6_ids}\n"
        msg += "\tIPv6 Address: {iso_ipv6_addr}\n\n"

        return msg.format(**data)

    @property
    def pnet_ports(self):
        """
        @summary: server public network ports
        @return: public network ports
        @rtype: list of port entity objects
        """
        return self._port_response(network_type=NetworkTypes.PUBLIC)

    @property
    def snet_ports(self):
        """
        @summary: server service (private) network ports
        @return: private network ports
        @rtype: list of port entity objects
        """
        return self._port_response(network_type=NetworkTypes.SERVICE)

    @property
    def inet_ports(self):
        """
        @summary: server isolated network ports
        @return: isolated network ports
        @rtype: list of port entity objects
        """
        return self._port_response(network_type=NetworkTypes.ISOLATED)

    @property
    def inet_fix_ipv4(self):
        """
        @summary: updates server attribute with latest isolated fixed IPs
        @return: isolated network fixed IPv4 addresses
        @rtype: list of strings
        """
        return self._get_fixed_ips(ip_version=4, port_type=PortTypes.ISOLATED,
                                   network_type=NetworkTypes.ISOLATED)

    @property
    def inet_fix_ipv6(self):
        """
        @summary: updates server attribute with latest isolated fixed IPs
        @return: isolated network fixed IPv6 addresses
        @rtype: list of strings
        """
        return self._get_fixed_ips(ip_version=6, port_type=PortTypes.ISOLATED,
                                   network_type=NetworkTypes.ISOLATED)

    @property
    def snet_fix_ipv4(self):
        """
        @summary: updates server attribute with latest private fixed IPs
        @return: service (private) network fixed IPv4 addresses
        @rtype: list of strings
        """
        return self._get_fixed_ips(ip_version=4, port_type=PortTypes.SERVICE,
                                   network_type=NetworkTypes.SERVICE)

    @property
    def snet_fix_ipv6(self):
        """
        @summary: updates server attribute with latest private fixed IPs
        @return: service (private) network fixed IPv6 addresses
        @rtype: list of strings
        """
        return self._get_fixed_ips(ip_version=6, port_type=PortTypes.SERVICE,
                                   network_type=NetworkTypes.SERVICE)

    @property
    def pnet_fix_ipv4(self):
        """
        @summary: updates server attribute with latest public fixed IPs
        @return: public network fixed IPv4 addresses
        @rtype: list of strings
        """
        return self._get_fixed_ips(ip_version=4, port_type=PortTypes.PUBLIC,
                                   network_type=NetworkTypes.PUBLIC)

    @property
    def pnet_fix_ipv6(self):
        """
        @summary: updates server attribute with latest public fixed IPs
        @return: public network fixed IPv6 addresses
        @rtype: list of strings
        """
        return self._get_fixed_ips(ip_version=6, port_type=PortTypes.PUBLIC,
                                   network_type=NetworkTypes.PUBLIC)

    @property
    def pnet_port_ids(self):
        """
        @summary: gets the public network port ids
        """
        return self._get_port_ids(port_type=PortTypes.PUBLIC)

    @property
    def snet_port_ids(self):
        """
        @summary: gets the service (private) network port ids
        """
        return self._get_port_ids(port_type=PortTypes.SERVICE)

    @property
    def inet_port_ids(self):
        """
        @summary: gets the isolated network port ids
        """
        return self._get_port_ids(port_type=PortTypes.ISOLATED)

    @property
    def pnet_security_groups(self):
        """
        @summary: gets the security groups at the public network ports
        """
        return self._get_port_security_groups(port_type=PortTypes.PUBLIC)

    @property
    def snet_security_groups(self):
        """
        @summary: gets the security groups at the service network ports
        """
        return self._get_port_security_groups(port_type=PortTypes.SERVICE)

    @property
    def inet_security_groups(self):
        """
        @summary: gets the security groups at the isolated network ports
        """
        return self._get_port_security_groups(port_type=PortTypes.ISOLATED)

    @property
    def remote_client(self):
        """
        @summary: gets remote instance client
        """
        return self._get_remote_instance_client()

    def update_server_persona(self, clear_errors=True):
        """
        @summary: updates the self.server entity doing a GET server call
        """
        self.server = self.behaviors.get_networking_server(server=self.server)
        self.isolated_network_id = getattr(self.network, 'id', None)

        # Updating the isolated network port attribute
        isolated_ports = self.inet_ports
        if self.subnetv4 and isolated_ports:
            self.portv4 = isolated_ports[0]
        if self.subnetv6 and isolated_ports:
            self.portv6 = isolated_ports[0]

        if clear_errors:
            self.errors = []

    def add_security_groups_to_ports(self, port_type, security_group_ids,
                                     port_ids=None, raise_exception=False):
        """
        Adds a security group or groups to a server port or ports based on type
        @param port_type: port network type, for ex. pnet (public),
            snet (service), or inet (isolated).
        @type port_type: str
        @param security_group_ids: the escurity group or groups to
            be added to the port(s).
        @type security_group_ids: list
        @param port_ids (optional): to target specific ports by ID where the
            security group(s) should be added. They must match the network type
            param. By default, all the server port(s) by the given network type
            will be added the security group(s).
        @type port_ids: list
        """

        # Getting all the port ids from the network port type
        port_ids_label = '{0}_port_ids'.format(port_type)
        persona_port_ids = getattr(self, port_ids_label, None)

        # Targeting specific ports if port_ids given
        if port_ids:
            port_ids_set = set(port_ids)
            port_ids = list(port_ids_set.intersection(persona_port_ids))
        else:
            port_ids = persona_port_ids

        # Adding the security group
        for port_id in port_ids:
            update = self.ports.behaviors.update_port(
                port_id=port_id, security_groups=security_group_ids)
            if update.failures:
                msg = self.update_port_failure_msg.format(self.server.id,
                                                          port_type,
                                                          update.failures)
                self.errors.append(msg)
                self._log.error(msg)
                if raise_exception:
                    raise PortUpdateException(msg)
                return False
        return True

    def _port_response(self, network_type):
        """
        @summary: returns server network ports based on network type
        @param network_type: public, service or isolated network type
        @param network_type: str
        """
        network_id_label = '{0}_network_id'.format(network_type.lower())
        network_id = getattr(self, network_id_label, None)
        if not network_id:
            return []

        ports = self.ports.behaviors.list_ports(device_id=self.server.id,
                                                network_id=network_id)
        if ports.failures:
            msg = self.list_port_failure_msg.format(self.server.id, network_id,
                                                    ports.failures)
            self.errors.append(msg)
            self._log.error(msg)
            return []
        return ports.response.entity

    def _get_remote_instance_client(self):
        """
        @summary: returns a remote instance client
        """
        ip_address = self.pnet_fix_ipv4[0]
        remote_client = self.behaviors.get_remote_instance_client(
            server=self.server, ip_address=ip_address,
            private_key=self.keypair.private_key,
            ssh_username=self.ssh_username)
        return remote_client

    def _get_fixed_ips(self, ip_version, port_type, network_type):
        """
        @summary: gets fixed IPs from server ports
        @param ip_version: 4 or 6 depending on the port IP version
        @type ip_version: int
        @param port_type: pnet, snet or inet port type
        @type port_type: str
        @param network_type: public, service or isolated network type
        @param network_type: str
        @return: fixed IP addresses
        @rtype: list of strings
        """
        port_attr = '{0}_ports'.format(port_type)
        network_id_label = '{0}_network_id'.format(network_type.lower())
        network_id = getattr(self, network_id_label, None)
        ports = getattr(self, port_attr, [])

        result = []
        for port in ports:
            addresses = self.ports.behaviors.get_addresses_from_fixed_ips(
                fixed_ips=port.fixed_ips, ip_version=ip_version)
            result.extend(addresses)

        if not result:
            msg = self.fixed_ips_failure_msg.format(
                self.server.id, ip_version, network_id)
            self.errors.append(msg)
            self._log.error(msg)

        return result

    def _get_port_ids(self, port_type):
        """
        @summary: gets the port ids
        @param port_type: pnet, snet or inet port type
        @type port_type: str
        @return: port IDs
        @rtype: list(str)
        """
        port_attr = '{0}_ports'.format(port_type.lower())
        ports = getattr(self, port_attr, [])
        port_ids = [port.id for port in ports]
        return port_ids

    def _get_port_security_groups(self, port_type):
        """
        @summary: gets the ports security groups
        @param port_type: pnet, snet or inet port type
        @type port_type: str
        @return: all the security groups of the same port type
        @rtype: list(list)
        """
        port_attr = '{0}_ports'.format(port_type.lower())
        ports = getattr(self, port_attr, [])
        port_sec_groups = [port.security_groups for port in ports]
        return port_sec_groups
