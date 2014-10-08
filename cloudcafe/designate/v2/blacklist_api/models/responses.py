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


class BlacklistResponse(AutoMarshallingModel):

    def __init__(self, description=None, links=None, pattern=None,
                 created_at=None, updated_at=None, id=None):
        self.description = description
        self.links = links
        self.pattern = pattern
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = id

    @classmethod
    def _from_dict(cls, blacklist_dict):
        return BlacklistResponse(blacklist_dict.get("description"),
                                 blacklist_dict.get("links"),
                                 blacklist_dict.get("pattern"),
                                 blacklist_dict.get("created_at"),
                                 blacklist_dict.get("updated_at"),
                                 blacklist_dict.get("id"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        {
          "blacklist":{
            "description":"This is a blacklisted domain.",
            "links":{
              "self":"http://127.0.0.1:9001/v2/
                      blacklists/c47229fb-0831-4b55-a5b5-380d361be4bd"
            },
            "pattern":"^([A-Za-z0-9_\\-]+\\.)*example\\.com\\.$",
            "created_at":"2014-03-11T21:54:57.000000",
            "updated_at":null,
            "id":"c47229fb-0831-4b55-a5b5-380d361be4bd"
          }
        }
        """
        response_json = json.loads(serialized_str)
        return BlacklistResponse._from_dict(response_json.get("blacklist"))


class BlacklistList(AutoMarshallingListModel):

    @classmethod
    def _list_to_obj(cls, blacklist_list):
        return BlacklistList(
            [BlacklistResponse._from_dict(x) for x in blacklist_list])


class BlacklistListResponse(AutoMarshallingListModel):

    def __init__(self, blacklists=None, links=None):
        self.blacklists = blacklists
        self.links = links

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return BlacklistListResponse(
            BlacklistResponse._list_to_obj(response_json.get("blacklists")),
            Links._from_dict(response_json.get("links")))

