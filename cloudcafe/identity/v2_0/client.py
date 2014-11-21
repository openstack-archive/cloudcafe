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
from cloudcafe.identity.common.client import BaseIdentityAPIClient
from cloudcafe.identity.v2_0.models import requests
from cloudcafe.identity.v2_0.models import responses


class IdentityServiceClient(BaseIdentityAPIClient):
    def __init__(
            self, url=None, serialize_format=None, deserialize_format=None,
            auth_token=None):
        super(IdentityServiceClient, self).__init__(
            url, serialize_format, deserialize_format, auth_token)
        self.url = '{0}'.format(self.url)

    def get_tenants(self, requestslib_kwargs=None):
        url = '{0}/tenants'.format(self.url)
        return self.get(
            url, response_entity_type=responses.TenantList,
            requestslib_kwargs=requestslib_kwargs)

    def get_tenant_by_id(self, tenant_id, requestslib_kwargs=None):
        url = '{0}/tenants/{1}'.format(self.url, tenant_id)
        return self.get(
            url, response_entity_type=responses.Tenant,
            requestslib_kwargs=requestslib_kwargs)

    def get_tenant_by_name(self, name, requestslib_kwargs=None):
        url = '{0}/tenants'.format(self.url)
        return self.get(
            url, params={'name': name}, response_entity_type=responses.Tenant,
            requestslib_kwargs=requestslib_kwargs)

    def get_user_roles(self, tenant_id, user_id, requestslib_kwargs=None):
        url = '{0}/tenants/{1}/users/{2}/roles'.format(
            self.url, tenant_id, user_id)
        return self.get(
            url, response_entity_type=responses.RoleList,
            requestslib_kwargs=requestslib_kwargs)

    def authenticate(
            self, username=None, password=None, tenant_name=None,
            tenant_id=None, token=None, requestslib_kwargs=None):
        url = '{0}/tokens'.format(self.url)
        request_entity = requests.Auth(
            username=username, password=password,
            tenant_name=tenant_name, token=token)

        return self.post(
            url, response_entity_type=responses.AuthResponse,
            request_entity=request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def validate_token(
            self, token_id, belongs_to=None, requestslib_kwargs=None):
        url = "{url}/tokens/{token_id}".format(url=self.url, token_id=token_id)

        return self.get(
            url, response_entity_type=responses.ValidationResponse,
            requestslib_kwargs=requestslib_kwargs)

    def get_user_by_name(self, name, requestslib_kwargs=None):
        url = '{0}/users'.format(self.url)
        return self.get(
            url, params={'name': name}, response_entity_type=responses.UserAlt,
            requestslib_kwargs=requestslib_kwargs)

    def get_user_by_id(self, user_id, requestslib_kwargs=None):
        url = "{0}/users/{1}".format(self.url, user_id)
        return self.get(
            url, response_entity_type=responses.UserAlt,
            requestslib_kwargs=requestslib_kwargs)

    def get_user_global_roles(self, user_id, requestslib_kwargs=None):
        url = "{0}/users/{1}/roles".format(self.url, user_id)
        return self.get(
            url, response_entity_type=responses.RoleList,
            requestslib_kwargs=requestslib_kwargs)
