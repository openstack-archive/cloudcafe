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

from copy import deepcopy
import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.networking.lbaas.common.constants import Constants


class CreateHealthMonitor(AutoMarshallingModel):
    """ Create Health Monitor Request Model
    @summary: An object that represents the the request data of a
        Health Monitor.  Health monitors describe the probes that are used to
        determine the health of pool members.

    json ex:

        {
            "healthmonitor": {
                "type": "HTTP",
                "tenant_id": "453105b9-1754-413f-aab1-55f1af620750",
                "delay": 20,
                "timeout": 10,
                "max_retries": 5,
                "url_path": "/check",
                "expected_codes": "200-299",
                "admin_state_up": false
            }
        }

    xml ex:
        <healthmonitor xmlns=""
            type="HTTP"
            tenant_id="453105b9-1754-413f-aab1-55f1af620750"
            delay="20"
            timeout="10"
            max_retries="5"
            url_path="/check"
            expected_codes="200-299"
            admin_state_up="false"
        />

    """

    ROOT_TAG = 'healthmonitor'

    def __init__(self, type_, tenant_id, delay, timeout, max_retries,
                 http_method=None, url_path=None, expected_codes=None,
                 admin_state_up=None):
        """
        @summary: Create Health Monitor Object Model
        @param type_: Protocol used for health monitor.
            e.g., HTTP, HTTPS, TCP, PING
        @type type_: str
        @param tenant_id: Tenant that owns the health monitor.
        @type tenant_id: str
        @param delay: Time in seconds between probes.
        @type delay: int
        @param timeout: Time in seconds to timeout each probe.
        @type timeout: int
        @param max_retries: Maximum consecutive health probe tries.
        @type max_retries: int
        @param http_method: HTTP method monitor uses to make request.
            Default: "GET"
        @type http_method: str
        @param url_path: Path portion of URI that will be probed if
            type is HTTP(S).
                Default: "/"
        @type url_path: str
        @param expected_codes: Expected HTTP codes for a passing HTTP(S).
            Default: "200"
        @type expected_codes: str
        @param admin_state_up: Enabled or Disabled
            Default: "true"
        @type admin_state_up: bool
        @return: Create Health Monitor Object
        @rtype: CreateHealthMonitor
        """
        super(CreateHealthMonitor, self).__init__()
        self.type_ = type_
        self.tenant_id = tenant_id
        self.delay = delay
        self.timeout = timeout
        self.max_retries = max_retries
        self.http_method = http_method
        self.url_path = url_path
        self.expected_codes = expected_codes
        self.admin_state_up = admin_state_up
        self.attr_dict = {
            'type': self.type_,
            'tenant_id': self.tenant_id,
            'delay': self.delay,
            'timeout': self.timeout,
            'max_retries': self.max_retries,
            'http_method': self.http_method,
            'url_path': self.url_path,
            'expected_codes': self.expected_codes,
            'admin_state_up': self.admin_state_up
        }

    def _obj_to_json(self):
        body = self._remove_empty_values(deepcopy(self.attr_dict))
        main_body = {self.ROOT_TAG: body}
        return json.dumps(main_body)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        elements_dict = deepcopy(self.attr_dict)
        # cast non-strings into strings
        elements_dict['delay'] = str(self.delay)
        elements_dict['timeout'] = str(self.timeout)
        elements_dict['max_retries'] = str(self.max_retries)
        if self.http_method is not None:
            elements_dict['http_method'] = str(self.http_method)
        if self.url_path is not None:
            elements_dict['url_path'] = str(self.url_path)
        if self.expected_codes is not None:
            elements_dict['expected_codes'] = str(self.expected_codes)
        if self.admin_state_up is not None:
            elements_dict['admin_state_up'] = str(self.admin_state_up)
        element = self._set_xml_etree_element(element, elements_dict)
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml


class UpdateHealthMonitor(AutoMarshallingModel):
    """ Update Pool Request Model
    @summary: An object that represents the the request data of updating a
        Health Monitor.  This is used in updating an existing Health Monitor.

    json ex:
        {
            "healthmonitor": {
                "delay": 3,
                "path": "/healthcheck"
            }
        }

    xml ex:
        <healthmonitor xmlns=""
            delay="3"
            path="/healthcheck"
        />

    """

    ROOT_TAG = CreateHealthMonitor.ROOT_TAG

    def __init__(self, delay=None, timeout=None, max_retries=None,
                 http_method=None, url_path=None, expected_codes=None,
                 admin_state_up=None):
        super(UpdateHealthMonitor, self).__init__()
        self.delay = delay
        self.timeout = timeout
        self.max_retries = max_retries
        self.http_method = http_method
        self.url_path = url_path
        self.expected_codes = expected_codes
        self.admin_state_up = admin_state_up
        self.attr_dict = {
            'delay': self.delay,
            'timeout': self.timeout,
            'max_retries': self.max_retries,
            'http_method': self.http_method,
            'url_path': self.url_path,
            'expected_codes': self.expected_codes,
            'admin_state_up': self.admin_state_up
        }

    def _obj_to_json(self):
        body = self._remove_empty_values(deepcopy(self.attr_dict))
        main_body = {self.ROOT_TAG: body}
        return json.dumps(main_body)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        elements_dict = deepcopy(self.attr_dict)
        # cast non-strings into strings
        if self.delay is not None:
            elements_dict['delay'] = str(self.delay)
        if self.timeout is not None:
            elements_dict['timeout'] = str(self.timeout)
        if self.max_retries is not None:
            elements_dict['max_retries'] = str(self.max_retries)
        if self.admin_state_up is not None:
            elements_dict['admin_state_up'] = str(self.admin_state_up)
        element = self._set_xml_etree_element(element, elements_dict)
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml
