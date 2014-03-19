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

from cafe.drivers.unittest.decorators import memoized
from cafe.engine.behaviors import BaseBehavior, behavior
from cafe.engine.http.client import AutoMarshallingHTTPClient

from cloudcafe.identity.v2_0.client import IdentityServiceClient
from cloudcafe.identity.v2_0.models import requests, responses


class IdentityServiceBehaviors(BaseBehavior):
    def __init__(self, service_client=None):
        self.client = service_client

    @behavior(IdentityServiceClient)
    def get_access_data(
            self, username, password, tenant_name):
        """Supports configured user for auth provider compatability"""
        username = username or self.user_config.username
        password = password or self.user_config.password
        tenant_name = tenant_name or self.user_config.tenant_name

        access_data = None
        if username is not None and password is not None:
            response = self.client.authenticate(
                username=username, password=password,
                tenant_name=tenant_name)
            access_data = response.entity
        return access_data

    @classmethod
    @memoized
    def memoized_authenticate(
            cls, username, password, tenant_name, url, serialize_format="json",
            deserialize_format="json"):
        url = '{0}/tokens'.format(url)
        client = AutoMarshallingHTTPClient(
            serialize_format, deserialize_format)
        request_entity = requests.Auth(
            username=username, password=password, tenant_name=tenant_name)

        r = client.request(
            "POST", url, request_entity=request_entity,
            response_entity_type=responses.AuthResponse)
        r.entity = responses.AuthResponse.deserialize(r.content, "json")
        return r
