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


class TokenAPI_Config(ConfigSectionInterface):

    SECTION_NAME = 'user'

    @property
    def serialize_format(self):
        return self.get("serialize_format")

    @property
    def deserialize_format(self):
        return self.get("deserialize_format")

    @property
    def username(self):
        return self.get("username")

    @property
    def api_key(self):
        return self.get_raw("api_key")

    @property
    def tenant_id(self):
        return self.get("tenant_id")
