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

from cloudcafe.auth.config import UserAuthConfig as _UserAuthConfig
from cloudcafe.common.models.configuration import ConfigSectionInterface


class BlockstorageAltUserConfig(_UserAuthConfig):
    SECTION_NAME = 'blockstorage_alt_user'


class BlockStorageConfig(ConfigSectionInterface):

    SECTION_NAME = 'blockstorage'

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def region(self):
        return self.get('region')

    @property
    def availability_zone(self):
        return self.get('availability_zone')

    @property
    def service_endpoint_override(self):
        return self.get('service_endpoint_override')
