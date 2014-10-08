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

from cafe.engine.models.base import AutoMarshallingModel
from cafe.engine.models.base import AutoMarshallingListModel
from cloudcafe.designate.models import Links


class ZoneResponse(AutoMarshallingModel):

    def __init__(self, status=None, description=None, links=None,
                 updated_at=None, ttl=None, serial=None, id=None, name=None,
                 created_at=None, pool_id=None, version=None, project_id=None,
                 email=None):
        self.status = status
        self.description = description
        self.links = links
        self.updated_at = updated_at
        self.ttl = ttl
        self.serial = serial
        self.id = id
        self.name = name
        self.created_at = created_at
        self.pool_id = pool_id
        self.version = version
        self.project_id = project_id
        self.email = email

    @classmethod
    def _from_dict(cls, zone_dict):
        return ZoneResponse(zone_dict.get("status"),
                            zone_dict.get("description"),
                            zone_dict.get("links"),
                            zone_dict.get("updated_at"),
                            zone_dict.get("ttl"),
                            zone_dict.get("serial"),
                            zone_dict.get("id"),
                            zone_dict.get("name"),
                            zone_dict.get("created_at"),
                            zone_dict.get("pool_id"),
                            zone_dict.get("version"),
                            zone_dict.get("project_id"),
                            zone_dict.get("email"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return cls._from_dict(response_json.get("zone"))


class ZoneList(AutoMarshallingListModel):

    @classmethod
    def _list_to_obj(cls, zone_list):
        return ZoneList([ZoneResponse._from_dict(zone) for zone in zone_list])


class ZoneListResponse(AutoMarshallingModel):

    def __init__(self, zones, links=None):
        self.zones = zones
        self.links = links

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        zones = ZoneList._list_to_obj(response_json.get("zones"))
        links = Links._from_dict(response_json.get("links"))
        return ZoneListResponse(zones=zones, links=links)


class ExportZoneResponse(AutoMarshallingModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        return serialized_str
