"""
Copyright 2013 Rackspace

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


class NetworksMockResponse(object):

    def __init__(self, format):
        self.format = format

    def _get_network(self):
        return getattr(self, '_{0}_network'.format(self.format))()

    def _json_network(self):
        return ('{"network":'
                '{"status": "ACTIVE",'
                '"subnets": ['
                '"efee1b83-0084-4a45-b676-38b554188f22"],'
                '"name": "nuevo_miguelito",'
                '"router:external": false,'
                '"tenant_id": "1ac35462fd5a43bf955ba307212930ac",'
                '"admin_state_up": false,'
                '"shared": false,'
                '"id": "97a5cb31-bdc4-48c0-b04f-34ab551053e1"}}')

    def _xml_network(self):
        return ('<?xml version="1.0" encoding="UTF-8" ?>'
                '<network>'
                '<status>ACTIVE</status>'
                '<subnets>'
                '<subnet>efee1b83-0084-4a45-b676-38b554188f22</subnet>'
                '</subnets>'
                '<name>nuevo_miguelito</name>'
                '<router:external>false</router:external>'
                '<tenant_id>1ac35462fd5a43bf955ba307212930ac</tenant_id>'
                '<admin_state_up>false</admin_state_up>'
                '<shared>false</shared>'
                '<id>97a5cb31-bdc4-48c0-b04f-34ab551053e1</id>'
                '</network>')


class ListNetworksMockResponse(object):

    def __init__(self, format):
        self.format = format

    def _get_network(self):
        return getattr(self, '_{0}_network'.format(self.format))()

    def _json_network(self):
        return ('{"networks": ['
                '{"status": "ACTIVE",'
                '"subnets": ['
                '"efee1b83-0084-4a45-b676-38b554188f22"],'
                '"name": "nuevo_miguelito",'
                '"router:external": false,'
                '"tenant_id": "1ac35462fd5a43bf955ba307212930ac",'
                '"admin_state_up": false,'
                '"shared": false,'
                '"id": "97a5cb31-bdc4-48c0-b04f-34ab551053e1"}]}')

    def _xml_network(self):
        return ('<?xml version="1.0" encoding="UTF-8" ?>'
                '<networks>'
                '<network>'
                '<status>ACTIVE</status>'
                '<subnets>'
                '<subnet>efee1b83-0084-4a45-b676-38b554188f22</subnet>'
                '</subnets>'
                '<name>nuevo_miguelito</name>'
                '<router:external>false</router:external>'
                '<tenant_id>1ac35462fd5a43bf955ba307212930ac</tenant_id>'
                '<admin_state_up>false</admin_state_up>'
                '<shared>false</shared>'
                '<id>97a5cb31-bdc4-48c0-b04f-34ab551053e1</id>'
                '<network>'
                '</networks>')


class SubnetsMockResponse(object):

    def __init__(self, format):
        self.format = format

    def _get_subnet(self):
        return getattr(self, '_{0}_subnet'.format(self.format))()

    def _json_subnet(self):
        return ('{"subnet":'
                '{"name": "nuevo_miguelito",'
                '"enable_dhcp": true,'
                '"network_id":'
                '"97a5cb31-bdc4-48c0-b04f-34ab551053e1",'
                '"tenant_id":'
                '"1ac35462fd5a43bf955ba307212930ac",'
                '"dns_nameservers": [],'
                '"gateway_ip": "10.0.1.1",'
                '"ipv6_ra_mode": null,'
                '"allocation_pools": ['
                '{"start": "10.0.1.2",'
                '"end": "10.0.1.254"}],'
                '"host_routes": ['
                '{"nexthop": "10.0.1.1",'
                '"destination": "100.0.0.0/24"}],'
                '"ip_version": 4,'
                '"ipv6_address_mode": null,'
                '"cidr": "10.0.1.0/24",'
                '"id": "efee1b83-0084-4a45-b676-38b554188f22"}}')

    def _xml_subnet(self):
        return ('<?xml version="1.0" encoding="UTF-8" ?>'
                '<subnet>'
                '<name>nuevo_miguelito</name>'
                '<enable_dhcp>true</enable_dhcp>'
                '<network_id>97a5cb31-bdc4-48c0-b04f-34ab551053e1</network_id>'
                '<tenant_id>1ac35462fd5a43bf955ba307212930ac</tenant_id>'
                '<gateway_ip>10.0.1.1</gateway_ip>'
                '<ipv6_ra_mode />'
                '<allocation_pools>'
                '<allocation_pool>'
                '<start>10.0.1.2</start>'
                '<end>10.0.1.254</end>'
                '</allocation_pool'
                '</allocation_pools>'
                '<host_routes>'
                '<host_route>'
                '<nexthop>10.0.1.1</nexthop>'
                '<destination>100.0.0.0/24</destination>'
                '</host_route>'
                '</host_routes>'
                '<ip_version>4</ip_version>'
                '<ipv6_address_mode/>'
                '<cidr>10.0.1.0/24</cidr>'
                '<id>efee1b83-0084-4a45-b676-38b554188f22</id>'
                '</subnet>')


class ListSubnetsMockResponse(object):

    def __init__(self, format):
        self.format = format

    def _get_subnet(self):
        return getattr(self, '_{0}_subnet'.format(self.format))()

    def _json_subnet(self):
        return ('{"subnets": ['
                '{"name": "nuevo_miguelito",'
                '"enable_dhcp": true,'
                '"network_id":'
                '"97a5cb31-bdc4-48c0-b04f-34ab551053e1",'
                '"tenant_id":'
                '"1ac35462fd5a43bf955ba307212930ac",'
                '"dns_nameservers": [],'
                '"gateway_ip": "10.0.1.1",'
                '"ipv6_ra_mode": null,'
                '"allocation_pools": ['
                '{"start": "10.0.1.2",'
                '"end": "10.0.1.254"}],'
                '"host_routes": ['
                '{"nexthop": "10.0.1.1",'
                '"destination": "100.0.0.0/24"}],'
                '"ip_version": 4,'
                '"ipv6_address_mode": null,'
                '"cidr": "10.0.1.0/24",'
                '"id": "efee1b83-0084-4a45-b676-38b554188f22"}]}')

    def _xml_subnet(self):
        return ('<?xml version="1.0" encoding="UTF-8" ?>'
                '<subnets>'
                '<subnet>'
                '<name>nuevo_miguelito</name>'
                '<enable_dhcp>true</enable_dhcp>'
                '<network_id>97a5cb31-bdc4-48c0-b04f-34ab551053e1</network_id>'
                '<tenant_id>1ac35462fd5a43bf955ba307212930ac</tenant_id>'
                '<gateway_ip>10.0.1.1</gateway_ip>'
                '<ipv6_ra_mode />'
                '<allocation_pools>'
                '<allocation_pool>'
                '<start>10.0.1.2</start>'
                '<end>10.0.1.254</end>'
                '</allocation_pool'
                '</allocation_pools>'
                '<host_routes>'
                '<host_route>'
                '<nexthop>10.0.1.1</nexthop>'
                '<destination>100.0.0.0/24</destination>'
                '</host_route>'
                '</host_routes>'
                '<ip_version>4</ip_version>'
                '<ipv6_address_mode/>'
                '<cidr>10.0.1.0/24</cidr>'
                '<id>efee1b83-0084-4a45-b676-38b554188f22</id>'
                '</subnet>'
                '</subnets>')


class PortsMockResponse(object):

    def __init__(self, format):
        self.format = format

    def _get_port(self):
        return getattr(self, '_{0}_port'.format(self.format))()

    def _json_port(self):
        return ('{"port":'
                '{"status": "DOWN",'
                '"name": "nuevo_miguelito",'
                '"allowed_address_pairs": [],'
                '"admin_state_up": false,'
                '"network_id": "97a5cb31-bdc4-48c0-b04f-34ab551053e1",'
                '"tenant_id": "1ac35462fd5a43bf955ba307212930ac",'
                '"extra_dhcp_opts": [],'
                '"binding:vnic_type": "normal",'
                '"device_owner": "",'
                '"mac_address": "fa:16:3e:da:68:96",'
                '"fixed_ips": ['
                '{"subnet_id": "efee1b83-0084-4a45-b676-38b554188f22",'
                '"ip_address": "10.0.1.25"}],'
                '"id": "25a658c7-4773-46ce-9bf3-52fc87176b07",'
                '"security_groups": ['
                '"dd01c7b8-d244-40a1-8369-bc0e0f0fa05a"],'
                '"device_id":""}}')

    def _xml_port(self):
        return ('<?xml version="1.0" encoding="UTF-8" ?>'
                '<port>'
                '<status>DOWN</status>'
                '<name>nuevo_miguelito</name>'
                '<admin_state_up>false</admin_state_up>'
                '<network_id>97a5cb31-bdc4-48c0-b04f-34ab551053e1</network_id>'
                '<tenant_id>1ac35462fd5a43bf955ba307212930ac</tenant_id>'
                '<binding:vnic_type>normal</binding:vnic_type>'
                '<device_owner></device_owner>'
                '<mac_address>fa:16:3e:da:68:96</mac_address>'
                '<fixed_ips>'
                '<fixed_ip>'
                '<subnet_id>efee1b83-0084-4a45-b676-38b554188f22</subnet_id>'
                '<ip_address>10.0.1.25</ip_address>'
                '</fixed_ip>'
                '</fixed_ips>'
                '<id>25a658c7-4773-46ce-9bf3-52fc87176b07</id>'
                '<security_groups>'
                '<security_group>'
                'dd01c7b8-d244-40a1-8369-bc0e0f0fa05a'
                '</security_group>'
                '</security_groups>'
                '<device_id></device_id>'
                '</port>')


class ListPortsMockResponse(object):

    def __init__(self, format):
        self.format = format

    def _get_port(self):
        return getattr(self, '_{0}_port'.format(self.format))()

    def _json_port(self):
        return ('{"ports": ['
                '{"status": "DOWN",'
                '"name": "nuevo_miguelito",'
                '"allowed_address_pairs": [],'
                '"admin_state_up": false,'
                '"network_id": "97a5cb31-bdc4-48c0-b04f-34ab551053e1",'
                '"tenant_id": "1ac35462fd5a43bf955ba307212930ac",'
                '"extra_dhcp_opts": [],'
                '"binding:vnic_type": "normal",'
                '"device_owner": "",'
                '"mac_address": "fa:16:3e:da:68:96",'
                '"fixed_ips": ['
                '{"subnet_id": "efee1b83-0084-4a45-b676-38b554188f22",'
                '"ip_address": "10.0.1.25"}],'
                '"id": "25a658c7-4773-46ce-9bf3-52fc87176b07",'
                '"security_groups": ['
                '"dd01c7b8-d244-40a1-8369-bc0e0f0fa05a"],'
                '"device_id":""}]}')

    def _xml_port(self):
        return ('<?xml version="1.0" encoding="UTF-8" ?>'
                '<ports>'
                '<port>'
                '<status>DOWN</status>'
                '<name>nuevo_miguelito</name>'
                '<admin_state_up>false</admin_state_up>'
                '<network_id>97a5cb31-bdc4-48c0-b04f-34ab551053e1</network_id>'
                '<tenant_id>1ac35462fd5a43bf955ba307212930ac</tenant_id>'
                '<binding:vnic_type>normal</binding:vnic_type>'
                '<device_owner></device_owner>'
                '<mac_address>fa:16:3e:da:68:96</mac_address>'
                '<fixed_ips>'
                '<fixed_ip>'
                '<subnet_id>efee1b83-0084-4a45-b676-38b554188f22</subnet_id>'
                '<ip_address>10.0.1.25</ip_address>'
                '</fixed_ip>'
                '</fixed_ips>'
                '<id>25a658c7-4773-46ce-9bf3-52fc87176b07</id>'
                '<security_groups>'
                '<security_group>'
                'dd01c7b8-d244-40a1-8369-bc0e0f0fa05a'
                '</security_group>'
                '</security_groups>'
                '<device_id></device_id>'
                '</port>'
                '</ports>')
