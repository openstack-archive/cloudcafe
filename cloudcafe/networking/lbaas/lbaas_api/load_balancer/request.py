"""
Copyright 2014-2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@summary: Load balancer request models.

CreateLoadBalancer
UpdateLoadBalancer
"""

import json

from cafe.engine.models.base import AutoMarshallingModel


class CreateLoadBalancer(AutoMarshallingModel):
    """ Create Load Balancer Request Model
    @summary: An object that represents the the request data of a
        Load Balancer.  This is used in provisioning a new load balancer.

    json ex:
        {
            "loadbalancer": {
                "name": "a-new-loadbalancer",
                "description": "A very simple example load balancer.",
                "vip_subnet": "SUBNET_ID",
                "vip_address": "1.2.3.4",
                "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                "admin_state_up": true
            }
        }
    """

    ROOT_TAG = 'loadbalancer'

    def __init__(self, name, vip_subnet, tenant_id, admin_state_up=None,
                 description=None, vip_address=None):
        """
        @summary: Create Load Balancer Request Object Model
        @param name: Name of the load balancer.
        @type name: String
        @param vip_subnet: Subnet from which to allocate a virtual IP address.
        @type vip_subnet:  String
        @param tenant_id: Tenant that will own this load balancer.
        @type tenant_id: String
        @param admin_state_up: Defines whether an active load balancer is
            functioning or not
        @type admin_state_up: Boolean
        @param description: Detailed description of the load balancer.
        @type description: String
        @param vip_address: IP address to assign to VIP.
        @type vip_address: String
        @return: Create Load Balancer Request Object
        @rtype: CreateLoadBalancer
        """
        self.name = name
        self.vip_subnet = vip_subnet
        self.tenant_id = tenant_id
        self.admin_state_up = admin_state_up
        self.description = description
        self.vip_address = vip_address

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'vip_subnet': self.vip_subnet,
            'tenant_id': self.tenant_id,
            'admin_state_up': self.admin_state_up,
            'description': self.description,
            'vip_address': self.vip_address
        }
        body = self._remove_empty_values(body)
        main_body = {self.ROOT_TAG: body}
        return json.dumps(main_body)


class UpdateLoadBalancer(AutoMarshallingModel):
    """ Update Load Balancer Request Model
    @summary: An object that represents the the request data of updating a
        Load Balancer.  This is used in updating an existing load balancer.

    json ex:
        {
            "loadbalancer": {
                "name": "an_updated-loadbalancer",
                "description": "A new very simple example load balancer.",
                "admin_state_up": false
            }
        }
    """

    ROOT_TAG = CreateLoadBalancer.ROOT_TAG

    def __init__(self, name=None, description=None, admin_state_up=None):
        """
        @summary: Update Load Balancer Request Object Model
        @param name: Name of the load balancer.
        @type name: String
        @param description: Detailed description of the load balancer.
        @type description: String
        @param admin_state_up: Defines whether an active load balancer is
            functioning or not
        @type admin_state_up: Boolean
        @return: Update Load Balancer Request Object
        @rtype: UpdateLoadBalancer
        """
        self.name = name
        self.description = description
        self.admin_state_up = admin_state_up

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'description': self.description,
            'admin_state_up': self.admin_state_up
        }
        body = self._remove_empty_values(body)
        main_body = {self.ROOT_TAG: body}
        return json.dumps(main_body)
