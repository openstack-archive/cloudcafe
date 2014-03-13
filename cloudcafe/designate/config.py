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


class DesignateConfig(ConfigSectionInterface):
    SECTION_NAME = 'designate'

    @property
    def url_v1(self):
        """An override for the version one API url"""
        return self.get("url_v1")

    @property
    def url_v2(self):
        """An override for the version two API url"""
        return self.get("url_v2")

    @property
    def default_ttl(self):
        """Defines a default value for the TTL"""
        return int(self.get("default_ttl", default="5600"))
