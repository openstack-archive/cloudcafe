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
from cloudcafe.networking.lbaas.lbaas_api.session_persistence.request \
    import SetSessionPersistence


class CreatePool(AutoMarshallingModel):
    """" Create Pool Request Model
    @summary: An object that represents the the request data of a Pool.
        Pools are groupings of backend member servers to which client requests
        are forwarded.

    json ex:
        {
            "pool": {
                "name": "Example HTTPS Pool",
                "description": "Example HTTPS Pool Description"
                "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                "protocol":	"HTTPS",
                "session_persistence": {
                    "type": "COOKIE",
                    "cookie_name": "session_persistence_cookie"
                },
                "lb_algorithm": "ROUND_ROBIN",
                "healthmonitor_id": "health_monitor_123",
                "admin_state_up": true
            }
        }

    xml ex:
        <pool xmlns=""
            name="Example HTTPS Listener"
            description="Example HTTPS Pool Description"
            tenant_id="7725fe12-1c14-4f45-ba8e-44bf01763578"
            protocol="HTTPS"
            lb_algorithm="ROUND_ROBIN"
            healthmonitor_id="health_monitor_123"
            admin_state_up="True" >
            <session_persistence
                type="COOKIE"
                cookie_name="session_persistence_cookie"
            />
        </pool>

    """

    ROOT_TAG = 'pool'

    def __init__(self, name, tenant_id, protocol, lb_algorithm,
                 description=None, session_persistence=None,
                 healthmonitor_id=None, admin_state_up=None):
        """
        @summary: Create Pool Object Model
        @param name: Name of the Pool that will be created
        @type name: str
        @param tenant_id:  Tenant that will own the pool.
        @type tenant_id: str
        @param protocol: Protocol use to connect to members: HTTP, HTTPS, TCP
        @type protocol: str
        @param lb_algorithm: round-robin, least-connections, etc. (load
            balancing provider dependent, but round-robin must be supported).
        @type lb_algorithm: str
        @param description: Description of a pool.
        @type description: str
        @param session_persistence: Session persistence algorithm that should
            be used (if any). This is a dictionary that has keys of
            "type" and "cookie_name".
                Default: {}
        @type session_persistence: dict
        @param healthmonitor_id: ID of existing health monitor.
            Default: null
        @type healthmonitor_id: str
        @param admin_state_up: Enabled or disabled.
        @type admin_state_up: bool
        """
        super(CreatePool, self).__init__()
        self.name = name
        self.tenant_id = tenant_id
        self.protocol = protocol
        self.lb_algorithm = lb_algorithm
        self.description = description
        self.session_persistence = session_persistence
        self.healthmonitor_id = healthmonitor_id
        self.admin_state_up = admin_state_up

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'tenant_id': self.tenant_id,
            'protocol': self.protocol,
            'lb_algorithm': self.lb_algorithm,
            'description': self.description,
            'session_persistence': self.session_persistence,
            'healthmonitor_id': self.healthmonitor_id,
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
        element.set('tenant_id', self.tenant_id)
        element.set('protocol', self.protocol)
        element.set('lb_algorithm', self.lb_algorithm)
        if self.description is not None:
            element.set('description', self.description)
        if self.session_persistence is not None:
            element.append(ET.fromstring(
                SetSessionPersistence(
                    type_=self.session_persistence.get('type'),
                    cookie_name=self.session_persistence.get('cookie_name')
                )._obj_to_xml()))
        if self.healthmonitor_id is not None:
            element.set('healthmonitor_id', self.healthmonitor_id)
        if self.admin_state_up is not None:
            element.set('admin_state_up', str(self.admin_state_up))
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml


class UpdatePool(AutoMarshallingModel):
    """" Update Pool Request Model
    @summary: An object that represents the the request data of updating a
        Pool.  This is used in updating an existing Pool.

    json ex:
        {
            "pool": {
                "name": "an_updated-pool",
                "description": "A new description",
                "session_persistence": {
                    "type": "COOKIE",
                    "cookie_name": "session_persistence_cookie"
                },
                "lb_algorithm": "LEAST_CONNECTIONS",
                "healthmonitor_id": "health_monitor_321",
                "admin_state_up": false
            }
        }

    xml ex:
        <pool xmlns=""
            name="an_updated-pool"
            description="A new description"
            lb_algorithm="LEAST_CONNECTIONS"
            healthmonitor_id="health_monitor_321"
            admin_state_up="False" >
            <sessionPersistence
                type="COOKIE"
                cookie_name="session_persistence_cookie" />
            </pool>
    """

    ROOT_TAG = 'pool'

    def __init__(self, name=None, description=None,
                 session_persistence=None, lb_algorithm=None,
                 healthmonitor_id=None, admin_state_up=None):
        super(UpdatePool, self).__init__()
        self.name = name
        self.description = description
        self.session_persistence = session_persistence
        self.lb_algorithm = lb_algorithm
        self.healthmonitor_id = healthmonitor_id
        self.admin_state_up = admin_state_up

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'description': self.description,
            'session_persistence': self.session_persistence,
            'lb_algorithm': self.lb_algorithm,
            'healthmonitor_id': self.healthmonitor_id,
            'admin_state_up': self.admin_state_up
        }
        body = self._remove_empty_values(body)
        return json.dumps({self.ROOT_TAG: body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        if self.name is not None:
            element.set('name', self.name)
        if self.description is not None:
            element.set('description', self.description)
        if self.lb_algorithm is not None:
            element.set('lb_algorithm', self.lb_algorithm)
        if self.healthmonitor_id is not None:
            element.set('healthmonitor_id', self.healthmonitor_id)
        if self.admin_state_up is not None:
            element.set('admin_state_up', str(self.admin_state_up))
        if self.session_persistence is not None:
            element.append(ET.fromstring(
                SetSessionPersistence(
                    type_=self.session_persistence.get('type'),
                    cookie_name=self.session_persistence.get('cookie_name')
                )._obj_to_xml()))
        xml = "{0}{1}".format(xml, ET.tostring(element))
        return xml
