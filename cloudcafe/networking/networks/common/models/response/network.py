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

import copy
import json

from cafe.engine.models.base import AutoMarshallingListModel, \
    AutoMarshallingModel


class Network(AutoMarshallingModel):
    """
    @summary: Network model object for the OpenStack Neutron v2.0 API
    responses for networks show and list (GET) calls
    @param id_: UUID for the network (CRUD: R)
    @type id_: string
    @param name: human readable name for the network, may not be unique
        (CRUD: CRU)
    @type name: string
    @param admin_state_up: true or false, the admin state of the network.
        If down, the network does not forward packets. Usually True (CRUD: CRU)
    @type admin_state_up: bool
    @param status: Indicates if the network is currently operational.
        Possible values: ACTIVE, DOWN, BUILD, ERROR. (CRUD: R)
    @type status: string
    @param subnets: associated network subnets UUID list. (CRUD: R)
    @type subnets: list(str)
    @param shared: specifies if the network can be accessed by any tenant.
        Usually False (CRUD: CRU)
    @type shared: bool
    @param tenant_id: owner of the network. (CRUD: CR)
    @type tenant_id: string
    """
    NETWORK = 'network'

    def __init__(self, id_=None, name=None, admin_state_up=None,
                 status=None, subnets=None, shared=None, tenant_id=None,
                 **kwargs):

        # kwargs is to be used for extensions or checking unexpected attrs
        super(Network, self).__init__()
        self.id = id_
        self.name = name
        self.admin_state_up = admin_state_up
        self.status = status
        self.subnets = subnets
        self.shared = shared
        self.tenant_id = tenant_id
        self.kwargs = kwargs

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Return network object from a JSON serialized string"""

        ret = None
        json_response = json.loads(serialized_str)

        # Creating a deep copy just in case later we want the original resp
        json_dict = copy.deepcopy(json_response)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_ or if they have a
        # special character within the name replacing it for an underscore too
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.NETWORK in json_dict:
            network_dict = json_dict.get(cls.NETWORK)
            ret = Network(**network_dict)
        return ret


class Networks(AutoMarshallingListModel):

    NETWORKS = 'networks'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Return a list of network objects from a JSON serialized string"""

        ret = cls()
        json_response = json.loads(serialized_str)

        # Creating a deep copy just in case later we want the original resp
        json_dict = copy.deepcopy(json_response)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_ or if they have a
        # special character within the name replacing it for an underscore too
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.NETWORKS in json_dict:
            networks = json_dict.get(cls.NETWORKS)
            for network in networks:
                ret.append(Network(**network))
        return ret
