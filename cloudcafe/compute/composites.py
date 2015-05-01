"""
Copyright 2014 Rackspace

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

from cloudcafe.compute.cells_api.composites import CellsComposite
from cloudcafe.compute.config import UserAuthConfig, UserConfig, \
    ComputeAdminAuthConfig, ComputeAdminUserConfig
from cloudcafe.compute.extensions.config_drive.composites import \
    ConfigDriveComposite
from cloudcafe.compute.extensions.console_output_api.composites import \
    ConsoleOutputComposite
from cloudcafe.compute.extensions.keypairs_api.composites import \
    KeypairsComposite
from cloudcafe.compute.extensions.rescue_api.composites import RescueComposite
from cloudcafe.compute.extensions.security_groups_api.composites import \
    SecurityGroupsComposite
from cloudcafe.compute.extensions.vnc_console_api.composites import \
    VncConsoleComposite
from cloudcafe.compute.extensions.extensions_api.composites import \
    ExtensionComposite
from cloudcafe.compute.extensions.volumes_boot_api.composites import \
    BootFromVolumeComposite
from cloudcafe.compute.flavors_api.composites import FlavorsComposite
from cloudcafe.compute.hosts_api.composites import HostsComposite
from cloudcafe.compute.hypervisors_api.composites import HypervisorsComposite
from cloudcafe.compute.images_api.composites import ImagesComposite
from cloudcafe.compute.limits_api.composites import LimitsComposite
from cloudcafe.compute.quotas_api.composites import QuotasComposite
from cloudcafe.compute.servers_api.composites import ServersComposite
from cloudcafe.compute.volume_attachments_api.composites import \
    VolumeAttachmentsComposite
from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.blockstorage.composites import VolumesAutoComposite
from cloudcafe.compute.config import ComputeAdminEndpointConfig, \
    ComputeEndpointConfig, MarshallingConfig


class _ComputeAuthComposite(MemoizedAuthServiceComposite):
    _compute_endpoint_config = ComputeEndpointConfig
    _auth_endpoint_config = UserAuthConfig
    _auth_user_config = UserConfig

    def __init__(self, endpoint_config=None, user_config=None):
        self.compute_endpoint_config = self._compute_endpoint_config()
        self.marshalling_config = MarshallingConfig()
        self._auth_endpoint_config = \
            endpoint_config or self._auth_endpoint_config()
        self._auth_user_config = user_config or self._auth_user_config()

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
    _auth_endpoint_config = ComputeAdminAuthConfig
    _auth_user_config = ComputeAdminUserConfig


class ComputeComposite(object):
    _auth_composite = _ComputeAuthComposite

    def __init__(self, auth_composite=None):
        auth_composite = auth_composite or self._auth_composite()
        self.user = auth_composite._auth_user_config
        self.servers = ServersComposite(auth_composite)
        self.flavors = FlavorsComposite(auth_composite)
        self.images = ImagesComposite(auth_composite)
        self.keypairs = KeypairsComposite(auth_composite)
        self.console_output = ConsoleOutputComposite(auth_composite)
        self.rescue = RescueComposite(auth_composite)
        self.extension = ExtensionComposite(auth_composite)
        self.vnc_console = VncConsoleComposite(auth_composite)
        self.limits = LimitsComposite(auth_composite)
        self.quotas = QuotasComposite(auth_composite)
        self.hypervisors = HypervisorsComposite(auth_composite)
        self.cells = CellsComposite(auth_composite)
        self.hosts = HostsComposite(auth_composite)
        self.volume_attachments = VolumeAttachmentsComposite(auth_composite)
        self.boot_from_volume = BootFromVolumeComposite(auth_composite)
        self.config_drive = ConfigDriveComposite(auth_composite)
        self.security_groups = SecurityGroupsComposite(auth_composite)

        self.servers.behaviors = self.servers.behavior_class(
            servers_client=self.servers.client,
            images_client=self.images.client,
            servers_config=self.servers.config,
            images_config=self.images.config,
            flavors_config=self.flavors.config,
            security_groups_config=self.security_groups.config)

        self.boot_from_volume.behaviors = \
            self.boot_from_volume.behavior_class(
                servers_client=self.servers.client,
                images_client=self.images.client,
                servers_config=self.servers.config,
                images_config=self.images.config,
                flavors_config=self.flavors.config,
                server_behaviors=self.servers.behaviors,
                boot_from_volume_client=self.boot_from_volume.client,)

        self.images.behaviors = self.images.behavior_class(
            self.images.client, self.servers.client, self.images.config)

        self.config_drive.behaviors = self.config_drive.behavior_class(
            servers_client=self.servers.client,
            servers_config=self.servers.config,
            server_behaviors=self.servers.behaviors)


class ComputeAdminComposite(ComputeComposite):
    _auth_composite = _ComputeAdminAuthComposite


class ComputeIntegrationComposite(ComputeComposite):

    def __init__(
            self, compute_auth_composite=None,
            blockstorage_auth_composite=None):

        super(ComputeIntegrationComposite, self).__init__(
            auth_composite=compute_auth_composite)

        self.volumes = VolumesAutoComposite(
            auth_composite=blockstorage_auth_composite)

        self.volume_attachments.behaviors = \
            self.volume_attachments.behavior_class(
                self.volume_attachments.client,
                self.volume_attachments.config,
                self.volumes.client)
