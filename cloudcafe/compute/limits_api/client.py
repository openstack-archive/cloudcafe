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
from cloudcafe.compute.limits_api.models.limit import Limits


class LimitsClient(AutoMarshallingRestClient):

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

        super(LimitsClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_limits(self, requestslib_kwargs=None):
        """
        @summary: Returns limits.
        @param requestslib_kwargs: Overrides any default values injected by
        the framework
        @type requestslib_kwargs:dict
        @return: limit_response
        @rtype: Limits Response Domain Object
        """
        url = '%s/limits' % (self.url)
        limit_response = self.request('GET', url,
                                      response_entity_type=Limits,
                                      requestslib_kwargs=requestslib_kwargs)
        return limit_response

    def _get_absolute_limits_property(self, limits_property=None):
        """
        @summary: Returns the value of the specified key from the
                absolute_limits dictionary
        @param requestslib_kwargs: Overrides any default values injected by
        the framework
        @type requestslib_kwargs:dict
        """
        if property is None:
            return None
        limits_response = self.get_limits()
        absolute_limits = vars(limits_response.entity).get('absolute')
        if absolute_limits is not None:
            return absolute_limits.get(limits_property)
        else:
            return None

    def get_max_server_meta(self):
        """
        @summary: Returns maximum number of metadata allowed for a server
        @return: Maximum number of server meta data
        @rtype:  Integer
        """
        return self._get_absolute_limits_property('maxServerMeta')

    def get_max_image_meta(self):
        """
        @summary: Returns maximum number of metadata allowed for an Image.
        @return: Maximum number of image meta data
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxImageMeta')

    def get_personality_file_limit(self):
        """
        @summary: Returns maximum number of personality files allowed for a
                  server
        @return: Maximum number of personality files.
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxPersonality')

    def get_personality_file_size_limit(self):
        """
        @summary: Returns the maximum size of a personality file.
        @return: Maximum size of a personality file.
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxPersonalitySize')

    def get_max_total_instances(self):
        """
        @summary: Returns maximum number of server allowed for a user
        @return: Maximum number of server
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxTotalInstances')

    def get_max_total_RAM_size(self):
        """
        @summary: Returns maximum RAM size to create servers for a user
        @return: Maximum RAM size
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxTotalRAMSize')

    def get_total_RAM_used(self):
        """
        @summary: Returns total RAM used by a user
        @return: total RAM used
        @rtype: Integer
        """
        return self._get_absolute_limits_property('totalRAMUsed')
