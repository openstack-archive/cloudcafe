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


class VolumeAttachmentsAPIConfig(ConfigSectionInterface):

    SECTION_NAME = 'volume_attachments'

    @property
    def attachment_propagation_timeout(self):
        """
        Seconds it should take for a new volume attachment instance to
        propagate.
        """
        return self.get("attachment_propagation_timeout", 60)

    @property
    def api_max_poll_rate(self):
        """
        Seconds to wait between polling the os-volume_attachments API in loops.
        """
        return self.get("api_max_poll_rate", 5)
