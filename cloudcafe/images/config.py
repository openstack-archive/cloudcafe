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

    SECTION_NAME = 'images_admin_user'


class SecondaryUserConfig(BaseUserConfig):

    SECTION_NAME = 'images_secondary_user'


class ImagesConfig(ConfigSectionInterface):

    SECTION_NAME = 'images'

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
    def image_status_interval(self):
        return int(self.get('image_status_interval'))

    @property
    def snapshot_timeout(self):
        return int(self.get('snapshot_timeout'))

    @property
    def get_schema_count(self):
        return int(self.get('get_schema_count'))

    @property
    def post_members_count(self):
        return int(self.get('post_members_count'))

    @property
    def post_tasks_count(self):
        return int(self.get('post_tasks_count'))

    @property
    def remote_image(self):
        return self.get('remote_image')

    @property
    def http_image(self):
        return self.get('http_image')

    @property
    def test_image(self):
        return self.get('test_image')

    @property
    def test_disk_format(self):
        return self.get('test_disk_format')

    @property
    def test_container_format(self):
        return self.get('test_container_format')

    @property
    def image_schema_json(self):
        return self.get('image_schema_json')

    @property
    def images_schema_json(self):
        return self.get('images_schema_json')
