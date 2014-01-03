from cloudcafe.openstackcli.common.client import BaseOpenstackPythonCLI_Client
from cloudcafe.openstackcli.novacli.models import responses


class NovaCLI(BaseOpenstackPythonCLI_Client):

    _KWMAP = {
        'os_cache': 'os-cache',
        'timings': 'timings',
        'timeout': 'timeout',
        'os_auth_system': 'os-auth-system',
        'service_type': 'service-type',
        'service_name': 'service-name',
        'volume_service_name': 'volume-service-name',
        'os_compute_api_version': 'os-compute-api-version',
        'bypass_url': 'bypass-url',
        'insecure': 'insecure'}

    # Make sure to include all openstack common cli paramaters in addition to
    # the nova specific ones
    _KWMAP.update(BaseOpenstackPythonCLI_Client._KWMAP)

    #The client command the must precede any call to the cli
    _CMD = 'nova'

    def __init__(
            self, os_cache=None, timings=None, timeout=None,
            os_auth_system=None, service_type=None, service_name=None,
            volume_service_name=None, os_compute_api_version=None,
            insecure=True, bypass_url=None, **kwargs):

        super(NovaCLI, self).__init__(**kwargs)
        self.os_cache = os_cache
        self.timings = timings
        self.timeout = timeout
        self.os_auth_system = os_auth_system
        self.service_type = service_type
        self.service_name = service_name
        self.volume_service_name = volume_service_name
        self.os_compute_api_version = os_compute_api_version
        self.insecure = insecure
        self.bypass_url = bypass_url

    def create_server(
            self, name, no_service_net=None, no_public=None, disk_config=None,
            flavor=None, image=None, image_with=None, boot_volume=None,
            snapshot=None, num_instances=None, meta=None, file_=None,
            key_name=None, user_data=None, availability_zone=None,
            security_groups=None, block_device_mapping=None, block_device=None,
            swap=None, ephemeral=None, hint=None, nic=None, config_drive=None):
        """
            Expected input for parameters

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
        _cmd = 'boot'
        _kwmap = {
            'no_service_net': 'no-service-net',
            'no_public': 'no-public',
            'disk_config': 'disk-config',
            'flavor': 'flavor',
            'image': 'image',
            'image_with': 'image-with',
            'boot_volume': 'boot-volume',
            'snapshot': 'snapshot',
            'num_instances': 'num-instances',
            'meta': 'meta',
            'file_': 'file',
            'key_name': 'key-name',
            'user_data': 'user-data',
            'availability_zone': 'availability-zone',
            'security_groups': 'security-groups',
            'block_device_mapping': 'block-device-mapping',
            'block_device': 'block-device',
            'swap': 'swap',
            'ephemeral': 'ephemeral',
            'hint': 'hint',
            'nic': 'nic',
            'config_drive': 'config-drive'}

        meta = self._multiplicable_flag_data_to_string('meta', meta)
        image_with = self._dict_to_key_value_string(image_with)
        file_ = self._dict_to_key_value_string(file_)
        block_device = self._dict_to_key_value_string(block_device)
        ephemeral = self._dict_to_key_value_string(ephemeral)
        hint = self._dict_to_key_value_string(hint)
        nic = self._dict_to_key_value_string(nic)
        block_device_mapping = self._dict_to_key_value_string(
            block_device_mapping)

        _response_type = responses.ServerResponse
        return self._process_command()

    def show_server(self, server_id):
        _cmd = 'show'
        _response_type = responses.ServerResponse
        return self._process_command()
