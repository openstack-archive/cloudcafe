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

from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.common.config import NetworkingBaseConfig
from cloudcafe.networking.networks.common.constants \
    import NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import NetworkGETException, SubnetGETException, UnsupportedTypeException
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

        log_msg = ('Checking {0} entity type initial {1} status is updated '
                   'to {2} status within a timeout of {3}').format(
                    resource_type, initial_status, new_status, timeout)
        self._log.info(log_msg)

        while time.time() < endtime:
            resp = client_call(entity_id)
            if resp.ok and resp.entity and resp.entity.status == new_status:
                return True
            time.sleep(poll_interval)
        return False
