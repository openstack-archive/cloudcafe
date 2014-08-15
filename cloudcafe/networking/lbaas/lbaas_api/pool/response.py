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

Pool Response Model
Pools Response Model
"""

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel
from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.session_persistence.response \
    import SessionPersistence


class Pools(AutoMarshallingListModel):
    """Pools Response Model
    @summary: Response Model for a List of Pool Objects
    @note:  Returns a list of elements of type "Pool"

    json ex:
        {
            "pools": [
                {
                    "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                    "name": "Example HTTPS Pool",
                    "description": "Example HTTPS Pool Description"
                    "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                    "protocol": "HTTPS",
                    "session_persistence": {
                        "type": "COOKIE",
                        "cookie_name": "session_persistence_cookie"
                    },
                    "lb_algorithm": "ROUND_ROBIN",
                    "healthmonitor_id": "health_monitor_123",
                    "admin_state_up": true
                    "status": "ACTIVE"
                }
            ]
        }

    xml ex:
        <pools xmlns="">
            <pool xmlns=""
                id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
                name="Example HTTPS Pool"
                description="Example HTTPS Pool Description"
                tenant_id="7725fe12-1c14-4f45-ba8e-44bf01763578"
                protocol="HTTPS"
                lb_algorithm="ROUND_ROBIN"
                healthmonitor_id="health_monitor_123"
                admin_state_up="True"
                status="ACTIVE" >
                <session_persistence
                    type="COOKIE"
                    cookie_name="session_persistence_cookie"
                />
            />
        </pools>
    """
    ROOT_TAG = 'pools'

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, pools_dict_list):
        pools = Pools()
        pools.extend([Pool._dict_to_obj(pool) for
                      pool in pools_dict_list])
        return pools

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Pool.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        pools = Pools()
        pools.extend(
            [Pool._xml_ele_to_obj(pools_ele)
             for pools_ele in xml_list])
        return pools


class Pool(AutoMarshallingModel):
    """Pool Response Model
    @summary: Response Model for a Pool
    @note: Represents a single Pool object

    json ex:
        {
            "pool": {
                "id": "8992a43f-83af-4b49-9afd-c2bfbd82d7d7",
                "name": "Example HTTPS Pool",
                "description": "Example HTTPS Pool Description"
                "tenant_id": "7725fe12-1c14-4f45-ba8e-44bf01763578",
                "protocol": "HTTPS",
                "session_persistence": {
                    "type": "COOKIE",
                    "cookie_name": "session_persistence_cookie"
                },
                "lb_algorithm": "ROUND_ROBIN",
                "healthmonitor_id": "health_monitor_123",
                "admin_state_up": true,
                "status": "ACTIVE"
            }
        }

    xml ex:
        <pool xmlns=""
            id="8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
            name="Example HTTPS Pool"
            description="Example HTTPS Pool Description"
            tenant_id="7725fe12-1c14-4f45-ba8e-44bf01763578"
            protocol="HTTPS"
            lb_algorithm="ROUND_ROBIN"
            healthmonitor_id="health_monitor_123"
            admin_state_up="True"
            status="ACTIVE" >
            <session_persistence
                type="COOKIE"
                cookie_name="session_persistence_cookie"
            />
        />
    """

    ROOT_TAG = 'pool'

    def __init__(self, id_=None, name=None, description=None,
                 tenant_id=None, protocol=None, lb_algorithm=None,
                 healthmonitor_id=None, admin_state_up=None, status=None,
                 session_persistence=None):
        super(Pool, self).__init__()
        self.id_ = id_
        self.name = name
        self.description = description
        self.tenant_id = tenant_id
        self.protocol = protocol
        self.lb_algorithm = lb_algorithm
        self.healthmonitor_id = healthmonitor_id
        self.admin_state_up = admin_state_up
        self.status = status
        self.session_persistence = session_persistence

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._dict_to_obj(json_dict[cls.ROOT_TAG])

    @classmethod
    def _dict_to_obj(cls, pool_dict):

        # Process single entity models
        session_persistence = None
        if SessionPersistence.ROOT_TAG in pool_dict:
            session_persistence = SessionPersistence._dict_to_obj(
                pool_dict[SessionPersistence.ROOT_TAG])

        pool = Pool(
            id_=pool_dict.get('id'),
            name=pool_dict.get('name'),
            description=pool_dict.get('description'),
            tenant_id=pool_dict.get('tenant_id'),
            protocol=pool_dict.get('protocol'),
            lb_algorithm=pool_dict.get('lb_algorithm'),
            healthmonitor_id=pool_dict.get('healthmonitor_id'),
            admin_state_up=pool_dict.get('admin_state_up'),
            status=pool_dict.get('status'),
            session_persistence=session_persistence)
        return pool

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        element = ET.fromstring(serialized_string)
        if element.tag != cls.ROOT_TAG:
            return None
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        pool = cls._xml_ele_to_obj(element)
        return pool

    @classmethod
    def _xml_ele_to_obj(cls, element):
        pool_dict = element.attrib
        # XML data types differ from JSON, so we normalize here
        # Cast boolean
        if 'admin_state_up' in pool_dict:
            pool_dict['admin_state_up'] = cls._string_to_bool(
                pool_dict.get('admin_state_up'))

        # Process single entity models
        session_persistence = None
        if element.find(SessionPersistence.ROOT_TAG) is not None:
            session_persistence = SessionPersistence._xml_ele_to_obj(
                element.find(SessionPersistence.ROOT_TAG))

        pool = Pool(
            id_=pool_dict.get('id'),
            name=pool_dict.get('name'),
            description=pool_dict.get('description'),
            tenant_id=pool_dict.get('tenant_id'),
            protocol=pool_dict.get('protocol'),
            lb_algorithm=pool_dict.get('lb_algorithm'),
            healthmonitor_id=pool_dict.get('healthmonitor_id'),
            admin_state_up=pool_dict.get('admin_state_up'),
            status=pool_dict.get('status'),
            session_persistence=session_persistence)
        return pool
