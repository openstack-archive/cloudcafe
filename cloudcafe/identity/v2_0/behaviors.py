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
from cafe.engine.behaviors import BaseBehavior
from cafe.engine.http.client import AutoMarshallingHTTPClient

from cloudcafe.identity.v2_0.models import requests, responses


class IdentityServiceBehaviors(BaseBehavior):
    def __init__(self, service_client=None):
        self.client = service_client

    @classmethod
    @memoized
    def memoized_authenticate(
            cls, username, password, tenant_name, url, serialize_format="json",
            deserialize_format="json"):
        return cls.authenticate(
            username, password, tenant_name, url, serialize_format,
            deserialize_format)

    @classmethod
    def get_access_data(
            cls, username, password, tenant_name, url, serialize_format="json",
            deserialize_format="json"):
        return cls.authenticate(
            username, password, tenant_name, url, serialize_format,
            deserialize_format).entity

    @classmethod
    def authenticate(
            cls, username, password, tenant_name, url, serialize_format="json",
            deserialize_format="json"):
        if url.endswith("v2.0") or url.endswith("v2.0/"):
            url = '{0}/tokens'.format(url)
        else:
            url = '{0}/v2.0/tokens'.format(url)
        client = AutoMarshallingHTTPClient(
            serialize_format, deserialize_format)

        #both are set because AutoMarshallingHTTPClient doesn't handle headers
        #correctly
        client.default_headers["Content-Type"] = "application/{0}".format(
            serialize_format)
        client.default_headers["Accept"] = "application/{0}".format(
            deserialize_format)

        request_entity = requests.Auth(
            username=username, password=password, tenant_name=tenant_name)
        r = client.request(
            "POST", url, request_entity=request_entity,
            response_entity_type=responses.AuthResponse)

        if not r.ok:
            raise Exception("Failed to authenticate")
        r.entity = responses.AuthResponse.deserialize(
            r.content, deserialize_format)
        if r.entity is None:
            raise Exception("Failed to parse Auth response Body")
        return r
