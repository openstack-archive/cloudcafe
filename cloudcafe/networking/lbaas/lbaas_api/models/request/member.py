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

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.networking.lbaas.common.constants import Constants


class CreateMember(AutoMarshallingModel):
    """ Create Member Request Model
    @summary: An object that represents the the request data of a Member.
        Members are individual backend services which are being load balanced.
        Usually these would be web application servers. They are represented
        as a pool, IP address, Layer 4 port tuple.

    json ex:
        {
            "member": {
                "subnet_id": "SUBNET_ID",
                "tenant_id": "453105b9-1754-413f-aab1-55f1af620750",
                "address": "192.0.2.14",
                "protocol_port": 8080,
                "weight": 7,
                "admin_state_up": false
            }
        }

    xml ex:
        <member xmlns=""
            subnet_id="SUBNET_ID"
            tenant_id="453105b9-1754-413f-aab1-55f1af620750"
            address="192.0.2.14"
            protocol_port="8080"
            weight="7"
            admin_state_up="false"
        />

    """

    ROOT_TAG = 'member'

    def __init__(self, subnet_id, tenant_id, address, protocol_port,
                 weight=None, admin_state_up=None):
        """
        @summary:  Create Member Object Model
        @param subnet_id: Subnet in which to access this member.
        @type subnet_id: str
        @param tenant_id: Tenant to which this member is owned.
        @type tenant_id: str
        @param address: IP address of pool member.
        @type address: str
        @param protocol_port: TCP or UDP port
        @type protocol_port: int
        @param weight: Positive integer indicating relative portion of
            traffic from pool this member should receive (e.g., a member with
            a weight of 10 will receive five times as much traffic as a
            member with weight 2)
                Default: 1
        @type weight: int
        @param admin_state_up: If set to False, member will be created in an
            administratively down state
                Default: True
        @type admin_state_up: bool
        @return: Create Member Object
        @rtype: CreateMember
        """
        self.subnet_id = subnet_id
        self.tenant_id = tenant_id
        self.address = address
        self.protocol_port = protocol_port
        self.weight = weight
        self.admin_state_up = admin_state_up

    def _obj_to_json(self):
        body = {
            'subnet_id': self.subnet_id,
            'tenant_id': self.tenant_id,
            'address': self.address,
            'protocol_port': self.protocol_port,
            'weight': self.weight,
            'admin_state_up': self.admin_state_up
        }
        body = self._remove_empty_values(body)
        main_body = {self.ROOT_TAG: body}
        return json.dumps(main_body)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('subnet_id', self.subnet_id)
        element.set('tenant_id', self.tenant_id)
        element.set('address', self.address)
        element.set('protocol_port', str(self.protocol_port))
        if self.weight is not None:
            element.set('weight', str(self.weight))
        if self.admin_state_up is not None:
            element.set('admin_state_up', str(self.admin_state_up))
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml


class UpdateMember(AutoMarshallingModel):
    """ Update Member Request Model
    @summary: An object that represents the the request data of updating a
        Member.  This is used in updating an existing Member.

    json ex:
        {
            "member": {
                "weight": 7,
                "admin_state_up": false
            }
        }

    xml ex:
        <member xmlns=""
            weight="7"
            admin_state_up="False" />

    """

    ROOT_TAG = CreateMember.ROOT_TAG

    def __init__(self, weight=None, admin_state_up=None):
        self.weight = weight
        self.admin_state_up = admin_state_up
        self.attr_dict = {
            'weight': self.weight,
            'admin_state_up': self.admin_state_up
        }

    def _obj_to_json(self):
        body = self._remove_empty_values(self.attr_dict)
        return json.dumps({self.ROOT_TAG: body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element_dict = self.attr_dict
        # cast non-strings into strings
        element_dict['weight'] = str(element_dict['weight'])
        element_dict['admin_state_up'] = str(element_dict['admin_state_up'])
        element = self._set_xml_etree_element(element, element_dict)
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml
