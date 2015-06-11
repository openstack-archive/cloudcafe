"""
Copyright 2015 Rackspace

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

import json

from cafe.engine.models.base import AutoMarshallingModel


class IPAssociationRequest(AutoMarshallingModel):
    """
    @summary: IP Association model request object for the Shared IPs Rackspace
        Compute v2.0 API extension for creating, by an API PUT call,
        a Shared IP addresses association with a server instance
    """

    def __init__(self, **kwargs):
        super(IPAssociationRequest, self).__init__()
        # Currently the IPAssociation is done without the need of a
        # request body with the following API call,
        # PUT https://{novaUri}/{version}/servers/{serverId}/ip_associations/{ipAddressId}
        # Still, the API should accept the empty main_body below, if given.

    def _obj_to_json(self):

        body = {}

        # Removing optional params not given
        # body = self._remove_empty_values(body)
        main_body = {'ip_association': body}
        return json.dumps(main_body)
