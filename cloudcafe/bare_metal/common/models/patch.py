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

from cafe.engine.models.base import AutoMarshallingModel, \
    AutoMarshallingListModel


class Patch(AutoMarshallingModel):

    def __init__(self, path=None, value=None, op=None):
        super(Patch, self).__init__()
        self.path = path
        self.value = value
        self.op = op

    def _obj_to_dict(self):
        return {'path': self.path, 'value': self.value, 'op': self.op}


class Patches(AutoMarshallingListModel):

    def _obj_to_json(self):
        patches = Patches()
        for patch in self:
            patches.append(patch)
        return json.dumps(patches)
