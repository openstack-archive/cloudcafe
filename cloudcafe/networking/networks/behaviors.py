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

from cloudcafe.compute.common.exceptions import ItemNotFound, TimeoutException
from cloudcafe.compute.composites import ComputeComposite
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.common.config import NetworkingBaseConfig
from cloudcafe.networking.networks.common.constants \
    import ComputeResponseCodes, NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import NetworkGETException, SubnetGETException, UnsupportedTypeException, \
        UnavailableComputeInteractionException
from cloudcafe.networking.networks.common.models.response.network \
    import Network
from cloudcafe.networking.networks.common.models.response.port \
    import Port


class NetworkingBehaviors(NetworkingBaseBehaviors):
    """All API behaviors for helper methods"""

    def __init__(self, networks_behaviors, subnets_behaviors, ports_behaviors):
        super(NetworkingBehaviors, self).__init__()

        self.config = NetworkingBaseConfig()
        self.networks_config = networks_behaviors.config
        self.networks_client = networks_behaviors.client
        self.subnets_client = subnets_behaviors.client
        self.subnets_config = subnets_behaviors.config
        self.ports_client = ports_behaviors.client
        self.ports_config = ports_behaviors.config
        self.networks_behaviors = networks_behaviors
        self.subnets_behaviors = subnets_behaviors
        self.ports_behaviors = ports_behaviors

        if self.config.use_compute_api:
            self.compute = ComputeComposite()
        else:
            self.compute = None

    def get_port_fixed_ips(self, port):
        """Get the port fixed ips"""
        if hasattr(port, 'fixed_ips') and port.fixed_ips:
            fixed_ips = port.fixed_ips
        else:
            fixed_ips = None
        return fixed_ips

    def get_port_subnet_id(self, port, n=0):
        """
        @summary: Get the n-th fixed ip subnet of the port
        @param port: port
        @type port: Port entity
        @param n: position in the Port attribute fixed_ip list
        @type n: int
        """
        fixed_ips = self.get_port_fixed_ips(port)
        fixed_ip = fixed_ips[n]
        subnet_id = fixed_ip.get('subnet_id')
        return subnet_id

    def get_port_ip_address(self, port, n=0):
        """
        @summary: Get the n-th fixed ip ip_address of the port
        @param port: port
        @type port: Port entity
        @param n: position in the Port attribute fixed_ip list
        @type n: int
        """
        fixed_ips = self.get_port_fixed_ips(port)
        fixed_ip = fixed_ips[n]
        ip_address = fixed_ip.get('ip_address')
        return ip_address

    def create_network_subnet_port(self, network_id=None, name=None,
                                   ip_version=None, raise_exception=False):
        """
        @summary: Creates a network with subnet and port, if the network id
            is given then only the subnet will be created if the network
            does not has any and then the port under a subnet is created
        @param network_id: network to create the subnet and port,
            if not given a new network will be created
        @type network_id: string
        @param name: start name label
        @type name: string
        @param ip_version: subnet ip version (if created)
        @type ip_version: int
        @param raise_exception: if there is an unsuccesfull call raise an
            exception
        @type raise_exception: bool (True/False)
        @return: network, subnet and port entities if the create and get calls
            were as expected and/or with None values if a resource create/get
            was unsuccessful and the raise exception flag is False
        @rtype: tuple
        """
        # Get or Create network depending if the network id is given
        if network_id:
            get_network = self.networks_behaviors.get_network(
                network_id=network_id)

            if get_network.response:
                network = get_network.response.entity
            elif raise_exception:
                raise NetworkGETException(get_network.failures)
            else:
                return (None, None, None)
        else:
            create_network = self.networks_behaviors.create_network(
                name=name, raise_exception=raise_exception)

            if not create_network.response:
                return (None, None, None)
            network = create_network.response.entity

        # Create a Subnet if needed
        subnet = None
        if not network.subnets:
            create_subnet = self.subnets_behaviors.create_subnet(
                network_id=network.id, name=name, ip_version=ip_version,
                raise_exception=raise_exception)

            # Return only the network if the subnet create was unsuccessful
            # and the raise_exception flag is False
            if not create_subnet.response:
                return (network, None, None)
            subnet = create_subnet.response.entity

        # Create the port
        create_port = self.ports_behaviors.create_port(
            network_id=network.id, name=name,
            raise_exception=raise_exception)

        # Return the network and subnet (if created) if the port create was
        # unsuccessful and the raise_exception flag is False
        if not create_port.response:
            return (network, subnet, None)
        port = create_port.response.entity

        # Get the port subnet, needed since subnet will not
        # always be created or the network used may have multiple subnets
        subnet_id = self.get_port_subnet_id(port)
        resp = self.subnets_behaviors.client.get_subnet(
            subnet_id=subnet_id)

        err_msg = 'Subnet Get failure'
        resp_check = self.check_response(resp=resp,
            status_code=NeutronResponseCodes.GET_SUBNET, label=subnet_id,
            message=err_msg, network_id=network_id)

        if not resp_check:
            subnet = resp.entity
            return (network, subnet, port)
        elif raise_exception:
            raise SubnetGETException(resp_check)
        else:
            return (network, None, port)

    def wait_for_status(self, resource_entity, new_status, timeout=None,
                        poll_interval=None):
        """
        @summary: Check a new status is reached by an entity object
        @param resource_entity: entity object like Network and Port
        @type resource_entity: Network or Port entity object (may be extended
            to other types with the status attribute)
        @param new_status: expected new status, like ACTIVE for ex.
        @type new_status: string
        @param timeout: seconds to wait for the new status
        @type timeout: int
        @param poll_interval: seconds between API calls
        @type poll_interval: int
        @return: True or False depending if the new status was reached
            within the expected timeout
        @rtype: bool
        """

        resource_type = type(resource_entity)

        # Subnets do NOT have a status attribute
        if resource_type == Network:
            client_call = self.networks_client.get_network
        elif resource_type == Port:
            client_call = self.ports_client.get_port
        else:
            msg = 'Entity type {0} NOT supported'.format(resource_type)
            raise UnsupportedTypeException(msg)

        entity_id = resource_entity.id
        initial_status = resource_entity.status
        timeout = timeout or self.config.resource_change_status_timeout
        poll_interval = poll_interval or self.config.api_poll_interval
        endtime = time.time() + int(timeout)

        log_msg = ('Checking {resource} entity type initial {init_status} '
                   'status is updated to {updated_status} status within a '
                   'timeout of {timeout}').format(resource=resource_type,
                       init_status=initial_status, updated_status=new_status,
                       timeout=timeout)
        self._log.info(log_msg)

        while time.time() < endtime:
            resp = client_call(entity_id)
            if resp.ok and resp.entity and resp.entity.status == new_status:
                return True
            time.sleep(poll_interval)
        return False

    def get_networks_format(self, network_ids=None, port_ids=None):
        """
        @summary: Formats network and port Ids in a list of dicts, for ex.
            [{"port": "1db5a0f3-54c4-4231-a10a-8abf48faf81b"},
            {"uuid": "00000000-0000-0000-0000-000000000000"},
            {"uuid": "11111111-1111-1111-1111-111111111111"}]
        @param network_ids: Network uuids
        @type network_ids: list(str)
        @param port_ids: Port uuids
        @type port_ids: list(str)
        @return: networks format for create server method calls
        @rtype: list(dict)
        """
        networks = []
        if network_ids:
            nets = [{'uuid': network_id} for network_id in network_ids]
            networks.extend(nets)
        if port_ids:
            ports = [{'port': port_id} for port_id in port_ids]
            networks.extend(ports)
        return networks

    # Compute related methods require the networking use_compute_api config
    # file param set to True and the compute_endpoint params
    def create_networking_server(
            self, name=None, image_ref=None, flavor_ref=None,
            personality=None, user_data=None, metadata=None, accessIPv4=None,
            accessIPv6=None, disk_config=None, networks=None, key_name=None,
            config_drive=None, scheduler_hints=None, admin_pass=None,
            block_device_mapping=None, security_groups=None,
            active_server=True, network_ids=None, port_ids=None):
        """
        @summary: Creates a server calling the servers_api behavior methods
            create_server_with_defaults or create_active_server based on the
            active_server flag. Also, can take as input network and/or port
            uuids instead of the networks list(dict)
        @param name: Name of the server
        @type name: str
        @param image_ref: Image uuid to build the server.
        @type image_ref: str
        @param flavor_ref: The flavor used to build the server.
        @type flavor_ref: str
        @param personality: Files to be injected into the server.
        @type personality: list(dict)
        @param user_data: Configuration info or scripts to use upon launch.
        @type user_data: str  (Must be Base64 encoded)
        @param metadata: key/values to be used as metadata (limit is 5).
        @type metadata: dict
        @param accessIPv4: IPv4 address for the server.
        @type accessIPv4: str
        @param accessIPv6: IPv6 address for the server.
        @type accessIPv6: str
        @param disk_config: MANUAL/AUTO/None
        @type disk_config: str
        @param networks: Server NICs specified by network and/or port uuids.
        @type networks: list(dict)
        @param key_name: Key name of keypair that created earlier (keypair-add)
        @type key_name: str
        @param config_drive: Config Drive flag
        @type config_drive: str
        @param scheduler_hints: nova scheduler hints.
        @type scheduler_hints: dict
        @param admin_pass: admn password for server.
        @type admin_pass: str
        @param block_device_mapping: fields to boot from a volume.
        @type block_device_mapping: dict
        @param security_groups: security groups names
        @type security_groups: list(dict) for ex. [{"name": secgroup.name}]
        @param active_server: Flag for making the create_active_server call.
        @type active_server: bool
        @param network_ids: Server network ids (replaces the networks param).
        @type network_ids: list
        @param port_ids: Server network port ids (replaces the networks param).
        @type port_ids: list
        @return: Response object with server entity object
        @rtype: requests.models.Response
        """
        if self.compute is None:
            raise UnavailableComputeInteractionException

        if active_server:
            create_server = (
                self.compute.servers.behaviors.create_active_server)
        else:
            create_server = (
                self.compute.servers.behaviors.create_server_with_defaults)

        if network_ids or port_ids:
            networks = self.get_networks_format(network_ids=network_ids,
                                                port_ids=port_ids)

        resp = create_server(
            name=name, image_ref=image_ref, flavor_ref=flavor_ref,
            personality=personality, config_drive=config_drive,
            metadata=metadata, accessIPv4=accessIPv4, accessIPv6=accessIPv6,
            disk_config=disk_config, networks=networks,
            scheduler_hints=scheduler_hints, user_data=user_data,
            admin_pass=admin_pass, key_name=key_name,
            block_device_mapping=block_device_mapping,
            security_groups=security_groups)

        # The compute behavior verifies the response, no need to check
        return resp

    def wait_for_servers_to_be_deleted(self, server_id_list,
                                       interval_time=None, timeout=None,
                                       raise_exception=False):
        """
        @summary: Waits for multiple servers to be deleted
        @param server_id_list: The uuids of the servers to be deleted
        @type server_id_list: List
        @param interval_time: Seconds to wait between polling
        @type interval_time: Integer
        @param timeout: The amount of time in seconds to wait before aborting
        @type timeout: Integer
        """

        interval_time = (interval_time or
                         self.compute.servers.config.server_status_interval)
        timeout = timeout or self.compute.servers.config.server_build_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            for server_id in server_id_list:
                self.compute.servers.client.delete_server(server_id)
            for server_id in server_id_list:
                try:
                    resp = self.compute.servers.client.get_server(server_id)
                    if (resp.status_code == ComputeResponseCodes.NOT_FOUND
                            and server_id in server_id_list):
                        server_id_list.remove(server_id)
                except ItemNotFound:
                    if server_id in server_id_list:
                        server_id_list.remove(server_id)
            if not server_id_list:
                break
            time.sleep(interval_time)
        else:
            msg = ('wait_for_servers_to_be_deleted {0} seconds timeout waiting'
                   'for the expected get_server HTTP {1} status code for '
                   'servers: {2}').format(timeout,
                                          ComputeResponseCodes.NOT_FOUND,
                                          server_id_list)
            self._log.info(msg)
            if raise_exception:
                raise TimeoutException(msg)
