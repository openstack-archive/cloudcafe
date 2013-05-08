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
from xml.etree import ElementTree

from cafe.engine.models.base import AutoMarshallingModel


class CreateSecurityGroup(AutoMarshallingModel):

    def __init__(self, name=None, description=None):

        super(CreateSecurityGroup, self).__init__()
        self.name = name
        self.description = description

    def _obj_to_json(self):
        ret = {'security_group': self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        ret['name'] = self.name
        ret['description'] = self.description
        return ret

    def _obj_to_xml(self):
        raise NotImplemented

    def _obj_to_xml_ele(self):
        raise NotImplemented
