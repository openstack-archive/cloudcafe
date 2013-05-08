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
from json import dumps as dict_to_str
from cafe.engine.models.base import AutoMarshallingModel


class UpdateStatus(AutoMarshallingModel):

    def __init__(self, status):
        super(UpdateStatus, self).__init__()
        self.worker_status = status

    def _obj_to_json(self):
        return dict_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        return {
            'worker_status': self.worker_status
        }
