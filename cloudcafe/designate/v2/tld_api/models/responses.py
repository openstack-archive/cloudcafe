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


class TLDResponse(AutoMarshallingModel):

    def __init__(self, description=None, links=None, created_at=None,
                 updated_at=None, id=None, name=None):
        self.description = description
        self.links = links
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = id
        self.name = name

    @classmethod
    def _from_dict(cls, tld_dict):
        return TLDResponse(tld_dict.get("description"),
                           tld_dict.get("links"),
                           tld_dict.get("created_at"),
                           tld_dict.get("updated_at"),
                           tld_dict.get("id"),
                           tld_dict.get("name"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        { "tld":{
            "description": "...",
            "links": {
              "self":"http://127.0.0.1:9001
              /v2/tlds/5abe514c-9fb5-41e8-ab73-5ed25f8a73e9"
            },
            "created_at": "2014-01-23T18:39:26.710827",
            "updated_at": null,
            "id": "5abe514c-9fb5-41e8-ab73-5ed25f8a73e9",
            "name": "com"
          }}
        """
        response_json = json.loads(serialized_str)
        return TLDResponse._from_dict(response_json.get("tld"))


class TLDList(AutoMarshallingListModel):

    @classmethod
    def _list_to_obj(cls, tld_list):
        return TLDList([TLDResponse._from_dict(tld) for tld in tld_list])


class TLDListResponse(AutoMarshallingModel):

    def __init__(self, tlds=None, links=None):
        self.tlds = tlds
        self.links = links

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        return TLDListResponse(
            tlds = TLDList._list_to_obj(response_json.get("tlds")),
            links = Links._from_dict(response_json.get("links")))
