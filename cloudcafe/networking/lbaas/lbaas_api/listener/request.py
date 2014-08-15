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


class CreateListener(AutoMarshallingModel):
    """ Create Listener Request Model
    @summary: An object that represents the the request data of a Listener.
        Listeners represent a single listening port and can optionally provide
        TLS termination.

    json ex:
        {
            "listener": {
                "name": "Example HTTPS Listener",
                "description": "A very simple example of an HTTPS listener.",
                "load_balancer_id": "b8a35470-f65d-11e3-a3ac-0800200c9a66",
                "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                "default_pool_id": "8311446e-8a13-4c00-95b3-03a92f9759c7",
                "connection_limit": 200,
                "protocol": "HTTPS",
                "protocol_port": "443",
                "tenant_id": "352686b7-c4b2-44ec-a458-84239713f685",
                "admin_state_up": true
            }
        }

    xml ex:
        <listener xmlns=""
            name="Example HTTPS Listener"
            description="A very simple example of an HTTPS listener."
            load_balancer_id="b8a35470-f65d-11e3-a3ac-0800200c9a66"
            tenant_id="7725fe12-1c14-4f45-ba8e-44bf01763578"
            default_pool_id="8311446e-8a13-4c00-95b3-03a92f9759c7"
            connection_limit="200"
            protocol="HTTPS"
            protocol_port="443"
            admin_state_up="true"
        </listener>

    """

    ROOT_TAG = 'listener'

    def __init__(self, name, load_balancer_id, tenant_id, default_pool_id,
                 protocol, protocol_port, description=None,
                 connection_limit=None, admin_state_up=None):
        """
        @summary: Create Listener Object Model
        @param name: Name of the listener that will be created
        @type name: String
        @param load_balancer_id:  ID of a load balancer.
        @type load_balancer_id: String
        @param tenant_id: Tenant that will own the listener.
        @type tenant_id: String
        @param default_pool_id: ID of default pool.  Must have compatible
            protocol with listener.
        @type default_pool_id: String
        @param protocol: Protocol to load balance: HTTP, HTTPS, TCP, UDP
        @type protocol: String
        @param protocol_port: TCP (or UDP) port to listen on.
        @type protocol_port: Integer
        @param description: Detailed description of the listener.
        @type description: String

        @param connection_limit: Maximum connections the load balancer can
            have.  Default is infinite.
        @type connection_limit: Integer
        @param admin_state_up: If set to false, listener will be created in an
            administratively down state
        @type admin_state_up: Boolean
        """
        self.name = name
        self.load_balancer_id = load_balancer_id
        self.tenant_id = tenant_id
        self.default_pool_id = default_pool_id
        self.protocol = protocol
        self.protocol_port = protocol_port
        self.description = description
        self.connection_limit = connection_limit
        self.admin_state_up = admin_state_up

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'load_balancer_id': self.load_balancer_id,
            'tenant_id': self.tenant_id,
            'default_pool_id': self.default_pool_id,
            'protocol': self.protocol,
            'protocol_port': self.protocol_port,
            'description': self.description,
            'connection_limit': self.connection_limit,
            'admin_state_up': self.admin_state_up
        }
        body = self._remove_empty_values(body)
        main_body = {self.ROOT_TAG: body}
        return json.dumps(main_body)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('name', self.name)
        element.set('load_balancer_id', self.load_balancer_id)
        element.set('tenant_id', self.tenant_id)
        element.set('default_pool_id', self.default_pool_id)
        element.set('protocol', self.protocol)
        element.set('protocol_port', str(self.protocol_port))
        if self.description is not None:
            element.set('description', self.description)
        if self.connection_limit is not None:
            element.set('connection_limit', str(self.connection_limit))
        if self.admin_state_up is not None:
            element.set('admin_state_up', str(self.admin_state_up))
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml


class UpdateListener(AutoMarshallingModel):
    """ Update Listener Request Model
    @summary: An object that represents the the request data of updating a
        Listener.  This is used in updating an existing Listener.

    json ex:
        {
            "listener": {
                "name": "an_updated-listener",
                "description": "A new very simple example load balancer."
                "default_pool_id": "8311446e-8a13-4c00-95b3-03a92f9759c7",
                "load_balancer_id": "updated-f65d-11e3-a3ac-0800200c9a66",
                "admin_state_up": false
            }
        }

    xml ex:
        <listener xmlns=""
            name="an_updated-listener"
            description="A new very simple example listener."
            default_pool_id="8311446e-8a13-4c00-95b3-03a92f9759c7"
            load_balancer_id="updated-f65d-11e3-a3ac-0800200c9a66"
            admin_state_up="False" />

    """

    ROOT_TAG = 'listener'

    def __init__(self, name=None, description=None, default_pool_id=None,
                 load_balancer_id=None, admin_state_up=None):
        self.name = name
        self.description = description
        self.default_pool_id = default_pool_id
        self.load_balancer_id = load_balancer_id
        self.admin_state_up = admin_state_up
        self.attr_dict = {
            'name': self.name,
            'description': self.description,
            'default_pool_id': self.default_pool_id,
            'load_balancer_id': self.load_balancer_id,
            'admin_state_up': self.admin_state_up
        }

    def _obj_to_json(self):
        body = self._remove_empty_values(deepcopy(self.attr_dict))
        return json.dumps({self.ROOT_TAG: body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        elements_dict = deepcopy(self.attr_dict)
        # cast non-strings into strings
        elements_dict['admin_state_up'] = str(self.admin_state_up)
        element = self._set_xml_etree_element(element, elements_dict)
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml
