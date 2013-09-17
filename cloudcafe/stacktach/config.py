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


class MiscConfig(ConfigSectionInterface):
    SECTION_NAME = 'misc'

    @property
    def serializer(self):
        return self.get("serializer")

    @property
    def deserializer(self):
        return self.get("deserializer")


class StacktachConfig(ConfigSectionInterface):

    SECTION_NAME = 'stacktach'

    @property
    def event_id(self):
        return self.get('event_id')

    @property
    def url(self):
        return self.get('url')

    @property
    def db_url(self):
        return self.get('db_url')

    @property
    def days_passed(self):
        return self.get('days_passed')
