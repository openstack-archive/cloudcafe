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
from cloudcafe.blockstorage.volumes_api.common.config import \
    VolumesAPIConfig as _VolumesAPIConfig


class VolumesAPIConfig(_VolumesAPIConfig):
    SECTION_NAME = 'volumes_api_v2'

    @property
    def min_volume_from_image_size(self):
        """Limit the smallest size a volume can be if building from an image"""
        return int(self.get("min_volume_from_image_size", default=1))

    @property
    def image_filter(self):
        """Expects Json.  Returns an empty dictionary by default.
        Dictionary keys should be attributes of the image model, and key values
        should be a list of values for that model attribute.
        """
        return json.loads(self.get('image_filter', '{}'))

    @property
    def volume_type_filter(self):
        """Expects Json.  Returns an empty dictionary by default.
        Dictionary keys should be attributes of the volume type model, and
        key values should be a list of values for that model attribute.
        """
        return json.loads(self.get('volume_type_filter', '{}'))
