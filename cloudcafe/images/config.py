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

    @property
    def username(self):
        return self.get("username")

    @property
    def api_key(self):
        return self.get_raw("api_key")

    @property
    def password(self):
        return self.get_raw("password")

    @property
    def tenant_id(self):
        return self.get("tenant_id")

    @property
    def tenant_name(self):
        return self.get("tenant_name")


class AltUserConfig(BaseUserConfig):

    SECTION_NAME = 'alt_user'

    @property
    def username(self):
        return self.get("username")

    @property
    def api_key(self):
        return self.get_raw("api_key")

    @property
    def password(self):
        return self.get_raw("password")

    @property
    def tenant_id(self):
        return self.get("tenant_id")

    @property
    def tenant_name(self):
        return self.get("tenant_name")


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
