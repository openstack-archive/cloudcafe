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

from cloudcafe.auth.config import UserAuthConfig, UserConfig
from cloudcafe.common.models.configuration import ConfigSectionInterface


class NetworkingBaseConfig(ConfigSectionInterface):
    """Config parent class to be inherited by all api configs"""

    SECTION_NAME = 'networking'

    @property
    def keep_resources(self):
        """Flag for not deleting resources on tearDown"""
        return self.get_boolean("keep_resources", False)

    @property
    def keep_resources_on_failure(self):
        """Flag for not deleting resources w failures on tearDown"""
        return self.get_boolean("keep_resources_on_failure", False)

    @property
    def api_poll_interval(self):
        """Time interval for api calls on while loops retries"""
        return int(self.get("api_poll_interval", 2))

    @property
    def api_retries(self):
        """Number of times to retry an API call by a behavior method"""
        return int(self.get("api_retries", 1))

    @property
    def resource_create_timeout(self):
        """Seconds to wait for creating a resource"""
        return int(self.get("resource_create_timeout", 7))

    @property
    def resource_update_timeout(self):
        """Seconds to wait for updating a resource"""
        return int(self.get("resource_update_timeout", 7))

    @property
    def resource_delete_timeout(self):
        """Seconds to wait for deleting a resource"""
        return int(self.get("resource_delete_timeout", 7))

    @property
    def resource_get_timeout(self):
        """Seconds to wait for getting a resource"""
        return int(self.get("resource_get_timeout", 7))

    @property
    def resource_change_status_timeout(self):
        """Seconds to wait for a status change in the resource"""
        return int(self.get("resource_change_status_timeout", 10))

    @property
    def check_response_attrs(self):
        """Flag to enable checking the response attributes"""
        return self.get_boolean("check_response_attrs", True)
