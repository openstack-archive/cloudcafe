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
from cloudcafe.meniscus.correlator_api.models.publish \
    import PublishMessage, JobInformation
from cafe.engine.clients.rest import AutoMarshallingRestClient


class PublishingClient(AutoMarshallingRestClient):

    def __init__(self, url, api_version, serialize_format=None,
                 deserialize_format=None):
        """
        Client to interact with the Correlator API to "publish" event messages
        """
        super(PublishingClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.url = url
        self.api_version = api_version

    def publish(self, tenant_id, message_token, host, pname, time, native):
        """
        POST {base_url}/{api_version}/{tenant_id}/publish
        Publishes a message to a Correlator worker.
        @param message_token: In Meniscus, this is the tenant token
        @return: Response from the Rest Client
        """
        remote = '{base}/{version}/tenant/{tenant_id}/publish'.format(
            base=self.url,
            version=self.api_version,
            tenant_id=tenant_id)
        body = PublishMessage(host=host, pname=pname,
                              time=time, native=native)
        headers = {'MESSAGE-TOKEN': message_token}
        response = self.request('POST',
                                url=remote,
                                headers=headers,
                                request_entity=body,
                                response_entity_type=JobInformation)
        return response
