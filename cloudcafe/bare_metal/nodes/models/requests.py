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


class CreateNode(AutoMarshallingModel):

    def __init__(
            self, chassis_uuid=None, driver=None, properties=None,
            driver_info=None, extra=None):
        super(CreateNode, self).__init__()

        properties = properties or {}
        driver_info = driver_info or {}
        extra = extra or {}

        self.chassis_uuid = chassis_uuid
        self.driver = driver
        self.properties = properties
        self.driver_info = driver_info
        self.extra = extra

    def _obj_to_json(self):
        create_request = {
            'chassis_uuid': self.chassis_uuid,
            'driver': self.driver,
            'properties': self.properties,
            'driver_info': self.driver_info,
            'extra': self.extra
        }
        self._remove_empty_values(create_request)
        return json.dumps(create_request)


class SetNodePowerState(AutoMarshallingModel):

    def __init__(self, power_state):
        super(SetNodePowerState, self).__init__()
        self.power_state = power_state

    def _obj_to_json(self):
        return json.dumps({'target': self.power_state})


class SetNodeConsoleMode(AutoMarshallingModel):

    def __init__(self, enabled):
        super(SetNodeConsoleMode, self).__init__()
        self.enabled = enabled

    def _obj_to_json(self):
        return json.dumps({'enabled': self.enabled})
