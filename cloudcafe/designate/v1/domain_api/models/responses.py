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
    def _from_json_str(cls, json_str):
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
        return DomainResponse(json_str.get("description"),
                              json_str.get("created_at"),
                              json_str.get("updated_at"),
                              json_str.get("email"),
                              json_str.get("ttl"),
                              json_str.get("serial"),
                              json_str.get("id"),
                              json_str.get("name"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        if "domains" in response_json:
            return [cls._from_json_str(record)
                    for record in response_json["domains"]]
        else:
            return cls._from_json_str(response_json)
