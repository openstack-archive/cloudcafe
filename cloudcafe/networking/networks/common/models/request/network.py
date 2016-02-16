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

from cafe.engine.models.base import AutoMarshallingModel


class NetworkRequest(AutoMarshallingModel):
    """
    @summary: Network model object for the OpenStack Neutron v2.0 API
    requests for creating (POST) and updating (PUT) networks calls
    @param name: human readable name for the network, may not be unique
        (CRUD: CRU)
    @type name: string
    @param admin_state_up: true or false, the admin state of the network.
        If down, the network does not forward packets. Usually True (CRUD: CRU)
    @type admin_state_up: bool
    @param shared: specifies if the network can be accessed by any tenant.
        Usually False (CRUD: CRU)
    @type shared: bool
    @param tenant_id: owner of the network. (CRUD: CR)
    @type tenant_id: string
    """

    def __init__(self, name=None, admin_state_up=None, shared=None,
                 tenant_id=None, **kwargs):

        # kwargs is to be used for extensions
        super(NetworkRequest, self).__init__()
        self.name = name
        self.admin_state_up = admin_state_up
        self.shared = shared
        self.tenant_id = tenant_id

    def _obj_to_json(self):

        body = {
            'shared': self.shared,
            'tenant_id': self.tenant_id,
            'name': self.name,
            'admin_state_up': self.admin_state_up
        }

        # Removing optional params not given
        body = self._remove_empty_values(body)
        main_body = {'network': body}
        return json.dumps(main_body)
