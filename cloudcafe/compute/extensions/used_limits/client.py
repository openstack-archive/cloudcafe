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

from cafe.engine.http.client import AutoMarshallingHTTPClient
from cloudcafe.compute.extensions.used_limits.model.used_limits \
    import UsedLimits


class UsedLimitsClient(AutoMarshallingHTTPClient):

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
        super(UsedLimitsClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = 'application/{0}'.format(self.serialize_format)
        accept = 'application/{0}'.format(self.serialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_used_limits_for_user(self, user_tenant_id,
                                 requestslib_kwargs=None):
        """
        @summary: Returns the used limits of a particular tenant
        @return: Used Limits Response
        @rtype: Response
        """
        url = "{url}/limits?tenant_id={user_tenant_id}".\
            format(url=self.url, user_tenant_id=user_tenant_id)
        used_limits_res = self.request('GET', url,
                                       response_entity_type=UsedLimits,
                                       requestslib_kwargs=requestslib_kwargs)
        return used_limits_res
