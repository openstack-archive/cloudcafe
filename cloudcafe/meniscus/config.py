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
from json import loads as json_to_dict
from cloudcafe.common.models.configuration import ConfigSectionInterface


class MarshallingConfig(ConfigSectionInterface):
    SECTION_NAME = 'marshalling'

    @property
    def serializer(self):
        return self.get("serializer")

    @property
    def deserializer(self):
        return self.get("deserializer")


class MeniscusConfig(ConfigSectionInterface):
    SECTION_NAME = 'meniscus'

    @property
    def base_url(self):
        return self.get("base_url")

    @property
    def api_version(self):
        return self.get("api_version")

    @property
    def db_host(self):
        return json_to_dict(self.get("db_hosts"))

    @property
    def db_name(self):
        return self.get("db_name")

    @property
    def db_username(self):
        return self.get("db_username")

    @property
    def db_password(self):
        return self.get("db_password")


class StorageConfig(ConfigSectionInterface):
    SECTION_NAME = 'meniscus-storage'

    @property
    def address(self):
        return self.get('address')


class TenantConfig(ConfigSectionInterface):
    SECTION_NAME = 'meniscus-tenant'

    @property
    def hostname(self):
        return self.get("hostname")

    @property
    def ip_address_v4(self):
        return self.get("ip_address_v4")

    @property
    def ip_address_v6(self):
        return self.get("ip_address_v6")

    @property
    def producer_name(self):
        return self.get("producer_name")

    @property
    def producer_pattern(self):
        return self.get("producer_pattern")

    @property
    def producer_durable(self):
        return self.get_boolean("producer_durable")

    @property
    def producer_encrypted(self):
        return self.get_boolean("producer_encrypted")

    @property
    def profile_name(self):
        return self.get("profile_name")


class CorrelationConfig(ConfigSectionInterface):
    SECTION_NAME = 'meniscus-correlation'

    @property
    def correlator_base_url(self):
        return self.get('correlator_base_url')

    @property
    def syslog_endpoint(self):
        return self.get('syslog_endpoint')

    @property
    def host(self):
        return self.get('host')

    @property
    def pname(self):
        return self.get('pname')

    @property
    def time(self):
        return self.get('time')

    @property
    def native(self):
        return json_to_dict(self.get('native'))
