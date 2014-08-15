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

from cloudcafe.networking.common.models.network import Network


class NetworkRequest(Network):
    """Network model for creating (POST) and updating (PUT) networks"""

    def _obj_to_json(self):

        body = {
            'status': self.status,
            'shared': self.shared,
            'id': self.id,
            'tenant_id': self.tenant_id,
            'subnets': self.subnets,
            'name': self.name,
            'admin_state_up': self.admin_state_up
        }

        # The client should instantiate the model with only desired parameters
        body = self._remove_empty_values(body)
        main_body = {'network': body}
        return json.dumps(main_body)
