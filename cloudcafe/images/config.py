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

from cloudcafe.common.models.configuration import ConfigSectionInterface


class ImagesConfig(ConfigSectionInterface):

    SECTION_NAME = 'images'

    @property
    def primary_image(self):
        """Primary image"""
        return self.get('primary_image')

    @property
    def secondary_image(self):
        """Secondary image"""
        return self.get('secondary_image')


class UserAuthConfig(ConfigSectionInterface):

    SECTION_NAME = 'user_auth_config'

    @property
    def endpoint(self):
        """Authentication endpoint for Images API"""
        return self.get('endpoint')

    @property
    def strategy(self):
        """Authentication strategy to use"""
        return self.get('strategy')


class ImagesUserConfig(ConfigSectionInterface):

    SECTION_NAME = 'images_user'

    @property
    def username(self):
        """Username authorized to access Images API"""
        return self.get('username')

    @property
    def password(self):
        """Password for user to access Images API"""
        return self.get('password')

    @property
    def tenant_name(self):
        """Name of tenant to use"""
        return self.get('tenant_name')

    @property
    def user_id(self):
        """User ID of user"""
        return self.get('user_id')
