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

from cafe.engine.provider import BaseProvider

from cloudcafe.blockstorage.config import BlockStorageConfig
from cloudcafe.blockstorage.volumes_api.provider import VolumesProvider


class BlockStorageProvider(BaseProvider):

    def get_volumes_provider(self):

        # NEED TO IMPORT IDENTITY AND GET THESE THINGS
        blockstorage_config = BlockStorageConfig()
        blockstorage_service_name = blockstorage_config.identity_service_name
        blockstorage_region = blockstorage_config.region
        auth_token = '924ur802ur08j2f0984'
        volumes_url = 'http://volumes_url'
        tenant_id = '234234'

        return VolumesProvider(volumes_url, auth_token, tenant_id)


