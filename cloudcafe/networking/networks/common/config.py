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
    def resource_change_status_timeout(self):
        """Seconds to wait for a status change in the resource"""
        return int(self.get("resource_change_status_timeout", 15))

    @property
    def api_poll_rate(self):
        """Time interval for api calls on while loops retries"""
        return int(self.get("api_poll_rate", 4))

    @property
    def check_response_attrs(self):
        """Flag to enable checking the response attributes"""
        return self.get("check_response_attrs", True)
