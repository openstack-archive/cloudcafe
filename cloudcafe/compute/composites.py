from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.blockstorage.composites import VolumesAutoComposite
from cloudcafe.compute.config import ComputeEndpointConfig, MarshallingConfig
from cloudcafe.compute.flavors_api.client import FlavorsClient
from cloudcafe.compute.flavors_api.config import FlavorsConfig
from cloudcafe.compute.images_api.client import ImagesClient
from cloudcafe.compute.images_api.config import ImagesConfig
from cloudcafe.compute.servers_api.client import ServersClient
from cloudcafe.compute.servers_api.config import ServersConfig
from cloudcafe.compute.images_api.behaviors import ImageBehaviors
from cloudcafe.compute.servers_api.behaviors import ServerBehaviors
from cloudcafe.compute.volume_attachments_api.client \
    import VolumeAttachmentsAPIClient
from cloudcafe.compute.volume_attachments_api.config \
    import VolumeAttachmentsAPIConfig
from cloudcafe.compute.volume_attachments_api.behaviors \
    import VolumeAttachmentsAPI_Behaviors


class _ComputeAuthComposite(MemoizedAuthServiceComposite):

    def __init__(self):
        self.endpoint_config = ComputeEndpointConfig()
        self.marshalling_config = MarshallingConfig()
        super(_ComputeAuthComposite, self).__init__(
            self.endpoint_config.compute_endpoint_name,
            self.endpoint_config.region)

        self.servers_url = self.public_url

        if self.endpoint_config.compute_endpoint_url:
            self.servers_url = '{0}/{1}'.format(
                self.endpoint_config.compute_endpoint_url,
                self.tenant_id)

        self.client_args = {
            'url': self.servers_url,
            'auth_token': self.token_id,
            'serialize_format': self.marshalling_config.serializer,
            'deserialize_format': self.marshalling_config.deserializer}


class ImagesComposite(object):
    behavior_class = ImageBehaviors

    def __init__(self):
        self.compute_auth_composite = _ComputeAuthComposite()
        self.config = ImagesConfig()
        self.client = ImagesClient(**self.compute_auth_composite.client_args)
        self.behaviors = None


class ServersComposite(object):
    behavior_class = ServerBehaviors

    def __init__(self):
        self.compute_auth_composite = _ComputeAuthComposite()
        self.config = ServersConfig()
        self.client = ServersClient(**self.compute_auth_composite.client_args)
        self.behaviors = None


class FlavorsComposite(object):

    def __init__(self):
        self.compute_auth_composite = _ComputeAuthComposite()
        self.config = FlavorsConfig()
        self.client = FlavorsClient(**self.compute_auth_composite.client_args)
        self.behaviors = None


class VolumeAttachmentsComposite(object):
    behavior_class = VolumeAttachmentsAPI_Behaviors

    def __init__(self):
        self.compute_auth_composite = _ComputeAuthComposite()
        self.config = VolumeAttachmentsAPIConfig()
        self.client = VolumeAttachmentsAPIClient(
            **self.compute_auth_composite.client_args)
        self.behaviors = None


class ComputeIntegrationComposite(object):

    def __init__(self):
        self.servers = ServersComposite()
        self.flavors = FlavorsComposite()
        self.images = ImagesComposite()
        self.volumes = VolumesAutoComposite()
        self.volume_attachments = VolumeAttachmentsComposite()

        self.servers.behaviors = self.servers.behavior_class(
            self.servers.client, self.servers.config, self.images.config,
            self.flavors.config)

        self.images.behaviors = self.images.behavior_class(
            self.images.client, self.servers.client, self.images.config)

        self.volume_attachments.behaviors = \
            self.volume_attachments.behavior_class(
                self.volume_attachments.client, self.volume_attachments.config,
                self.volumes.client)
