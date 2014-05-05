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
from cloudcafe.identity.v2_0.config import IdentityConfig, IdentityUserConfig


class CloudKeepAuthConfig(IdentityConfig, IdentityUserConfig):
    """ Temporary Hack until we can refactor identity in CloudCAFE """
    SECTION_NAME = 'tokens_api'

    @property
    def auth_type(self):
        return str(self.get("auth_type")).lower()

    @property
    def version(self):
        """ version is missing from the new identity configs """
        return self.get("version")


class MarshallingConfig(ConfigSectionInterface):
    SECTION_NAME = 'marshalling'

    @property
    def serializer(self):
        return self.get("serialize_format")

    @property
    def deserializer(self):
        return self.get("deserialize_format")


class CloudKeepConfig(ConfigSectionInterface):
    SECTION_NAME = 'cloudkeep'

    @property
    def base_url(self):
        return self.get("base_url")

    @property
    def api_version(self):
        return self.get("api_version")

    @property
    def tenant_id(self):
        return self.get("tenant_id")


class CloudKeepSecretsConfig(ConfigSectionInterface):
    SECTION_NAME = 'cloudkeep-secrets'

    @property
    def name(self):
        return self.get("name")

    @property
    def algorithm(self):
        return self.get("algorithm")

    @property
    def bit_length(self):
        return int(self.get("bit_length"))

    @property
    def mode(self):
        return self.get("mode")

    @property
    def payload(self):
        return self.get("payload")

    @property
    def payload_content_type(self):
        return self.get("payload_content_type")

    @property
    def payload_content_encoding(self):
        return self.get("payload_content_encoding")


class CloudKeepOrdersConfig(ConfigSectionInterface):
    SECTION_NAME = 'cloudkeep-orders'

    @property
    def name(self):
        return self.get("name")

    @property
    def algorithm(self):
        return self.get("algorithm")

    @property
    def bit_length(self):
        return int(self.get("bit_length"))

    @property
    def mode(self):
        return self.get("mode")

    @property
    def payload_content_type(self):
        return self.get("payload_content_type")

    @property
    def payload_content_encoding(self):
        return self.get("payload_content_encoding")


class CloudKeepRBACRoleConfig(ConfigSectionInterface):
    SECTION_NAME = 'cloudkeep-rbac-role-users'

    @property
    def admin(self):
        return self.get('admin')

    @property
    def admin_password(self):
        return self.get('admin_password')

    @property
    def creator(self):
        return self.get('creator')

    @property
    def creator_password(self):
        return self.get('creator_password')

    @property
    def observer(self):
        return self.get('observer')

    @property
    def observer_password(self):
        return self.get('observer_password')

    @property
    def audit(self):
        return self.get('audit')

    @property
    def audit_password(self):
        return self.get('audit_password')


class CloudKeepVerificationsConfig(ConfigSectionInterface):
    SECTION_NAME = 'cloudkeep-verifications'

    @property
    def resource_type(self):
        return self.get("resource_type")

    @property
    def resource_ref(self):
        return self.get("resource_ref")

    @property
    def resource_action(self):
        return self.get("resource_action")

    @property
    def impersonation_allowed(self):
        return self.get("impersonation_allowed")
