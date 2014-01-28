from time import time

from cafe.engine.behaviors import behavior

from cloudcafe.common.tools.datagen import random_string
from cloudcafe.openstackcli.novacli.client import NovaCLI
from cloudcafe.openstackcli.novacli.config import NovaCLI_Config
from cloudcafe.openstackcli.common.behaviors import \
    OpenstackCLI_BaseBehavior, OpenstackCLI_BehaviorError

from cloudcafe.compute.servers_api.config import ServersConfig
from cloudcafe.compute.images_api.config import ImagesConfig
from cloudcafe.compute.flavors_api.config import FlavorsConfig
from cloudcafe.compute.common.types import \
    NovaServerStatusTypes as ServerStates
from cloudcafe.compute.common.exceptions import \
    TimeoutException, BuildErrorException, RequiredResourceException


class NovaCLIBehaviorError(OpenstackCLI_BehaviorError):
    pass


class NovaCLI_Behaviors(OpenstackCLI_BaseBehavior):

    _default_error = NovaCLIBehaviorError

    def __init__(
            self, nova_cli_client=None, nova_cli_config=None,
            servers_api_config=None, images_api_config=None,
            flavors_api_config=None):

        super(NovaCLI_Behaviors, self).__init__()
        self.nova_cli_client = nova_cli_client
        self.nova_cli_config = nova_cli_config or NovaCLI_Config()

        self.servers_api_config = servers_api_config or ServersConfig()
        self.images_api_config = images_api_config or ImagesConfig()
        self.flavors_api_config = flavors_api_config or FlavorsConfig()

    @behavior(NovaCLI)
    def create_available_server(
            self, name, flavor=None, image=None, no_service_net=None,
            no_public=None, disk_config=None, image_with=None,
            boot_volume=None, snapshot=None, num_instances=None, meta=None,
            file_=None, key_name=None, user_data=None, availability_zone=None,
            security_groups=None, block_device_mapping=None, block_device=None,
            swap=None, ephemeral=None, hint=None, nic=None, config_drive=None):
        """
            Expected input for non-string parameters

            disk_config:          'auto' or 'manual'
            image-with:           {key: value}
            meta:                 {key: value, [key2=value2, ...] }
            file_:                {dst-path: src-path}
            block_device_mapping: {dev-name: mapping}
            block_device:         {key=value, [key2=value2, ...] }
            ephemeral:            {'size': size, ['format': format]}
            hint:                 {key: value}
            nic:                  {'net-id'=net-uuid,
                                   'port-id'=port-uuid,
                                   ['v4-fixed-ip'=ip-addr]}

        """
        name = name or random_string('NovaCLI')
        image = image or self.images_api_config.primary_image
        flavor = flavor or self.flavors_api_config.primary_flavor

        failures = []
        attempts = self.servers_api_config.resource_build_attempts
        for attempt in range(attempts):

            self._log.debug(
                'Attempt {attempt} of {attempts} to create server with the '
                'NovaCLI.'.format(attempt=attempt + 1, attempts=attempts))

            resp = self.nova_cli_client.create_server(
                name=name, flavor=flavor, image=image,
                no_service_net=no_service_net, no_public=no_public,
                disk_config=disk_config, image_with=image_with,
                boot_volume=boot_volume, snapshot=snapshot,
                num_instances=num_instances, meta=meta, file_=file_,
                key_name=key_name, user_data=user_data,
                availability_zone=availability_zone,
                security_groups=security_groups,
                block_device_mapping=block_device_mapping,
                block_device=block_device,
                swap=swap, ephemeral=ephemeral, hint=hint, nic=nic,
                config_drive=config_drive)
            server = resp.entity

            if server is None:
                raise self._default_error("Unable to parse nova boot response")

            try:
                resp = self.wait_for_server_status(
                    server.id_, ServerStates.ACTIVE)
                # Add the password from the create request
                # into the final response
                resp.entity.admin_pass = server.admin_pass
                return resp
            except (TimeoutException, BuildErrorException) as ex:
                msg = 'Failed to build server {server_id}'.format(
                    server_id=server.id_)
                self._log.exception(msg)
                failures.append(ex.message)
                self.nova_cli_client.delete_server(server.id_)

        raise RequiredResourceException(
            'Failed to successfully build a server after '
            '{attempts} attempts: {failures}'.format(
                attempts=attempts, failures=failures))

    def wait_for_server_status(
            self, server_id, desired_status, interval_time=None, timeout=None):

        interval_time = int(
            interval_time or self.servers_api_config.server_status_interval)
        timeout = int(timeout or self.servers_api_config.server_build_timeout)
        end_time = time.time() + timeout

        time.sleep(interval_time)
        while time.time() < end_time:
            resp = self.nova_cli_client.show_server(server_id)
            server = resp.entity

            if server.status.lower() == ServerStates.ERROR.lower():
                raise BuildErrorException(
                    'Build failed. Server with uuid "{0} entered ERROR status.'
                    .format(server.id))

            if server.status == desired_status:
                break
            time.sleep(interval_time)

        else:
            raise TimeoutException(
                "wait_for_server_status ran for {0} seconds and did not "
                "observe server {1} reach the {2} status.".format(
                    timeout, server_id, desired_status))

        return resp
