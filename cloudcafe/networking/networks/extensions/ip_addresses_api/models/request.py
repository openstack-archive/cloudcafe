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


class IPAddressRequest(AutoMarshallingModel):
    """
    @summary: IP Address model request object for the Shared IPs Rackspace
        Networking v2.0 API extension for creating (POST) and updating (PUT)
        IP addresses.
    @param network_id: network UUID to get the IP address from
    @type network_id: str
    @param version: IP address version 4 or 6
    @type version: int
    @param device_ids (optional): server UUIDs to add the IP address to their
        respective ports on the given network
    @type device_ids: list
    @param port_ids(optional): port UUIDs to add the IP address on the given
        network
    @type port_ids: list
    """

    def __init__(self, network_id=None, version=None, device_ids=None,
                 port_ids=None):
        super(IPAddressRequest, self).__init__()
        self.network_id = network_id
        self.version = version
        self.device_ids = device_ids
        self.port_ids = port_ids

    def _obj_to_json(self):

        body = {
            'network_id': self.network_id,
            'version': self.version,
            'device_ids': self.device_ids,
            'port_ids': self.port_ids
        }

        # Removing optional params not given
        body = self._remove_empty_values(body)
        main_body = {'ip_address': body}
        return json.dumps(main_body)
