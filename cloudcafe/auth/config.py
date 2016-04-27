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


class UserAuthConfig(ConfigSectionInterface):

    SECTION_NAME = 'user_auth_config'

    @property
    def auth_endpoint(self):
        """The authentication endpoint to use for the credentials in the
        [user] config section.  This value is used by the auth provider.
        """

        return self.get("endpoint")

    @property
    def strategy(self):
        """The type of authentication exposed by the auth_endpoint. Currently,
        supported values are 'keystone', 'rax_auth', 'rax_auth_mfa', or
        'saio_tempauth'.
        """
        return self.get("strategy")


class UserConfig(ConfigSectionInterface):

    SECTION_NAME = 'user'

    @property
    def username(self):
        """The name of the user, if applicable"""
        return self.get("username")

    @property
    def api_key(self):
        """The user's api key, if applicable"""
        return self.get_raw("api_key")

    @property
    def password(self):
        """The user's password, if applicable"""
        return self.get_raw("password")

    @property
    def tenant_id(self):
        """The user's tenant_id, if applicable"""
        return self.get("tenant_id")

    @property
    def tenant_name(self):
        """The user's tenant_name, if applicable"""
        return self.get("tenant_name")

    @property
    def user_id(self):
        """The users's user_id, if applicable"""
        return self.get("user_id")

    @property
    def project_id(self):
        """The users's project_id, if applicable"""
        return self.get("project_id")

    @property
    def passcode(self):
        """The auth MFA's secondary password/passcode"""
        return self.get("passcode", 'MFA_PASSCODE_NOT_SET')
