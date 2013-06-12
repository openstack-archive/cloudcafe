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


class Version(AutoMarshallingModel):
    def __init__(self, version, build):
        super(Version, self).__init__()
        self.v1 = version
        self.build = build

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Returns an instance of a Version based on the json serialized_str
        passed in."""
        result = None
        json_obj = json.loads(serialized_str)
        if json_obj is not None:
            result = cls._dict_to_obj(json_obj)
        return result

    @classmethod
    def _dict_to_obj(cls, json_dict):
        kwargs = {
            'version': json_dict.get('v1'),
            'build': json_dict.get('build')
        }
        return Version(**kwargs)
