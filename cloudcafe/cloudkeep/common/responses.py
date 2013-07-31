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
        self.ref = None
        self.id = None
        self.status_code = None
        self.get_resp = None
        if resp is not None:
            self.ref = resp.entity.reference
            self.status_code = resp.status_code
            self.id = self._get_id_from_ref(ref=self.ref)
        if get_resp is not None:
            self.get_resp = get_resp
            self.get_status_code = get_resp.status_code

    def _get_id_from_ref(self, ref):
        """Returns id from reference."""
        ref_id = None
        if ref is not None and len(ref) > 0:
            ref_id = path.split(ref)[1]
        return ref_id
