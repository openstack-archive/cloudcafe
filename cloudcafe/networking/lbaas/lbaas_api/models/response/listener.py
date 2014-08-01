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

Listener Response Model
Listeners Response Model
"""

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel
from cloudcafe.networking.lbaas.common.constants import Constants


class Listeners(AutoMarshallingListModel):
    """Listeners Response Model
    @summary: Response Model for a List of Listener Objects
    @note:  Returns a list of elements of type "Listener"

    json ex:
        {
            "listeners": [
                {
                    "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                    "name": "Example HTTPS Listener",
                    "description": "A simple example of an HTTPS listener.",
                    "load_balancer_id": "b8a35470-f65d-11e3-a3ac-0800200c9a66",
                    "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                    "default_pool_id": "8311446e-8a13-4c00-95b3-03a92f9759c7",
                    "connection_limit": 200,
                    "protocol": "HTTPS",
                    "protocol_port": 443,
                    "tenant_id": "352686b7-c4b2-44ec-a458-84239713f685",
                    "admin_state_up": true
                    "status": "ACTIVE"
                }
            ]
        }

    xml ex:
        <listeners xmlns="">
            <listener xmlns=""
                id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
                name="Example HTTPS Listener"
                description="A simple example of an HTTPS listener."
                load_balancer_id="b8a35470-f65d-11e3-a3ac-0800200c9a66"
                tenant_id="7725fe12-1c14-4f45-ba8e-44bf01763578"
                default_pool_id="8311446e-8a13-4c00-95b3-03a92f9759c7"
                connection_limit="200"
                protocol="HTTPS"
                protocol_port="443"
                admin_state_up="true"
                status="ACTIVE"
            />
        </loadbalancers>
    """
    ROOT_TAG = 'listeners'

    def __init__(self, listeners=None):
        super(Listeners, self).__init__()
        if listeners is None:
            listeners = []
        for listener in listeners:
            self.append(listener)

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, listeners_dict_list):
        listeners = Listeners()
        listeners.extend([Listener._dict_to_obj(listener) for
                          listener in listeners_dict_list])
        return listeners

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Listener.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        listeners = Listeners()
        listeners.extend(
            [Listener._xml_ele_to_obj(listeners_ele)
             for listeners_ele in xml_list])
        return listeners


class Listener(AutoMarshallingModel):
    """Listener Response Model
    @summary: Response Model for a Listener
    @note: Represents a single Listener object

    json ex:
        {
            "listener": {
                "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                "name": "Example HTTPS Listener",
                "description": "A very simple example of an HTTPS listener.",
                "load_balancer_id": "b8a35470-f65d-11e3-a3ac-0800200c9a66",
                "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                "default_pool_id": "8311446e-8a13-4c00-95b3-03a92f9759c7",
                "connection_limit": 200,
                "protocol": "HTTPS",
                "protocol_port": "443",
                "status": "ACTIVE"
            }
        }

    xml ex:
        <listener xmlns=""
            id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
            name="Example HTTPS Listener"
            description="A very simple example of an HTTPS listener."
            load_balancer_id="b8a35470-f65d-11e3-a3ac-0800200c9a66"
            tenant_id="7725fe12-1c14-4f45-ba8e-44bf01763578"
            default_pool_id="8311446e-8a13-4c00-95b3-03a92f9759c7"
            connection_limit="200"
            protocol="HTTPS"
            protocol_port="443"
            admin_state_up="true"
            status="ACTIVE"
        />
    """

    ROOT_TAG = 'listener'

    def __init__(self, id_=None, name=None, load_balancer_id=None,
                 tenant_id=None, default_pool_id=None, protocol=None,
                 protocol_port=None, description=None, connection_limit=None,
                 admin_state_up=None, status=None):
        super(Listener, self).__init__()
        self.id_ = id_
        self.name = name
        self.load_balancer_id = load_balancer_id
        self.tenant_id = tenant_id
        self.default_pool_id = default_pool_id
        self.protocol = protocol
        self.protocol_port = protocol_port
        self.description = description
        self.connection_limit = connection_limit
        self.admin_state_up = admin_state_up
        self.status = status

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._dict_to_obj(json_dict[cls.ROOT_TAG])

    @classmethod
    def _dict_to_obj(cls, listener_dict):
        listener = Listener(
            id_=listener_dict.get('id'),
            name=listener_dict.get('name'),
            load_balancer_id=listener_dict.get('load_balancer_id'),
            tenant_id=listener_dict.get('tenant_id'),
            default_pool_id=listener_dict.get('default_pool_id'),
            protocol=listener_dict.get('protocol'),
            protocol_port=listener_dict.get('protocol_port'),
            description=listener_dict.get('description'),
            connection_limit=listener_dict.get('connection_limit'),
            admin_state_up=listener_dict.get('admin_state_up'),
            status=listener_dict.get('status'))
        return listener

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        listener = cls._xml_ele_to_obj(element)
        return listener

    @classmethod
    def _xml_ele_to_obj(cls, element):
        listener_dict = element.attrib
        # Cast Integers
        if 'connection_limit' in listener_dict:
            listener_dict['connection_limit'] = (
                listener_dict.get('connection_limit') and
                int(listener_dict.get('connection_limit')))
        if 'protocol_port' in listener_dict:
            listener_dict['protocol_port'] = (
                listener_dict.get('protocol_port') and
                int(listener_dict.get('protocol_port')))
        # Cast boolean
        if 'admin_state_up' in listener_dict:
            listener_dict['admin_state_up'] = cls._string_to_bool(
                listener_dict.get('admin_state_up'))
        listener = Listener(
            id_=listener_dict.get('id'),
            name=listener_dict.get('name'),
            load_balancer_id=listener_dict.get('load_balancer_id'),
            tenant_id=listener_dict.get('tenant_id'),
            default_pool_id=listener_dict.get('default_pool_id'),
            protocol=listener_dict.get('protocol'),
            protocol_port=listener_dict.get('protocol_port'),
            description=listener_dict.get('description'),
            connection_limit=listener_dict.get('connection_limit'),
            admin_state_up=listener_dict.get('admin_state_up'),
            status=listener_dict.get('status'))
        return listener

    def __repr__(self):
        items = ', '.join("{key}: {value}".format(key=key, value=value)
                          for key, value in self.__dict__.items())
        return "{root_tag}: [{items}]".format(root_tag=self.ROOT_TAG,
                                              items=items)
