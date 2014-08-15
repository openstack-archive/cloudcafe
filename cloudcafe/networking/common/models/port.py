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


class Port(AutoMarshallingModel):
    """Port model object for the OpenStack Neutron v2.0 API

    @param string id: UUID for the port (CRUD: R)
    @param string network_id: network port is associated with (CRUD: CR)
    @param string name: human readable name for the port,
        may not be unique. (CRUD: CRU)
    @param bool admin_state_up: true or false (default true), the admin state
        of the port. If down, the port does not forward packets (CRUD: CRU)
    @param string status: Indicates if the port is currently
        operational. Possible values: ACTIVE, DOWN, BUILD, ERROR (CRUD: R)
    @param string mac_address: mac address to use on the port (CRUD: CR)
    @param list(dict) fixed_ips: ip addresses for the port associating the
        port with the subnets where the IPs come from (CRUD: CRU)
    @param string device_id: id of device using this port (CRUD: CRUD)
    @param string device_owner: entity using this port (ex. dhcp agent,
        CRUD: CRUD)
    @param string tenant_id: owner of the port (CRUD: CR)
    @param list(dict) security_groups: ids of any security groups associated
        with the port (CRUD: CRUD)
    """

    def __init__(self, id_=None, network_id=None, name=None,
                 admin_state_up=None, status=None, mac_address=None,
                 fixed_ips=None, device_id=None, device_owner=None,
                 tenant_id=None, security_groups=None, **kwargs):

        # kwargs is to be used for extensions
        super(Port, self).__init__()
        self.id = id_
        self.network_id = network_id
        self.name = name
        self.admin_state_up = admin_state_up
        self.status = status
        self.mac_address = mac_address
        self.fixed_ips = fixed_ips
        self.device_id = device_id
        self.device_owner = device_owner
        self.tenant_id = tenant_id
        self.security_groups = security_groups

    # Serialization Functions
    def _obj_to_json(self):
        raise NotImplementedError

    def _obj_to_xml(self):
        raise NotImplementedError
