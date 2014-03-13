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

from cafe.engine.models.behavior_response import BehaviorResponse


class DesignateResponse(BehaviorResponse):

    def __init__(self, response=None, entity=None):
        super(DesignateResponse, self).__init__()
        self.response = response
        self.entity = entity

    @property
    def status_code(self):
        if self.response is not None:
            return self.response.status_code

    @property
    def id(self):
        if self.entity is not None:
            return self.entity.id
