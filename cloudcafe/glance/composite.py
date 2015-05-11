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

from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.glance.behaviors import ImagesBehaviors
from cloudcafe.glance.client import ImagesClient
from cloudcafe.glance.config import (
    AdminAuthConfig, AdminUserConfig, AltOneUserConfig, AltTwoUserConfig,
    ImagesAdminEndpointConfig, ImagesConfig, ImagesEndpointConfig,
    MarshallingConfig)


class ImagesAuthComposite(MemoizedAuthServiceComposite):
    def __init__(self):
        self.images_endpoint_config = ImagesEndpointConfig()
        super(ImagesAuthComposite, self).__init__(
            region=self.images_endpoint_config.region,
            service_name=self.images_endpoint_config.endpoint_name)


class ImagesAuthCompositeAltOne(MemoizedAuthServiceComposite):
    def __init__(self):
        self.images_endpoint_config = ImagesEndpointConfig()
        user_config = AltOneUserConfig()
        super(ImagesAuthCompositeAltOne, self).__init__(
            region=self.images_endpoint_config.region,
            service_name=self.images_endpoint_config.endpoint_name,
            user_config=user_config)


class ImagesAuthCompositeAltTwo(MemoizedAuthServiceComposite):
    def __init__(self):
        self.images_endpoint_config = ImagesEndpointConfig()
        user_config = AltTwoUserConfig()
        super(ImagesAuthCompositeAltTwo, self).__init__(
            region=self.images_endpoint_config.region,
            service_name=self.images_endpoint_config.endpoint_name,
            user_config=user_config)


class ImagesAuthCompositeAdmin(MemoizedAuthServiceComposite):
    def __init__(self):
        self.images_endpoint_config = ImagesAdminEndpointConfig()
        user_config = AdminUserConfig()
        endpoint_config = AdminAuthConfig()
        super(ImagesAuthCompositeAdmin, self).__init__(
            endpoint_config=endpoint_config,
            region=self.images_endpoint_config.region,
            service_name=self.images_endpoint_config.endpoint_name,
            user_config=user_config)


class ImagesComposite(object):
    def __init__(self, auth_composite):
        self.auth = auth_composite
        self.config = ImagesConfig()
        self.marshalling = MarshallingConfig()
        # If an override_url was provided, use it instead
        if self.auth.images_endpoint_config.override_url:
            self.url = self.auth.images_endpoint_config.override_url
        else:
            self.url = self.auth.public_url
        self.client = ImagesClient(
            self.url, self.auth.token_id, self.marshalling.serializer,
            self.marshalling.deserializer)

        self.behaviors = ImagesBehaviors(
            images_client=self.client, images_config=self.config)
