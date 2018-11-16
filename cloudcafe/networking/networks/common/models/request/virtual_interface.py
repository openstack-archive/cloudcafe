"""
Copyright 2018 Rackspace

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


class VirtualInterface(AutoMarshallingModel):
    ROOT_TAG = 'virtual_interface'

    def __init__(self, network_id=None):
        """
        An object that represents the data of a Virtual Interface
        """
        super(VirtualInterface, self).__init__()
        self.network_id = network_id

    def _obj_to_json(self):
        ret = {'network_id': self.network_id}
        ret = {self.ROOT_TAG: ret}
        return json.dumps(ret)