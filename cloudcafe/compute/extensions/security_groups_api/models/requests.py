"""
Copyright 2013 Rackspace

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
from cloudcafe.compute.common.constants import Constants


class CreateSecurityGroup(AutoMarshallingModel):

    def __init__(self, name=None, description=None):

        super(CreateSecurityGroup, self).__init__()
        self.name = name
        self.description = description

    def _obj_to_json(self):
        ret = {'security_group': self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        ret['name'] = self.name
        ret['description'] = self.description
        return ret

    def _obj_to_xml(self):
        raise NotImplemented

    def _obj_to_xml_ele(self):
        raise NotImplemented


class CreateSecurityGroupRule(AutoMarshallingModel):

    def __init__(self, from_port=None, ip_protocol=None,
                 to_port=None, parent_group_id=None,
                 cidr=None, group_id=None):

        self.from_port = from_port
        self.ip_protocol = ip_protocol
        self.to_port = to_port
        self.parent_group_id = parent_group_id
        self.cidr = cidr
        self.group_id = group_id

    def _obj_to_json(self):
        """
        @summary: Converts the object to json.
        """
        ret = {'security_group_rule': self.__dict__}
        print ret
        return json.dumps(ret)

    def _obj_to_xml(self):
        """
        @summary: Converts the object to xml.
        """
        xml = Constants.XML_HEADER
        element = ET.Element('security_group_rule')
        for key, value in self.__dict__.iteritems():
            child = ET.Element(key)
            child.text = str(value)
            element.append(child)
        xml += ET.tostring(element)
        return xml
