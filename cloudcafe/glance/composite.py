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
    AltOneUserConfig, ImagesConfig, MarshallingConfig, AltTwoUserConfig)


class ImagesAuthComposite(MemoizedAuthServiceComposite):
    def __init__(self):
        glance_config = ImagesConfig()
        super(ImagesAuthComposite, self).__init__(
            glance_config.endpoint_name, glance_config.region)


class ImagesAuthCompositeAltOne(MemoizedAuthServiceComposite):
    def __init__(self):
        glance_config = ImagesConfig()
        user_config = AltOneUserConfig()
        super(ImagesAuthCompositeAltOne, self).__init__(
            glance_config.endpoint_name, glance_config.region,
            user_config=user_config)


class ImagesAuthCompositeAltTwo(MemoizedAuthServiceComposite):
    def __init__(self):
        glance_config = ImagesConfig()
        user_config = AltTwoUserConfig()
        super(ImagesAuthCompositeAltTwo, self).__init__(
            glance_config.endpoint_name, glance_config.region,
            user_config=user_config)


class ImagesComposite(object):
    def __init__(self, auth_composite):
        self.auth = auth_composite
        self.config = ImagesConfig()
        self.marshalling = MarshallingConfig()
        url = self.auth.public_url
        # If an override_url was provided, use it instead
        if self.config.override_url:
            url = self.config.override_url
        self.client = ImagesClient(
            url, self.auth.token_id, self.marshalling.serializer,
            self.marshalling.deserializer)

        self.behaviors = ImagesBehaviors(
            glance_client=self.client, glance_config=self.config)
