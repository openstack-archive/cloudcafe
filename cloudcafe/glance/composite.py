
from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.glance.config import (
    AltUserConfig, ImagesConfig, MarshallingConfig, ThirdUserConfig)
from cloudcafe.glance.behaviors import ImagesBehaviors
from cloudcafe.glance.client import ImagesClient


class ImagesAuthComposite(MemoizedAuthServiceComposite):
    def __init__(self):
        glance_config = ImagesConfig()
        super(ImagesAuthComposite, self).__init__(
            glance_config.endpoint_name,
            glance_config.region)


class ImagesAuthCompositeAltOne(MemoizedAuthServiceComposite):
    def __init__(self):
        glance_config = ImagesConfig()
        user_config = AltUserConfig()
        super(ImagesAuthCompositeAltOne, self).__init__(
            glance_config.endpoint_name,
            glance_config.region,
            user_config=user_config)


class ImagesAuthCompositeAltTwo(MemoizedAuthServiceComposite):
    def __init__(self):
        glance_config = ImagesConfig()
        user_config = ThirdUserConfig()
        super(ImagesAuthCompositeAltTwo, self).__init__(
            glance_config.endpoint_name,
            glance_config.region,
            user_config=user_config)


class ImagesComposite(object):
    def __init__(self, auth_composite):
        self.auth = auth_composite
        self.config = ImagesConfig()
        self.marshalling = MarshallingConfig()
        self.client = ImagesClient(
            self.auth.public_url,
            self.auth.token_id,
            self.marshalling.serializer,
            self.marshalling.deserializer)

        self.behaviors = ImagesBehaviors(
            glance_client=self.client,
            glance_config=self.config)
