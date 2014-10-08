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


class ZoneRequest(AutoMarshallingModel):

    def __init__(self, name=None, email=None, ttl=None,description=None):
        self.name = name
        self.email = email
        self.ttl = ttl
        self.description = description

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        """
        { "zone": {
            "name": "example.org.",
            "email": "joe@example.org",
            "ttl": 7200,
            "description": "This is an example zone."}}
        """
        return {"zone": {"name": self.name,
                         "email": self.email,
                         "ttl": self.ttl,
                         "description" : self.description}}


class ImportZoneRequest(AutoMarshallingModel):

    def __init__(self, import_text=None):
        self.import_text = import_text

    def _obj_to_json(self):
        return self.import_text
