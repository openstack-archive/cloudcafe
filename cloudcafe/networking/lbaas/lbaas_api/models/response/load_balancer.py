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

LoadBalancer Response Model
LoadBalancers Response Model

@note:  A load balancer is a logical device which belongs to a cloud account.
    It is used to distribute workloads between multiple back-end systems or
    services, based on the criteria defined as part of its configuration.

    This model is used to provide detailed output for a specific
    load balancer configured and associated with your account.  This model
    is not capable of returning details for a load balancer which has
    been deleted.

"""

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel
from cloudcafe.networking.lbaas.common.constants import Constants


class LoadBalancers(AutoMarshallingListModel):
    """LoadBalancers Response Model
    @summary: Response Model for a List of LoadBalancer Objects
    @note:  Returns a list of elements of type "LoadBalancer"

    json ex:
        {
            "loadbalancers": [
                {
                    "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                    "name": "a-new-loadbalancer",
                    "description": "A very simple example load balancer.",
                    "vip_subnet": "SUBNET_ID",
                    "vip_address": "1.2.3.4",
                    "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                    "admin_state_up": true,
                    "status": "ACTIVE"
                }
            ]
        }

    xml ex:
        <loadbalancers xmlns="">
            <loadbalancer xmlns=""
                id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
                name="a-new-loadbalancer"
                description="A very simple example load balancer."
                vip_subnet="SUBNET_ID"
                vip_address="1.2.3.4"
                tenant_id="7725fe12-1c14-4f45-ba8e-44bf01763578"
                admin_state_up="True"
                status="ACTIVE"
            />
        </loadbalancers>
    """
    ROOT_TAG = 'loadbalancers'

    def __init__(self, load_balancers=None):
        super(LoadBalancers, self).__init__()
        if load_balancers is None:
            load_balancers = []
        for load_balancer in load_balancers:
            self.append(load_balancer)

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, load_balancers_dict_list):
        load_balancers = LoadBalancers()
        load_balancers.extend([LoadBalancer._dict_to_obj(load_balancer)
                               for load_balancer in load_balancers_dict_list])
        return load_balancers

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(LoadBalancer.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        load_balancers = LoadBalancers()
        load_balancers.extend(
            [LoadBalancer._xml_ele_to_obj(load_balancers_ele)
             for load_balancers_ele in xml_list])
        return load_balancers


class LoadBalancer(AutoMarshallingModel):
    """LoadBalancer Response Model
    @summary: Response Model for a Load Balancer
    @note: Represents a single LoadBalancer object

    json ex:
        {
            "loadbalancer": {
                "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                "name": "a-new-loadbalancer",
                "description": "A very simple example load balancer.",
                "vip_subnet": "SUBNET_ID",
                "vip_address": "1.2.3.4",
                "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                "admin_state_up": true,
                "status": "ACTIVE"
            }
        }

    xml ex:
        <loadbalancer xmlns=""
            id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
            name="a-new-loadbalancer"
            description="A very simple example load balancer."
            vip_subnet="SUBNET_ID"
            vip_address="1.2.3.4"
            tenant_id="7725fe12-1c14-4f45-ba8e-44bf01763578"
            admin_state_up="True"
            status="ACTIVE"
        />
    """

    ROOT_TAG = 'loadbalancer'

    def __init__(self, id_=None, name=None, description=None,
                 vip_subnet=None, vip_address=None, tenant_id=None,
                 admin_state_up=None, status=None):
        super(LoadBalancer, self).__init__()
        self.id_ = id_
        self.name = name
        self.description = description
        self.vip_subnet = vip_subnet
        self.vip_address = vip_address
        self.tenant_id = tenant_id
        self.admin_state_up = admin_state_up
        self.status = status

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._dict_to_obj(json_dict[cls.ROOT_TAG])

    @classmethod
    def _dict_to_obj(cls, load_balancer_dict):
        load_balancer = LoadBalancer(
            id_=load_balancer_dict.get('id'),
            name=load_balancer_dict.get('name'),
            description=load_balancer_dict.get('description'),
            vip_subnet=load_balancer_dict.get('vip_subnet'),
            vip_address=load_balancer_dict.get('vip_address'),
            tenant_id=load_balancer_dict.get('tenant_id'),
            admin_state_up=load_balancer_dict.get('admin_state_up'),
            status=load_balancer_dict.get('status'))
        return load_balancer

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        load_balancer = cls._xml_ele_to_obj(element)
        return load_balancer

    @classmethod
    def _xml_ele_to_obj(cls, element):
        load_balancer_dict = element.attrib
        # Cast boolean
        if 'admin_state_up' in load_balancer_dict:
            load_balancer_dict['admin_state_up'] = cls._string_to_bool(
                load_balancer_dict.get('admin_state_up'))
        load_balancer = LoadBalancer(
            id_=load_balancer_dict.get('id'),
            name=load_balancer_dict.get('name'),
            description=load_balancer_dict.get('description'),
            vip_subnet=load_balancer_dict.get('vip_subnet'),
            vip_address=load_balancer_dict.get('vip_address'),
            tenant_id=load_balancer_dict.get('tenant_id'),
            admin_state_up=load_balancer_dict.get('admin_state_up'),
            status=load_balancer_dict.get('status'))
        return load_balancer
