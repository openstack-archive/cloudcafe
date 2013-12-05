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

from cloudcafe.auth.config import UserConfig as BaseUserConfig
from cloudcafe.common.models.configuration import ConfigSectionInterface


class MarshallingConfig(ConfigSectionInterface):

    SECTION_NAME = 'marshalling'

    @property
    def serializer(self):
        return self.get("serialize_format")

    @property
    def deserializer(self):
        return self.get("deserialize_format")


class AdminUserConfig(BaseUserConfig):

    SECTION_NAME = 'admin_user'


class AltUserConfig(BaseUserConfig):

    SECTION_NAME = 'alt_user'


class ImagesConfig(ConfigSectionInterface):

    SECTION_NAME = 'images'

    @property
    def internal_url(self):
        return self.get('internal_url')

    @property
    def override_url(self):
        return self.get('override_url')

    @property
    def endpoint_name(self):
        return self.get('endpoint_name')

    @property
    def region(self):
        return self.get('region')

    @property
    def primary_image(self):
        """Default image to be used when building servers in glance test"""
        return self.get("primary_image")

    @property
    def secondary_image(self):
        """Alternate image to be used in glance test"""
        return self.get("secondary_image")

    @property
    def image_status_interval(self):
        """Amount of time to wait between polling the status of an image"""
        return int(self.get("image_status_interval"))

    @property
    def snapshot_timeout(self):
        """Length of time to wait before giving up on reaching a status"""
        return int(self.get("snapshot_timeout"))

    @property
    def min_disk(self):
        return int(self.get('min_disk'))

    @property
    def min_ram(self):
        return int(self.get('min_ram'))

    @property
    def size_min(self):
        return int(self.get('size_min'))

    @property
    def size_max(self):
        return int(self.get('size_max'))

    @property
    def results_limit(self):
        return int(self.get('results_limit'))

    @property
    def image_schema_json(self):
        return self.get('image_schema_json')

    @property
    def images_schema_json(self):
        return self.get('images_schema_json')

    @property
    def created_at_offset(self):
        return self.get('created_at_offset')

    @property
    def updated_at_offset(self):
        return self.get('updated_at_offset')
