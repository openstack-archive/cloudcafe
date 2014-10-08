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


class RecordsetRequest(AutoMarshallingModel):

    def __init__(self, name=None, type=None, data=None, ttl=None):
        self.name = name
        self.type = type
        self.data = data
        self.ttl = ttl

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        """
        { "recordset" : {
             "name" : "foo.example.com.",
             "type" : "A",
             "ttl" : 3600
             "records" : [ "10.1.0.1" ] }}
        """
        return { "recordset": { "name": self.name,
                                "type": self.type,
                                "ttl": self.ttl,
                                "records": [self.data] }}
