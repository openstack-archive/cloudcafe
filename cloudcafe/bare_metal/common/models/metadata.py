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

from cafe.engine.models.base import AutoMarshallingDictModel


class MetadataBase(AutoMarshallingDictModel):

    METADATA_TYPE = ''

    def _obj_to_json(self):
        return json.dumps({self.METADATA_TYPE: self})

    @classmethod
    def _json_to_obj(cls, json_body):
        metadata = MetadataBase()
        meta_contents = json.loads(json_body)
        metadata.update(meta_contents.get(cls.METADATA_TYPE))
        return metadata

    @classmethod
    def _dict_to_obj(cls, json_dict):
        metadata = MetadataBase()
        metadata.update(json_dict)
        return metadata


class Extra(MetadataBase):
    METADATA_TYPE = 'extra'

