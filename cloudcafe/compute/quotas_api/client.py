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
from cloudcafe.compute.quotas_api.models.quotas import Quota
from cloudcafe.compute.quotas_api.models.requests import UpdateQuotaRequest


class QuotasClient(AutoMarshallingHTTPClient):

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
        super(QuotasClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_quota(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Returns a quota for tenant_id
        @param: tenant_id: id of tenant
        @type: String
        @return: resp
        @rtype: Request.responses
        """
        url = "{url}/os-quota-sets/{tenant_id}".format(url=self.url,
                                                       tenant_id=tenant_id)
        quota_response = self.request('GET', url,
                                      response_entity_type=Quota,
                                      requestslib_kwargs=requestslib_kwargs)
        return quota_response

    def get_default_quota(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Returns default quota for tenant_id
        @param: tenant_id: id of tenant
        @type: String
        @return: resp
        @rtype: Request.responses
        """
        url = "{url}/os-quota-sets/{tenant_id}/" \
              "defaults".format(url=self.url, tenant_id=tenant_id)
        quota_response = self.request('GET', url,
                                      response_entity_type=Quota,
                                      requestslib_kwargs=requestslib_kwargs)
        return quota_response

    def update_quota(self, tenant_id, **request_args):
        """
        @summary: Returns updated quota for tenant_id
        @param: tenant_id: id of tenant
        @type: String
        @param: request_args: key-value pair of attibutes
            have to be updated.
        @return: resp
        @rtype: Request.responses
        """
        update_quota_request_object = UpdateQuotaRequest(**request_args)
        url = "{url}/os-quota-sets/{tenant_id}".format(url=self.url,
                                                       tenant_id=tenant_id)
        quota_response = self.request('PUT', url,
                                      response_entity_type=Quota,
                                      request_entity=
                                      update_quota_request_object)
        return quota_response

    def delete_quota(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: deletes quota for tenant_id
        @param: tenant_id: id of tenant
        @type: String
        @param: request_args: key-value pair of attibutes
            have to be updated.
        @return: resp
        @rtype: Request.responses
        """
        url = "{url}/os-quota-sets/{tenant_id}".format(url=self.url,
                                                       tenant_id=tenant_id)
        quota_response = self.request('DELETE', url,
                                      requestslib_kwargs=requestslib_kwargs)
        return quota_response
