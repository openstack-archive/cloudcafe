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
    def cypher_type(self):
        return self.get("cypher_type")

    @property
    def plain_text(self):
        return self.get("plain_text")

    @property
    def mime_type(self):
        return self.get("mime_type")
