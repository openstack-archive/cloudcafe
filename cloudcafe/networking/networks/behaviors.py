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

from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.compute.common.exceptions import TimeoutException
from cloudcafe.compute.composites import ComputeComposite
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.common.config import NetworkingBaseConfig
from cloudcafe.networking.networks.common.constants \
    import ComputeResponseCodes, ComputeStatus, NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import NetworkGETException, SubnetGETException, UnsupportedTypeException, \
    UnavailableComputeInteractionException, UnableToCreateKeypair, \
    UnableToDeleteKeypair, UnableToDeleteServer, UnableToGetKeypairs, \
    UnableToGetNetworkingServer, MissingDataException
from cloudcafe.networking.networks.common.models.response.network \
    import Network
from cloudcafe.networking.networks.common.models.response.port \
    import Port
from cloudcafe.networking.networks.extensions.ip_addresses_api.constants \
    import IPAddressesServerZone


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

        self.error_msg = ('{message}: {status} {reason} {content}. '
                          'Expected status code {expected_status}')

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
        resp_check = self.check_response(
            resp=resp, status_code=NeutronResponseCodes.GET_SUBNET,
            label=subnet_id, message=err_msg, network_id=network_id)

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
                                                  init_status=initial_status,
                                                  updated_status=new_status,
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

    def get_networking_server(self, server=None, server_id=None,
                              raise_exception=False):
        """
        @summary: takes a server entity or ID and returns its latest version
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        if server is None and server_id is None:
            raise UnableToGetNetworkingServer('Must provide server entity '
                                              'or server_id')

        net_server_id = getattr(server, 'id', None) or server_id
        msg = 'Getting server {0}'.format(net_server_id)
        self._log.info(msg)

        resp = self.compute.servers.client.get_server(net_server_id)
        resp_check = self.check_response(
            resp=resp, status_code=ComputeResponseCodes.GET_SERVER,
            label=net_server_id, message='Server GET failure')
        if resp_check and raise_exception:
            raise UnableToGetNetworkingServer(resp_check)

        if hasattr(server, 'admin_pass'):
            resp.entity.admin_pass = server.admin_pass
        return resp.entity

    def get_remote_instance_client(self, server, ip_address, private_key,
                                   ssh_username='root', auth_strategy='key'):
        """
        @summary: gets a compute server remote client
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        remote_client = (
            self.compute.servers.behaviors.get_remote_instance_client(
                server=server, ip_address=ip_address, username=ssh_username,
                key=private_key, auth_strategy=auth_strategy))
        return remote_client

    def list_servers(self, name=None, raise_exception=False):
        """
        @summary: list servers wrapper for networks
        @param name: name or name_starts_with* to filter by
        @type name: str
        @param raise_exception: flag to raise an exception if get fails
        @type raise_exception: bool
        @return: server entities list
        @rtype: list
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        self._log.info('Getting servers')
        resp = self.compute.servers.client.list_servers()
        resp_check = self.check_response(
            resp=resp, status_code=ComputeResponseCodes.GET_SERVER,
            label='Servers', message='LIST failure')
        if resp_check and raise_exception:
            raise UnableToGetNetworkingServer(resp_check)

        server_list = resp.entity
        if name and server_list:
            server_list = self.filter_entity_list_by_name(
                entity_list=server_list, name=name)
        return server_list

    def list_server_ids(self, name=None, raise_exception=False):
        """
        @summary: gets a server id list from a server entities list
        @param name: name or name_starts_with* to filter by
        @type name: str
        @param raise_exception: flag to raise an exception if get fails
        @type raise_exception: bool
        @return: server id list
        @rtype: list(str)
        """
        server_list = self.list_servers(name=name,
                                        raise_exception=raise_exception)
        server_ids = self.get_id_list_from_entity_list(entity_list=server_list)
        return server_ids

    def delete_servers(self, name=None, raise_exception=False):
        """
        @summary: deletes servers (all or filtered by name) without waiting
        @param name: name or name_starts_with* to filter by
        @type name: str
        @param raise_exception: flag to raise an exception if delete fails
        @type raise_exception: bool
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        server_ids = self.list_server_ids(name=name)
        log_msg = 'Deleting servers: {0}'.format(server_ids)
        self._log.info(log_msg)
        for server_id in server_ids:
            resp = self.compute.servers.client.delete_server(
                server_id=server_id)
            resp_check = self.check_response(
                resp=resp, status_code=ComputeResponseCodes.DELETE_SERVER,
                label=server_id, message='Server DELETE failure')
            if resp_check and raise_exception:
                raise UnableToDeleteServer(resp_check)

    def create_keypair(self, name='networks_keypair', raise_exception=False):
        """
        @summary: create keypair wrapper for networks
        @param name: starts with keypair name
        @type name: str
        @param raise_exception: flag to raise an exception if create fails
        @type raise_exception: bool
        @return: keypair
        @rtype: keypair entity object
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        # Using rand_name to avoid HTTP 409 Conflict due to duplicate names
        name = rand_name(name)
        log_msg = 'Creating test server keypair: {0}'.format(name)
        self._log.info(log_msg)
        resp = self.compute.keypairs.client.create_keypair(name)
        resp_check = self.check_response(
            resp=resp, status_code=ComputeResponseCodes.CREATE_KEYPAIR,
            label=name, message='Keypair POST failure')
        if resp_check and raise_exception:
            raise UnableToCreateKeypair(resp_check)
        return resp.entity

    def get_keypair(self, name, raise_exception=False):
        """
        @summary: get keypair wrapper for networks
        @param name: keypair name
        @type name: str
        @param raise_exception: flag to raise an exception if get fails
        @type raise_exception: bool
        @return: keypair
        @rtype: keypair entity object
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        log_msg = 'Getting keypair: {0}'.format(name)
        self._log.info(log_msg)
        resp = self.compute.keypairs.client.get_keypair(name)
        resp_check = self.check_response(
            resp=resp, status_code=ComputeResponseCodes.GET_KEYPAIR,
            label=name, message='Keypair GET failure')
        if resp_check and raise_exception:
            raise UnableToGetKeypairs(resp_check)
        return resp.entity

    def list_keypairs(self, name=None, raise_exception=False):
        """
        @summary: gets the keypairs (all or filtered by name)
        @param name: name or name_starts_with* to filter by
        @type name: str
        @param raise_exception: flag to raise an exception if get fails
        @type raise_exception: bool
        @return: keypair list
        @rtype: list
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        self._log.info('Getting keypairs')
        resp = self.compute.keypairs.client.list_keypairs()
        resp_check = self.check_response(
            resp=resp, status_code=ComputeResponseCodes.LIST_KEYPAIRS,
            label='Keypairs', message='LIST failure')
        if resp_check and raise_exception:
            raise UnableToGetKeypairs(resp_check)

        keypair_list = resp.entity
        if name and keypair_list:
            keypair_list = self.filter_entity_list_by_name(
                entity_list=keypair_list, name=name)
        return keypair_list

    def delete_keypairs(self, name=None, raise_exception=False):
        """
        @summary: deletes the keypairs (all or filtered by name)
        @param name: name or name_starts_with* to filter by
        @type name: str
        @param raise_exception: flag to raise an exception if delete fails
        @type raise_exception: bool
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        keypair_list = self.list_keypairs(name=name)
        log_msg = 'Deleting keypairs: {0}'.format(keypair_list)
        self._log.info(log_msg)
        failed_deletes = []
        if keypair_list:
            for key in keypair_list:
                resp = self.compute.keypairs.client.delete_keypair(key.name)
                resp_check = self.check_response(
                    resp=resp, status_code=ComputeResponseCodes.DELETE_KEYPAIR,
                    label=key.name, message='Keypair DELETE failure',
                    entity_check=False)
                if resp_check:
                    failed_deletes.append(resp_check)
                    if raise_exception:
                        raise UnableToDeleteKeypair(resp_check)

        return failed_deletes

    def wait_for_servers_to_be_active(self, server_id_list,
                                      interval_time=None, timeout=None,
                                      raise_exception=False):
        """
        @summary: Waits for multiple servers to be ACTIVE
        @param server_id_list: The uuids of the servers to wait for ACTIVE
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
                resp = self.compute.servers.client.get_server(server_id)
                if (resp.status_code == ComputeResponseCodes.GET_SERVER and
                        resp.entity.status == ComputeStatus.ACTIVE and
                        server_id in server_id_list):
                    server_id_list.remove(server_id)
            if not server_id_list:
                break
            time.sleep(interval_time)
        else:
            msg = ('wait_for_servers_to_be_active {0} seconds timeout waiting'
                   'for servers: {1}').format(timeout, server_id_list)
            self._log.info(msg)
            if raise_exception:
                raise TimeoutException(msg)

    def wait_for_servers_to_be_deleted(self, server_id_list=None, name=None,
                                       interval_time=None, timeout=None,
                                       raise_exception=False):
        """
        @summary: Waits for multiple servers to be deleted
        @param server_id_list: The uuids of the servers to be deleted
        @type server_id_list: List
        @param name: name or name_starts_with* to filter by
        @type name: str
        @param interval_time: Seconds to wait between polling
        @type interval_time: Integer
        @param timeout: The amount of time in seconds to wait before aborting
        @type timeout: Integer
        @param raise_exception: flag to raise an exception if delete fails
        @type raise_exception: bool
        """

        if self.compute is None:
            raise UnavailableComputeInteractionException

        if not server_id_list:
            if not name:
                raise MissingDataException('Missing name pattern')
            server_id_list = self.list_server_ids(name=name)
            log_msg = 'Deleting servers: {0}'.format(server_id_list)
            self._log.info(log_msg)

        failed_deletes = self._wait_for_compute_delete(
            resource_id_list=server_id_list, resource='servers',
            delete_method=self.compute.servers.client.delete_server,
            get_method=self.compute.servers.client.get_server,
            interval_time=interval_time, timeout=timeout,
            raise_exception=raise_exception)

        return failed_deletes

    def _wait_for_compute_delete(self, resource_id_list, resource,
                                 delete_method, get_method, interval_time=None,
                                 timeout=None, raise_exception=False):
        """
        @summary: Waits for compute resource deletes
        @param resource_id_list: uuids of the compute resources to be deleted
        @type resource_id_list: List
        @param resource: compute resource like servers, ip associations, etc.
        @type resource: String
        @param delete_method: method used to delete the resource
        @type delete_method: behavior or client method
        @param get_method: method used to get the resource
        @type get_method: behavior or client method
        @param interval_time: Seconds to wait between polling
        @type interval_time: Integer
        @param timeout: The amount of time in seconds to wait before aborting
        @type timeout: Integer
        @param raise_exception: flag to raise an exception if deletes fail
        @type raise_exception: bool
        """

        interval_time = (interval_time or
                         self.compute.servers.config.server_status_interval)
        timeout = timeout or self.compute.servers.config.server_build_timeout
        end_time = time.time() + timeout
        failed_deletes = []

        for resource_id in resource_id_list:
            delete_method(resource_id)

        while time.time() < end_time:
            for resource_id in resource_id_list:
                resp = get_method(resource_id)
                if (resp.status_code == ComputeResponseCodes.NOT_FOUND and
                        resource_id in resource_id_list):
                    resource_id_list.remove(resource_id)

                # Retrying to delete servers in ERROR status
                elif (hasattr(resp, 'entity') and
                        hasattr(resp.entity, 'status') and
                        resp.entity.status == ComputeStatus.ERROR):
                    delete_method(resource_id)

            if not resource_id_list:
                break
            time.sleep(interval_time)
        else:
            msg = ('Wait for compute {0} resource delete {1} seconds timeout '
                   'for the expected resource get HTTP {2} status code for '
                   'resources: {3}').format(resource, timeout,
                                            ComputeResponseCodes.NOT_FOUND,
                                            resource_id_list)
            self._log.info(msg)
            failed_deletes.append(msg)
            if raise_exception:
                raise TimeoutException(msg)

        # keeping the response consistent with the _delete_resources of the
        # networking.networks.common.behaviors (failed_deletes)
        return failed_deletes

    def create_multiple_servers(self, create_by='names', names=None,
                                images=None, flavors=None,
                                keypair_name=None, networks=None, ports=None,
                                pnet=True, snet=True, use_ip_zone_hint=False,
                                ip_zone_hint=None, ip_zone_hint_id=None,
                                raise_exception=False):
        """
        @summary: Create multiple test servers with the same keypairs and
                  networks given a list of names, image ids or flavor ids.
        @param create_by: type of list to create servers from
            (names, images or flavors)
        @type create_by: str
        @param names: list of names to create servers from
        @type names: list(str)
        @param images: image ids to create servers from
        @type images: list(str)
        @param flavors: list of flavor ids to create servers from
        @type flavors: list(str)
        @param keypair_name: (optional) keypair to create servers with
        @type keypair_name: str
        @param networks: (optional) isolated network ids to create servers with
        @type networks: list(str)
        @param ports: (optional) isolated ports ids to create servers with
        @type ports: list(str)
        @param pnet: flag to create server with public network
        @type pnet: bool
        @param snet: flag to create server with service (private) network
        @type snet: bool
        @param use_ip_zone_hint: flag to use scheduler hints with ip zone hint
            WARNING if using with create by flavors, make sure the flavors
            are within the same cell type.
        @type use_ip_zone_hint: bool
        @param ip_zone_hint: scheduler ip zone hint, for ex.
            public_ip_zone:near, public_ip_zone:far, different_host, etc.
        @type ip_zone_hint: str
        @param ip_zone_hint_id: id to use for the ip_zone_hint, for ex.
            server id or a public ip zone id
        @type ip_zone_hint_id: str
        @param raise_exception: flag to raise an exception if the wait for
            active servers times out
        @type raise_exception: bool
        @return: server entity objects
        @rtype: dict(server name: server entity object)
        """
        NAMES_CREATE_BY_TYPE = 'names'
        IMAGES_CREATE_BY_TYPE = 'images'
        FLAVORS_CREATE_BY_TYPE = 'flavors'
        CREATE_TYPES = [NAMES_CREATE_BY_TYPE, IMAGES_CREATE_BY_TYPE,
                        FLAVORS_CREATE_BY_TYPE]

        # Verify the create_by is withing the expected create types
        if create_by not in CREATE_TYPES:
            msg = 'Unsupported create_by: {0}. Expecting: {1}'.format(
                create_by, CREATE_TYPES)
            raise UnsupportedTypeException(msg)

        # Verifying the expected name or image id or flavor id list is given
        create_by_list = None
        if create_by == NAMES_CREATE_BY_TYPE and names:
            create_by_list = names
        elif create_by == IMAGES_CREATE_BY_TYPE and images:
            create_by_list = images
        elif create_by == FLAVORS_CREATE_BY_TYPE and flavors:
            create_by_list = flavors
        else:
            msg = 'Missing {0} list'.format(create_by)
            raise MissingDataException(msg)

        if type(create_by_list) != list:
            msg = 'Expecting a {0} list instead of: {1}'.format(create_by,
                                                                create_by_list)
            raise UnsupportedTypeException(msg)

        server_count = len(create_by_list)
        create_by_msg = 'Creating {0} servers from {1}: {2}'.format(
            server_count, create_by, create_by_list)
        self._log.info(create_by_msg)

        self._log.info('Defining the network IDs to be used')
        network_ids = []

        if pnet:
            network_ids.append(self.networks_config.public_network_id)
        if snet:
            network_ids.append(self.networks_config.service_network_id)
        if networks:
            network_ids.extend(networks)

        # Removing duplicates if any (in case networks had pnet or snet too)
        network_ids = list(set(network_ids))

        net_ids_msg = 'Creating servers with networks: {0}'.format(network_ids)
        self._log.info(net_ids_msg)

        # Setting the ip_zone_hint if the use_ip_zone_hint set to True
        scheduler_hints = None
        if use_ip_zone_hint:
            ip_zone_hint = ip_zone_hint or (
                IPAddressesServerZone.PUBLIC_IP_ZONE_NEAR)

            # Setting the scheduler hints if the ip_zone_hint_id given
            if ip_zone_hint_id:
                scheduler_hints = {ip_zone_hint: ip_zone_hint_id}

        # Response dict where the key will be the server name and the value the
        # server entity object
        servers = dict()
        server_ids = []
        for n, param in enumerate(create_by_list):
            server_name = '{0}_{1}_svr_{2}'.format(create_by, param, n+1)
            server_kwargs = dict(name=server_name, key_name=keypair_name,
                                 network_ids=network_ids, port_ids=ports,
                                 active_server=False)
            if create_by == IMAGES_CREATE_BY_TYPE:
                server_kwargs.update(image_ref=param)
            if create_by == FLAVORS_CREATE_BY_TYPE:
                server_kwargs.update(flavor_ref=param)
            if use_ip_zone_hint and scheduler_hints:
                server_kwargs.update(scheduler_hints=scheduler_hints)

            resp = self.create_networking_server(**server_kwargs)
            server = resp.entity
            server_ids.append(server.id)
            servers[server_name] = server

            # Setting the scheduler hints with the first server ID if the
            # ip_zone_hint_id was not given and the use_ip_zone_hint was set
            if use_ip_zone_hint and not scheduler_hints and n < 1:
                scheduler_hints = {ip_zone_hint: server.id}

        # Waiting for the servers to be active
        self.wait_for_servers_to_be_active(server_id_list=server_ids,
                                           raise_exception=raise_exception)

        # Updating the servers dict with the latest server entities
        # Hopefully in active status with all expected data
        for server_name, server in servers.items():
            updated_server = self.get_networking_server(server=server)
            servers[server_name] = updated_server

        return servers
