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

from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.compute.hypervisors_api.model.hypervisor\
    import HypervisorMin, Hypervisor


class HypervisorsClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL for the compute service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(HypervisorsClient, self).__init__(serialize_format,
                                                deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_hypervisors(self, requestslib_kwargs=None):
        """
        @summary: Returns a list of hypervisors
        @return: List of hypervisors
        @rtype: C{list}
        """
        url = "{url}/os-hypervisors".format(url=self.url)
        hypervisor_res = self.request('GET', url,
                                      response_entity_type=HypervisorMin,
                                      requestslib_kwargs=requestslib_kwargs)
        return hypervisor_res

    def list_hypervisors_in_detail(self, requestslib_kwargs=None):
        """
        @summary: Returns a list of hypervisors
        @return: List of hypervisors
        @rtype: C{list}
        """
        url = "{url}/os-hypervisors/detail".format(url=self.url)
        hypervisor_res = self.request('GET', url,
                                      response_entity_type=Hypervisor,
                                      requestslib_kwargs=requestslib_kwargs)
        return hypervisor_res

    def list_hypervisor_servers(self, hypervisor_hostname,
                                requestslib_kwargs=None):
        """
        @summary: Returns a list of servers in a hypervisor host
        @return: List of servers
        @rtype: C{list}
        """
        url = "{url}/os-hypervisors/{hypervisor_hostname}/servers".\
            format(url=self.url, hypervisor_hostname=hypervisor_hostname)
        hypervisor_res = self.request('GET', url,
                                      response_entity_type=HypervisorMin,
                                      requestslib_kwargs=requestslib_kwargs)
        return hypervisor_res
