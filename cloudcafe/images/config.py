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


class ImagesConfig(ConfigSectionInterface):

    SECTION_NAME = 'images'

    @property
    def base_url(self):
        """Base URL where Images API is reached"""
        return self.get('base_url')

    @property
    def primary_image(self):
        """Primary image ID"""
        return self.get('primary_image')

    @property
    def secondary_image(self):
        """Secondary image ID"""
        return self.get('secondary_image')

    @property
    def image_status_interval(self):
        return int(self.get('image_status_interval'))

    @property
    def snapshot_timeout(self):
        return int(self.get('snapshot_timeout'))

    @property
    def remote_image(self):
        return self.get('remote_image')

    @property
    def http_image(self):
        return self.get('http_image')
