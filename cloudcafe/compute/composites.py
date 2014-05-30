from cloudcafe.auth.config import UserAuthConfig, UserConfig, \
    ComputeAdminAuthConfig, ComputeAdminUserConfig
from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.blockstorage.composites import VolumesAutoComposite
from cloudcafe.compute.cells_api.client import CellsClient
from cloudcafe.compute.config import ComputeAdminEndpointConfig, \
    ComputeEndpointConfig, MarshallingConfig
from cloudcafe.compute.flavors_api.client import FlavorsClient
from cloudcafe.compute.flavors_api.config import FlavorsConfig
from cloudcafe.compute.hosts_api.client import HostsClient
from cloudcafe.compute.hypervisors_api.client import HypervisorsClient
from cloudcafe.compute.images_api.client import ImagesClient
from cloudcafe.compute.images_api.config import ImagesConfig
from cloudcafe.compute.extensions.console_output_api.client import \
    ConsoleOutputClient
from cloudcafe.compute.extensions.keypairs_api.client import KeypairsClient
from cloudcafe.compute.extensions.rescue_api.client import RescueClient
from cloudcafe.compute.extensions.vnc_console_api.client import \
    VncConsoleClient
from cloudcafe.compute.limits_api.client import LimitsClient
from cloudcafe.compute.quotas_api.client import QuotasClient
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
    _compute_endpoint_config = ComputeEndpointConfig
    _auth_endpoint_config = UserAuthConfig()
    _auth_user_config = UserConfig()

    def __init__(self):
        self.compute_endpoint_config = self._compute_endpoint_config()
        self.marshalling_config = MarshallingConfig()

        super(_ComputeAuthComposite, self).__init__(
            service_name=self.compute_endpoint_config.compute_endpoint_name,
            region=self.compute_endpoint_config.region,
            endpoint_config=self._auth_endpoint_config,
            user_config=self._auth_user_config)

        self.servers_url = self.public_url

        if self.compute_endpoint_config.compute_endpoint_url:
            self.servers_url = '{0}/{1}'.format(
                self.compute_endpoint_config.compute_endpoint_url,
                self.tenant_id)

        self.client_args = {
            'url': self.servers_url,
            'auth_token': self.token_id,
            'serialize_format': self.marshalling_config.serializer,
            'deserialize_format': self.marshalling_config.deserializer}


class _ComputeAdminAuthComposite(_ComputeAuthComposite):
    _compute_endpoint_config = ComputeAdminEndpointConfig
    _auth_endpoint_config = ComputeAdminAuthConfig()
    _auth_user_config = ComputeAdminUserConfig()


class BaseComputeComposite(object):

    def __init__(self, auth_composite):
        self.compute_auth_composite = auth_composite


class ImagesComposite(BaseComputeComposite):
    behavior_class = ImageBehaviors

    def __init__(self, auth_composite):
        super(ImagesComposite, self).__init__(auth_composite)
        self.config = ImagesConfig()
        self.client = ImagesClient(**self.compute_auth_composite.client_args)
        self.behaviors = None


class ServersComposite(BaseComputeComposite):
    behavior_class = ServerBehaviors

    def __init__(self, auth_composite):
        super(ServersComposite, self).__init__(auth_composite)
        self.config = ServersConfig()
        self.client = ServersClient(**self.compute_auth_composite.client_args)
        self.behaviors = None


class FlavorsComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(FlavorsComposite, self).__init__(auth_composite)
        self.config = FlavorsConfig()
        self.client = FlavorsClient(**self.compute_auth_composite.client_args)
        self.behaviors = None


class VolumeAttachmentsComposite(BaseComputeComposite):
    behavior_class = VolumeAttachmentsAPI_Behaviors

    def __init__(self, auth_composite):
        super(VolumeAttachmentsComposite, self).__init__(auth_composite)
        self.config = VolumeAttachmentsAPIConfig()
        self.client = VolumeAttachmentsAPIClient(
            **self.compute_auth_composite.client_args)
        self.behaviors = None


class KeypairsComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(KeypairsComposite, self).__init__(auth_composite)
        self.client = KeypairsClient(
            **self.compute_auth_composite.client_args)


class ConsoleOutputComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(ConsoleOutputComposite, self).__init__(auth_composite)
        self.client = ConsoleOutputClient(
            **self.compute_auth_composite.client_args)


class RescueComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(RescueComposite, self).__init__(auth_composite)
        self.client = RescueClient(**self.compute_auth_composite.client_args)


class VncConsoleComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(VncConsoleComposite, self).__init__(auth_composite)
        self.client = VncConsoleClient(
            **self.compute_auth_composite.client_args)


class LimitsComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(LimitsComposite, self).__init__(auth_composite)
        self.client = LimitsClient(**self.compute_auth_composite.client_args)


class QuotasComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(QuotasComposite, self).__init__(auth_composite)
        self.client = QuotasClient(**self.compute_auth_composite.client_args)


class HypervisorsComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(HypervisorsComposite, self).__init__(auth_composite)
        self.client = HypervisorsClient(
            **self.compute_auth_composite.client_args)


class CellsComposite(BaseComputeComposite):

    def __init__(self, auth_composite):
        super(CellsComposite, self).__init__(auth_composite)
        self.client = CellsClient(**self.compute_auth_composite.client_args)


class HostsComposite(object):

    def __init__(self, auth_composite):
        super(HostsComposite, self).__init__(auth_composite)
        self.client = HostsClient(**self.compute_auth_composite.client_args)


class ComputeComposite(object):
    _auth_composite = _ComputeAuthComposite

    def __init__(self):
        auth_composite = self._auth_composite()
        self.servers = ServersComposite(auth_composite)
        self.flavors = FlavorsComposite(auth_composite)
        self.images = ImagesComposite(auth_composite)
        self.keypairs = KeypairsComposite(auth_composite)
        self.console_output = ConsoleOutputComposite(auth_composite)
        self.rescue = RescueComposite(auth_composite)
        self.vnc_console = VncConsoleComposite(auth_composite)
        self.limits = LimitsComposite(auth_composite)
        self.quotas = QuotasComposite(auth_composite)
        self.hypervisors = HypervisorsComposite(auth_composite)
        self.cells = CellsComposite(auth_composite)
        self.hosts = HostsComposite(auth_composite)

        self.servers.behaviors = self.servers.behavior_class(
            self.servers.client, self.images.client, self.servers.config,
            self.images.config, self.flavors.config)

        self.images.behaviors = self.images.behavior_class(
            self.images.client, self.servers.client, self.images.config)


class ComputeAdminComposite(ComputeComposite):
    _auth_composite = _ComputeAdminAuthComposite


class ComputeIntegrationComposite(ComputeComposite):

    def __init__(self):
        super(ComputeIntegrationComposite, self).__init__()
        self.volume_attachments = VolumeAttachmentsComposite(
            self._auth_composite)
        self.volumes = VolumesAutoComposite()
        self.volume_attachments.behaviors = \
            self.volume_attachments.behavior_class(
                self.volume_attachments.client,
                self.volume_attachments.config,
                self.volumes.client)
