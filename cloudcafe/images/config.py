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

from cloudcafe.auth.config import UserConfig as BaseUserConfig
from cloudcafe.common.models.configuration import ConfigSectionInterface


class MarshallingConfig(ConfigSectionInterface):
    SECTION_NAME = 'marshalling'

    @property
    def serializer(self):
        """Default serialization format"""
        return self.get("serialize_format")

    @property
    def deserializer(self):
        """Default Deserialization format"""
        return self.get("deserialize_format")


class AltUserConfig(BaseUserConfig):
    SECTION_NAME = 'alt_user'


class ThirdUserConfig(BaseUserConfig):
    SECTION_NAME = 'third_user'


class ImagesConfig(ConfigSectionInterface):
    SECTION_NAME = 'images'

    @property
    def override_url(self):
        """Url used to override service catalog endpoint"""
        return self.get('override_url')

    @property
    def allow_post_images(self):
        """Toggle to determine if override_url allows POST calls to /images"""
        return self.get_boolean('allow_post_images')

    @property
    def allow_put_image_file(self):
        """
        Toggle to determine if override_url allows PUT calls to
        /images/<image_id>/file
        """
        return self.get_boolean('allow_put_image_file')

    @property
    def allow_get_image_file(self):
        """
        Toggle to determine if override_url allows GET calls to
        /images/<image_id>/file
        """
        return self.get_boolean('allow_get_image_file')

    @property
    def allow_create_update_public_images(self):
        """
        Toggle to determine if override_url allows creating and updating
        public images
        """
        return self.get_boolean('allow_create_update_public_images')

    @property
    def endpoint_name(self):
        """Name to identify endpoint in service catalog"""
        return self.get('endpoint_name')

    @property
    def region(self):
        """Region to identity endpoint in service catalog"""
        return self.get('region')

    @property
    def superuser(self):
        """Toggle to determine if primary user has superuser privileges"""
        return self.get_boolean('superuser')

    @property
    def primary_image(self):
        """Primary image to be used during tests"""
        return self.get("primary_image")

    @property
    def windows_image(self):
        """Windows image to be used during tests"""
        return self.get("windows_image")

    @property
    def windows_flavor(self):
        """Windows flavor to be used during tests"""
        return self.get("windows_flavor")

    @property
    def image_status_interval(self):
        """Time to wait between polling the status of an image"""
        return int(self.get("image_status_interval"))

    @property
    def snapshot_timeout(self):
        """Time to wait before giving up on reaching a status"""
        return int(self.get("snapshot_timeout"))

    @property
    def primary_image_default_user(self):
        """The default user created when a server is booted"""
        return self.get("primary_image_default_user")

    @property
    def min_disk(self):
        """Default minimum disk space in image properties"""
        return int(self.get('min_disk'))

    @property
    def min_ram(self):
        """Default minimum ram in image properties"""
        return int(self.get('min_ram'))

    @property
    def size_min(self):
        """Default minimum size in image properties"""
        return int(self.get('size_min'))

    @property
    def size_max(self):
        """Default maximum size in image properties"""
        return int(self.get('size_max'))

    @property
    def additional_property(self):
        """Default additional property in image properties"""
        return self.get('additional_property')

    @property
    def additional_property_value(self):
        """Default additional property value in image properties"""
        return self.get('additional_property_value')

    @property
    def results_limit(self):
        """Default number of results to return is list requests"""
        return int(self.get('results_limit'))

    @property
    def test_image_name(self):
        """Name of image used for internal testing"""
        return self.get('test_image_name')

    @property
    def resource_creation_attempts(self):
        """Number of times to attempt to create a specified resource"""
        return int(self.get('resource_creation_attempts'))

    @property
    def max_created_at_delta(self):
        """Maximum number of seconds that created_at can differ"""
        return int(self.get('max_created_at_delta'))

    @property
    def max_updated_at_delta(self):
        """Maximum number of seconds that updated_at can differ"""
        return int(self.get('max_updated_at_delta'))

    @property
    def max_expires_at_delta(self):
        """Maximum number of seconds that expires_at can differ"""
        return int(self.get('max_expires_at_delta'))

    @property
    def test_file(self):
        """Test file for tasks and file data"""
        return self.get('test_file')

    @property
    def image_members_limit(self):
        """Maximum number of members allowed on a given image"""
        return int(self.get('image_members_limit'))

    @property
    def image_properties_limit(self):
        """Maximum number of properties allowed on a given image"""
        return int(self.get('image_properties_limit'))

    @property
    def image_tags_limit(self):
        """Maximum number of tags allowed on a given image"""
        return int(self.get('image_tags_limit'))

    @property
    def import_from(self):
        """Location from which to import a minimal VHD that is not bootable"""
        return self.get('import_from')

    @property
    def import_from_bootable(self):
        """Location from which to import a bootable VHD"""
        return self.get('import_from_bootable')

    @property
    def import_from_format(self):
        """Format for which to import the a given file"""
        return self.get('import_from_format')

    @property
    def export_to(self):
        """Location to export a given file"""
        return self.get('export_to')

    @property
    def alt_export_to(self):
        """Location to export a given file"""
        return self.get('alt_export_to')

    @property
    def task_status_interval(self):
        """Amount of time to wait between polling the status of a task"""
        return int(self.get("task_status_interval"))

    @property
    def task_timeout(self):
        """Length of time to wait before giving up on reaching a status"""
        return int(self.get("task_timeout"))

    @property
    def do_not_delete_files(self):
        """List of files that should not be deleted"""
        return ([x.strip() for x in
                 self.get('do_not_delete_files', "").split(',')])

    @property
    def versions_data(self):
        """Path to versions data"""
        return self.get('versions_data')

    @property
    def versions_list(self):
        """List of versions"""
        return [x.strip() for x in self.get('versions_list', "").split(',')]

    @property
    def account_list(self):
        """List of accounts"""
        return [x.strip() for x in self.get('account_list', "").split(',')]

    @property
    def image_schema_json(self):
        """Path to json file which contains the image schema data"""
        return self.get('image_schema_json')

    @property
    def images_schema_json(self):
        """Path to json file which contains the images schema data"""
        return self.get('images_schema_json')

    @property
    def image_member_schema_json(self):
        """Path to json file which contains the image member schema data"""
        return self.get('image_member_schema_json')

    @property
    def image_members_schema_json(self):
        """Path to json file which contains the image members schema data"""
        return self.get('image_members_schema_json')

    @property
    def task_schema_json(self):
        """Path to json file which contains the task schema data"""
        return self.get('task_schema_json')

    @property
    def tasks_schema_json(self):
        """Path to json file which contains the tasks schema data"""
        return self.get('tasks_schema_json')
