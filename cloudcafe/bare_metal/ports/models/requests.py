"""
Copyright 2014 Rackspace

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


class CreatePort(AutoMarshallingModel):

    def __init__(
            self, node_uuid=None, address=None, extra=None):
        super(CreatePort, self).__init__()
        extra = extra or {}

        self.node_uuid = node_uuid
        self.address = address
        self.extra = extra

    def _obj_to_json(self):
        create_request = {
            'node_uuid': self.node_uuid,
            'address': self.address,
            'extra': self.extra
        }
        self._remove_empty_values(create_request)
        return json.dumps(create_request)
