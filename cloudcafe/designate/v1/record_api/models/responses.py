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


class RecordResponse(AutoMarshallingModel):

    def __init__(self, id=None, name=None, type=None, created_at=None,
                 updated_at=None, domain_id=None, tenant_id=None, ttl=None,
                 priority=None, data=None, description=None, version=None):
        self.id = id
        self.name = name
        self.type = type
        self.ttl = ttl
        self.created_at = created_at
        self.updated_at = updated_at
        self.data = data
        self.domain_id = domain_id
        self.tenant_id = tenant_id
        self.priority = priority
        self.description = description
        self.version = version

    @classmethod
    def _from_dict(cls, record_dict):
        """
        {
          "id": "2e32e609-3a4f-45ba-bdef-e50eacd345ad",
          "name": "www.example.com.",
          "type": "A",
          "created_at": "2012-11-02T19:56:26.366792",
          "updated_at": null,
          "domain_id": "89acac79-38e7-497d-807c-a011e1310438",
          "ttl": null,
          "priority": null,
          "data": "192.0.2.3",
          "description": null
        }
        """
        return RecordResponse(id = record_dict.get("id"),
                              name = record_dict.get("name"),
                              type = record_dict.get("type"),
                              ttl = record_dict.get("ttl"),
                              created_at = record_dict.get("created_at"),
                              updated_at = record_dict.get("updated_at"),
                              data = record_dict.get("data"),
                              domain_id = record_dict.get("domain_id"),
                              tenant_id = record_dict.get("tenant_id"),
                              priority = record_dict.get("priority"),
                              description = record_dict.get("description"),
                              version = record_dict.get("version"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return cls._from_dict(response_json)


class RecordListResponse(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return cls._list_to_obj(response_json.get("records"))

    @classmethod
    def _list_to_obj(cls, record_list):
        return RecordListResponse(
            [RecordResponse._from_dict(record) for record in record_list])
