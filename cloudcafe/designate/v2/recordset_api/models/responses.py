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


class RecordsetResponse(AutoMarshallingModel):

    def __init__(self, description=None, links=None, created_at=None,
                 updated_at=None, priority=None, records=None, zone_id=None,
                 version=None, ttl=None, type=None, id=None, name=None):
         self.description = description
         self.links = links
         self.created_at = created_at
         self.updated_at = updated_at
         self.priority = priority
         self.records = records
         self.zone_id = zone_id
         self.version = version
         self.ttl = ttl
         self.type=type
         self.id = id
         self.name = name

    @classmethod
    def _from_dict(cls, recordset_dict):
        """
        {
            "created_at" : "2014-05-01T19:34:21.819615",
            "version" : 1,
            "zone_id" : "766d7605-4c48-41fa-a9de-76692ed8051c",
            "links" : {
                "self" : "http://192.168.33.8:9001/v2/zones/
                          766d7605-4c48-41fa-a9de-76692ed8051c/recordsets/
                           06c3a2de-4e23-4143-98ab-6bf6d41ded12"
            },
            "ttl" : 3600,
            "updated_at" : null,
            "description" : null,
            "type" : "A",
            "id" : "06c3a2de-4e23-4143-98ab-6bf6d41ded12",
            "name" : "foo.example.com.",
            "records" : [ "10.1.0.1" ]
        }
        """
        return RecordsetResponse(
            description = recordset_dict.get("description"),
            links = recordset_dict.get("links"),
            created_at = recordset_dict.get("created_at"),
            updated_at = recordset_dict.get("updated_at"),
            priority = recordset_dict.get("priority"),
            records = recordset_dict.get("records"),
            zone_id = recordset_dict.get("zone_id"),
            version = recordset_dict.get("version"),
            ttl = recordset_dict.get("ttl"),
            type = recordset_dict.get("type"),
            id = recordset_dict.get("id"),
            name = recordset_dict.get("name"))


    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return cls._from_dict(response_json.get("recordset"))


class RecordsetList(AutoMarshallingListModel):

    @classmethod
    def _list_to_obj(cls, recordset_list):
        return RecordsetList(
            [RecordsetResponse._from_dict(x) for x in recordset_list])


class RecordsetListResponse(AutoMarshallingModel):

    def __init__(self, recordsets, links):
        self.recordsets = recordsets
        self.links = links

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return RecordsetListResponse(
            RecordsetList._list_to_obj(response_json.get("recordsets")),
            Links._from_dict(response_json.get("links")))


