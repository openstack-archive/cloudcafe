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

from cafe.engine.models.base import AutoMarshallingModel


class Subnet(AutoMarshallingModel):
    """Subnet model object for the OpenStack Neutron v2.0 API

    @param string id: UUID for the subnet (CRUD: R)
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
    @param list(dict) allocation_pools: sub range of cidr available for dynamic
        allocation to ports (CRUD: CR)
    @param list(dict) host_routes: routes that should be used by devices with
        IPs from this subnet (does not includes the local route, CRUD: CRU)
    @param bool enable_dhcp: whether DHCP is enabled (CRUD:CRU)
    """

    def __init__(self, id_=None, name=None, tenant_id=None, network_id=None,
                 ip_version=None, cidr=None, gateway_ip=None,
                 dns_nameservers=None, allocation_pools=None,
                 host_routes=None, enable_dhcp=None, **kwargs):

        # kwargs is to be used for extensions
        super(Subnet, self).__init__()
        self.id = id_
        self.name = name
        self.tenant_id = tenant_id
        self.network_id = network_id
        self.ip_version = ip_version
        self.cidr = cidr
        self.gateway_ip = gateway_ip
        self.dns_nameservers = dns_nameservers
        self.allocation_pools = allocation_pools
        self.host_routes = host_routes
        self.enable_dhcp = enable_dhcp

    # Serialization Functions
    def _obj_to_json(self):
        raise NotImplementedError

    def _obj_to_xml(self):
        raise NotImplementedError
