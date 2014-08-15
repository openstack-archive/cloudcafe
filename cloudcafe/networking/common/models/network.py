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


class Network(AutoMarshallingModel):
    """Network model object for the OpenStack Neutron v2.0 API

    @param string id: UUID for the network (CRUD: R)
    @param string name: human readable name for the network,
        may not be unique. (CRUD: CRU)
    @param bool admin_state_up: true or false, the admin state
        of the network. If down, the network does not forward packets.
        Default value is True (CRUD: CRU)
    @param string status: Indicates if the network is currently
        operational. Possible values: ACTIVE, DOWN, BUILD, ERROR. (CRUD: R)
    @param list subnets: associated network subnets UUID list. (CRUD: R)
    @param bool shared: specifies if the network can be accessed by any
        tenant. Default value is False. (CRUD: CRU)
    @param string tenant_id: owner of the network. (CRUD: CR)
    """

    def __init__(self, id_=None, name=None, admin_state_up=None,
                 status=None, subnets=None, shared=None, tenant_id=None,
                 **kwargs):

        # kwargs is to be used for extensions
        super(Network, self).__init__()
        self.id = id_
        self.name = name
        self.admin_state_up = admin_state_up
        self.status = status
        self.subnets = subnets
        self.shared = shared
        self.tenant_id = tenant_id

    # Serialization Functions
    def _obj_to_json(self):
        raise NotImplementedError

    def _obj_to_xml(self):
        raise NotImplementedError
