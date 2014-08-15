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

import json
import xml.etree.ElementTree as ET

from cloudcafe.networking.common.models.subnet import Subnet


class SubnetRequest(Subnet):
    """Subnet model for creating (POST) and updating (PUT) networks"""

    def _obj_to_json(self):

        body = {
            'id': self.id,
            'name': self.name,
            'tenant_id': self.tenant_id,
            'network_id': self.network_id,
            'ip_version': self.ip_version,
            'cidr': self.cidr,
            'gateway_ip': self.gateway_ip,
            'dns_nameservers': self.dns_nameservers,
            'allocation_pools': self.allocation_pools,
            'host_routes': self.host_routes,
            'enable_dhcp': self.enable_dhcp
        }

        # The client should instantiate the model with only desired parameters
        body = self._remove_empty_values(body)
        main_body = {'subnet': body}
        return json.dumps(main_body)
