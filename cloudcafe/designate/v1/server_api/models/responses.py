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


class ServerResponse(AutoMarshallingModel):

    def __init__(self, id=None, name=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def _from_json_str(self, json_str):
        return ServerResponse(json_str.get("id"),
                              json_str.get("name"),
                              json_str.get("updated_at"),
                              json_str.get("created_at"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        {
          "id": "384a9b20-239c-11e2-81c1-0800200c9a66",
          "name": "ns1.example.org."
          "created_at": "2011-01-21T11:33:21Z",
          "updated_at": null
        }
        """
        response_json = json.loads(serialized_str)
        if "servers" in response_json:
            return [cls._from_json_str(record)
                    for record in response_json["servers"]]
        else:
            return cls._from_json_str(response_json)
