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
    def attachment_timeout(self):
        """
        Maximum time to wait before assuming the attachment will not succeede
        """
        return int(self.get("attachment_timeout", 120))

    @property
    def attachment_propagation_timeout(self):
        """
        Seconds it should take for a new volume attachment instance to
        propagate through cells.
        """
        return int(self.get("attachment_propagation_timeout", 60))

    @property
    def api_poll_rate(self):
        """
        Seconds to wait between polling the os-volume_attachments API in loops.
        """
        return int(self.get("api_poll_rate", 5))

    @property
    def api_poll_failure_retry_limit(self):
        """
        Times to retry polling the attachments api when it recieves an error
        response.
        """
        return int(self.get("api_poll_failure_retry_limit", 3))
