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

@summary: Health monitors describe the probes that are used to determine the
    health of pool members.

HealthMonitor Response Model
HealthMonitors Response Model
"""

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel
from cloudcafe.networking.lbaas.common.constants import Constants


class HealthMonitors(AutoMarshallingListModel):
    """HealthMonitors Response Model
    @summary: Response Model for a List of HealthMonitor Objects
    @note:  Returns a list of elements of type "HealthMonitor"

    json ex:
        {
            "healthmonitors": [
                {
                    "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                    "type": "HTTP",
                    "tenant_id": "453105b9-1754-413f-aab1-55f1af620750",
                    "delay": 20,
                    "timeout": 10,
                    "max_retries": 5,
                    "url_path": "/check",
                    "expected_codes": "200-299",
                    "admin_state_up": false,
                    "status": "ACTIVE"
                }
            ]
        }

    xml ex:
        <healthmonitors xmlns="">
            <healthmonitor xmlns=""
                id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
                type="HTTP"
                tenant_id="453105b9-1754-413f-aab1-55f1af620750"
                delay="20"
                timeout="10"
                max_retries="5"
                url_path="/check"
                expected_codes="200-299"
                admin_state_up="false"
                status="ACTIVE"
            />
        </healthmonitors>
    """
    ROOT_TAG = 'healthmonitors'

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, healthmonitors_dict_list):
        healthmonitors = HealthMonitors()
        healthmonitors.extend([HealthMonitor._dict_to_obj(healthmonitor) for
                               healthmonitor in healthmonitors_dict_list])
        return healthmonitors

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(HealthMonitor.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        healthmonitors = HealthMonitors()
        healthmonitors.extend(
            [HealthMonitor._xml_ele_to_obj(healthmonitors_ele)
             for healthmonitors_ele in xml_list])
        return healthmonitors


class HealthMonitor(AutoMarshallingModel):
    """HealthMonitor Response Model
    @summary: Response Model for a HealthMonitor
    @note: Represents a single HealthMonitor object

    json ex:
        {
            "healthmonitor": {
                "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                "type": "HTTP",
                "tenant_id": "453105b9-1754-413f-aab1-55f1af620750",
                "delay": 20,
                "timeout": 10,
                "max_retries": 5,
                "url_path": "/check",
                "expected_codes": "200-299",
                "admin_state_up": false,
                "status": "ACTIVE"
            }
        }

    xml ex:
        <healthmonitor xmlns=""
            id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
            type="HTTP"
            tenant_id="453105b9-1754-413f-aab1-55f1af620750"
            delay="20"
            timeout="10"
            max_retries="5"
            url_path="/check"
            expected_codes="200-299"
            admin_state_up="false"
            status="ACTIVE"
        />
    """

    ROOT_TAG = 'healthmonitor'

    def __init__(self, id_=None, type_=None, tenant_id=None, delay=None,
                 timeout=None, max_retries=None, url_path=None,
                 expected_codes=None, admin_state_up=None, status=None):
        super(HealthMonitor, self).__init__()
        self.id_ = id_
        self.type_ = type_
        self.tenant_id = tenant_id
        self.delay = delay
        self.timeout = timeout
        self.max_retries = max_retries
        self.url_path = url_path
        self.expected_codes = expected_codes
        self.admin_state_up = admin_state_up
        self.status = status

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._dict_to_obj(json_dict[cls.ROOT_TAG])

    @classmethod
    def _dict_to_obj(cls, healthmonitor_dict):
        healthmonitor = HealthMonitor(
            id_=healthmonitor_dict.get('id'),
            type_=healthmonitor_dict.get('type'),
            tenant_id=healthmonitor_dict.get('tenant_id'),
            delay=healthmonitor_dict.get('delay'),
            timeout=healthmonitor_dict.get('timeout'),
            max_retries=healthmonitor_dict.get('max_retries'),
            url_path=healthmonitor_dict.get('url_path'),
            expected_codes=healthmonitor_dict.get('expected_codes'),
            admin_state_up=healthmonitor_dict.get('admin_state_up'),
            status=healthmonitor_dict.get('status'))
        return healthmonitor

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        healthmonitor = cls._xml_ele_to_obj(element)
        return healthmonitor

    @classmethod
    def _xml_ele_to_obj(cls, element):
        healthmonitor_dict = element.attrib
        # Cast Integers
        if 'delay' in healthmonitor_dict:
            healthmonitor_dict['delay'] = (
                healthmonitor_dict.get('delay') and
                int(healthmonitor_dict.get('delay')))
        if 'timeout' in healthmonitor_dict:
            healthmonitor_dict['timeout'] = (
                healthmonitor_dict.get('timeout') and
                int(healthmonitor_dict.get('timeout')))
        if 'max_retries' in healthmonitor_dict:
            healthmonitor_dict['max_retries'] = (
                healthmonitor_dict.get('max_retries') and
                int(healthmonitor_dict.get('max_retries')))
        # Cast boolean
        if 'admin_state_up' in healthmonitor_dict:
            healthmonitor_dict['admin_state_up'] = cls._string_to_bool(
                healthmonitor_dict.get('admin_state_up'))
        healthmonitor = HealthMonitor(
            id_=healthmonitor_dict.get('id'),
            type_=healthmonitor_dict.get('type'),
            tenant_id=healthmonitor_dict.get('tenant_id'),
            delay=healthmonitor_dict.get('delay'),
            timeout=healthmonitor_dict.get('timeout'),
            max_retries=healthmonitor_dict.get('max_retries'),
            url_path=healthmonitor_dict.get('url_path'),
            expected_codes=healthmonitor_dict.get('expected_codes'),
            admin_state_up=healthmonitor_dict.get('admin_state_up'),
            status=healthmonitor_dict.get('status'))
        return healthmonitor
