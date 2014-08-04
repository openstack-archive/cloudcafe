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

@summary: Members are individual backend services which are being
    load balanced. Usually these would be web application servers.
    They are represented as a pool, IP address, Layer 4 port tuple.

Member Response Model
Members Response Model
"""

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel
from cloudcafe.networking.lbaas.common.constants import Constants


class Members(AutoMarshallingListModel):
    """Members Response Model
    @summary: Response Model for a List of Member Objects
    @note:  Returns a list of elements of type "Member"

    json ex:
        {
            "members": [
                {
                    "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                    "subnet_id": "SUBNET_ID",
                    "tenant_id": "453105b9-1754-413f-aab1-55f1af620750",
                    "address": "192.0.2.14",
                    "protocol_port": 8080,
                    "weight": 7,
                    "admin_state_up": false,
                    "status": "ACTIVE"
                }
            ]
        }

    xml ex:
        <members xmlns="">
            <member xmlns=""
                id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
                subnet_id="SUBNET_ID"
                tenant_id="453105b9-1754-413f-aab1-55f1af620750"
                address="192.0.2.14"
                protocol_port="8080"
                weight="7"
                admin_state_up="false"
                status="ACTIVE"
            />
        </loadbalancers>
    """
    ROOT_TAG = 'members'

    def __init__(self, members=None):
        super(Members, self).__init__()
        if members is None:
            members = []
        for member in members:
            self.append(member)

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, members_dict_list):
        members = Members()
        members.extend([Member._dict_to_obj(member) for
                        member in members_dict_list])
        return members

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Member.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        members = Members()
        members.extend(
            [Member._xml_ele_to_obj(members_ele)
             for members_ele in xml_list])
        return members


class Member(AutoMarshallingModel):
    """Member Response Model
    @summary: Response Model for a Member
    @note: Represents a single Member object

    json ex:
        {
            "member": {
                "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                "subnet_id": "SUBNET_ID",
                "tenant_id": "453105b9-1754-413f-aab1-55f1af620750",
                "address": "192.0.2.14",
                "protocol_port": 8080,
                "weight": 7,
                "admin_state_up": false
                "status": "ACTIVE"
            }
        }

    xml ex:
        <member xmlns=""
            id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
            subnet_id="SUBNET_ID"
            tenant_id="453105b9-1754-413f-aab1-55f1af620750"
            address="192.0.2.14"
            protocol_port="8080"
            weight="7"
            admin_state_up="false"
            status="ACTIVE"
        />
    """

    ROOT_TAG = 'member'

    def __init__(self, id_=None, subnet_id=None, tenant_id=None,
                 address=None, protocol_port=None, weight=None,
                 admin_state_up=None, status=None):
        super(Member, self).__init__()
        self.id_ = id_
        self.subnet_id = subnet_id
        self.tenant_id = tenant_id
        self.address = address
        self.protocol_port = protocol_port
        self.weight = weight
        self.admin_state_up = admin_state_up
        self.status = status

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._dict_to_obj(json_dict[cls.ROOT_TAG])

    @classmethod
    def _dict_to_obj(cls, member_dict):
        member = Member(
            id_=member_dict.get('id'),
            subnet_id=member_dict.get('subnet_id'),
            tenant_id=member_dict.get('tenant_id'),
            address=member_dict.get('address'),
            protocol_port=member_dict.get('protocol_port'),
            weight=member_dict.get('weight'),
            admin_state_up=member_dict.get('admin_state_up'),
            status=member_dict.get('status'))
        return member

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        member = cls._xml_ele_to_obj(element)
        return member

    @classmethod
    def _xml_ele_to_obj(cls, element):
        member_dict = element.attrib
        # Cast Integers
        if 'protocol_port' in member_dict:
            member_dict['protocol_port'] = (
                member_dict.get('protocol_port') and
                int(member_dict.get('protocol_port')))
        if 'weight' in member_dict:
            member_dict['weight'] = (
                member_dict.get('weight') and
                int(member_dict.get('weight')))
        # Cast boolean
        if 'admin_state_up' in member_dict:
            member_dict['admin_state_up'] = cls._string_to_bool(
                member_dict.get('admin_state_up'))
        member = Member(
            id_=member_dict.get('id'),
            subnet_id=member_dict.get('subnet_id'),
            tenant_id=member_dict.get('tenant_id'),
            address=member_dict.get('address'),
            protocol_port=member_dict.get('protocol_port'),
            weight=member_dict.get('weight'),
            admin_state_up=member_dict.get('admin_state_up'),
            status=member_dict.get('status'))
        return member
