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


class ServerResponse(AutoMarshallingModel):

    def __init__(self, id=None, name=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def _from_dict(self, server_dict):
        """
        {
          "id": "384a9b20-239c-11e2-81c1-0800200c9a66",
          "name": "ns1.example.org."
          "created_at": "2011-01-21T11:33:21Z",
          "updated_at": null
        }
        """
        return ServerResponse(server_dict.get("id"),
                              server_dict.get("name"),
                              server_dict.get("updated_at"),
                              server_dict.get("created_at"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return cls._from_dict(response_json)

class ServerListResponse(AutoMarshallingListModel):

    def __init__(Self, servers=None):
        self.servers = servers

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return cls._list_to_obj(response_json.get("servers"))

    @classmethod
    def _list_to_obj(cls, server_list):
        return [ServerResponse._from_dict(server) for server in server_list]
