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


class RecordRequest(AutoMarshallingModel):

    def __init__(self, name=None, record_type=None, data=None, ttl=None,
                 priority=None):
        self.name = name
        self.type = record_type
        self.data = data
        self.ttl = ttl
        self.priority = priority

    def _obj_to_json(self):
        records = self._obj_to_dict()
        return json.dumps(records)

    def _obj_to_dict(self):
        """
        { "name": "www.example.com.",
          "type": "A",
          "data": "192.0.2.3" }
        """
        records = {
            "name": self.name,
            "type": self.type,
            "data": self.data,
            "ttl": self.ttl,
            "priority": self.priority,
        }
        return self._remove_empty_values(records)
