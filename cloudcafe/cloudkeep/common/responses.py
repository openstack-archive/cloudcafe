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

from os import path

from cafe.engine.models.behavior_response import BehaviorResponse


class CloudkeepResponse(BehaviorResponse):

    def __init__(self, resp=None, get_resp=None, entity=None):
        super(CloudkeepResponse, self).__init__()
        self.create_resp = resp
        self.entity = entity
        self.get_resp = get_resp

    @property
    def status_code(self):
        if self.create_resp is not None:
            return self.create_resp.status_code

    @property
    def ref(self):
        if self.create_resp is not None and self.create_resp.entity:
            return self.create_resp.entity.reference

    @property
    def id(self):
        return self.get_id_from_ref(self.ref)

    @property
    def get_status_code(self):
        if self.get_resp is not None:
            return self.get_resp.status_code

    @classmethod
    def get_id_from_ref(cls, ref):
        """Returns id from reference."""
        ref_id = None
        if ref is not None and len(ref) > 0:
            ref_id = path.split(ref)[1]
        return ref_id
