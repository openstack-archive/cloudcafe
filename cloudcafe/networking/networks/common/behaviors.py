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

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.networking.networks.common.exceptions \
    import UnsupportedTypeException


class NetworksCommonBehaviors(BaseBehavior):
    """All API behaviors for helper methods"""

    def __init__(self, networks_behaviors, subnets_behaviors, ports_behaviors,
                 parent_behaviors):
        super(NetworksCommonBehaviors, self).__init__()
        self.networks_behaviors = networks_behaviors
        self.subnets_behaviors = subnets_behaviors
        self.ports_behaviors = ports_behaviors
        self.parent_behaviors = parent_behaviors

    def create_network_subnet_port(self, network_id=None, name=None,
                                   ip_version=None):
        """
        @summary: Creates a network with subnet and port, if the network id
            is given then only the subnet and port under it are created
        @param string network_id: network to create the subnet and port,
            if not given a new network will be created
        @param string name: start name label
        @param int ip_version: subnet ip version
        @return: tuple with network, subnet and port entities or None if
            the creates were unsuccessful
        """
        # Get network entity or create if network id is None
        if network_id:
            network = self.networks_behaviors.client.get_network(
                network_id=network_id).entity
        else:
            network = self.networks_behaviors.create_network(
                name=name, raise_exception=False)

        if network:
            subnet = self.subnets_behaviors.create_subnet(
                network_id=network.id, name=name, ip_version=ip_version,
                raise_exception=False)
        else:
            return None
        if subnet:
            port = self.ports_behaviors.create_port(
                network_id=network.id, name=name, raise_exception=False)
        else:
            return None
        if port:
            return network, subnet, port
        else:
            return None
