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

import json

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.networking.networks.extensions.floating_ips.constants \
    import COMMON_ROOT_TAG

class FloatingIPRequest(AutoMarshallingModel):
    """
    Model for associating the floating IP with an internal port.
    """
    ROOT_TAG = COMMON_ROOT_TAG

    def __init__(self, floating_network_id, tenant_id=None,
                 fixed_ip_address=None, floating_ip_address=None,
                 port_id=None):
        """
        Constructor for Floating IP Request Model

        :param floating_network_id: (UUID) - The ID of the network associated
             with the floating IP

        :param tenant_id: (UUID) - The tenant id. [OPTIONAL]
        :param fixed_ip_address: (string) - The fixed IP address associated
             with the floating IP. If you intend to associate the floating IP
             with a fixed IP at creation time, then you must indicate the
             identifier of the internal port. If an internal port has multiple
             associated IP addresses, the service chooses the first IP unless
             you explicitly specify the parameter fixed_ip_address to select
             a specific IP. [OPTIONAL]
        :param floating_ip_address: (string) The floating IP address [OPTIONAL]
        :param port_id: (UUID) The port ID [OPTIONAL]

        :return: None
        """
        super(FloatingIPRequest, self).__init__()
        self.floating_network_id = floating_network_id
        self.floating_ip_address = floating_ip_address
        self.tenant_id = tenant_id
        self.fixed_ip_address = fixed_ip_address
        self.port_id = port_id

    def _obj_to_json(self):
        """ Serializes instantiated object into JSON representation """
        obj_content = {
            'floating_network_id': self.floating_network_id,
            'floating_ip_address': self.floating_ip_address,
            'tenant_id': self.tenant_id,
            'fixed_ip_address': self.fixed_ip_address,
            'port_id': self.port_id,
        }

        # Build request JSON payload, while removing unset optional params
        request_content = {
            self.ROOT_TAG: self._remove_empty_values(obj_content)
        }

        return json.dumps(request_content)


class FloatingIPUpdate(AutoMarshallingModel):
    """
    Model for updating the floating IP associated with an internal port.
    """
    ROOT_TAG = COMMON_ROOT_TAG

    def __init__(self, port_id):
        """
        Constructor for Floating IP Update Model

        :param port_id: (UUID) The port ID
        :return: None
        """
        super(FloatingIPUpdate, self).__init__()
        self.port_id = port_id

    def _obj_to_json(self):
        """ Serializes instantiated object into JSON representation """
        obj_content = {'port_id': self.port_id}

        # Build request JSON payload, while removing unset optional params
        request_content = {
            self.ROOT_TAG: self._remove_empty_values(obj_content)
        }

        return json.dumps(request_content)
