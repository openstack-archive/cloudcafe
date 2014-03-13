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


class DomainResponse(AutoMarshallingModel):

    def __init__(self, description=None, created_at=None, updated_at=None,
                 email=None, ttl=None, serial=None, id=None, name=None):
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.email = email
        self.ttl = ttl
        self.serial = serial
        self.id = id
        self.name = name

    @classmethod
    def _from_dict(cls, domain_dict):
        """
        {
          "id": "89acac79-38e7-497d-807c-a011e1310438",
          "name": "domain1.com.",
          "ttl": 3600,
          "serial": 1351800588,
          "email": "nsadmin@example.org",
          "created_at": "2012-11-01T20:09:48.094457",
          "updated_at": null,
          "description": null
        }
        """
        return DomainResponse(domain_dict.get("description"),
                              domain_dict.get("created_at"),
                              domain_dict.get("updated_at"),
                              domain_dict.get("email"),
                              domain_dict.get("ttl"),
                              domain_dict.get("serial"),
                              domain_dict.get("id"),
                              domain_dict.get("name"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return cls._from_dict(response_json)

class DomainListResponse(AutoMarshallingListModel):

    def __init__(self, domains=None):
        self.domains = domains

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return cls._list_to_obj(response_json.get("domains"))

    @classmethod
    def _list_to_obj(cls, domain_list):
        return [DomainResponse._from_dict(domain) for domain in domain_list]
