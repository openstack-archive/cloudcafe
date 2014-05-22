from cloudcafe.openstackcli.common.client import BaseOpenstackPythonCLI_Client
from cloudcafe.openstackcli.novacli.models import responses


class NovaCLI(BaseOpenstackPythonCLI_Client):

    _KWMAP = {
        'os_cache': 'os-cache',
        'timings': 'timings',
        'timeout': 'timeout',
        'os_tenant_id': 'os-tenant-id',
        'os_auth_system': 'os-auth-system',
        'service_type': 'service-type',
        'service_name': 'service-name',
        'volume_service_name': 'volume-service-name',
        'os_compute_api_version': 'os-compute-api-version',
        'bypass_url': 'bypass-url',
        'os_auth_url': 'os-auth-url',
        'endpoint_type': 'endpoint-type',
        'insecure': 'insecure'}

    # Make sure to include all openstack common cli paramaters in addition to
    # the nova specific ones
    _KWMAP.update(BaseOpenstackPythonCLI_Client._KWMAP)

    # The client command that must precede any cli call, essentially the
    # name of the cli client.
    _CMD = 'nova'

    def __init__(
            self, os_cache=None, timings=None, timeout=None, os_tenant_id=None,
            os_auth_system=None, service_type=None, service_name=None,
            volume_service_name=None, os_compute_api_version=None,
            insecure=False, bypass_url=None, os_auth_url=None,
            endpoint_type=None, **kwargs):

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
        self.os_tenant_id = os_tenant_id
        self.os_auth_url = os_auth_url
        self.endpoint_type = endpoint_type

    def boot(
            self, name, no_service_net=None, no_public=None, disk_config=None,
            flavor=None, image=None, image_with=None, boot_volume=None,
            snapshot=None, num_instances=None, meta=None, file_=None,
            key_name=None, user_data=None, availability_zone=None,
            security_groups=None, block_device_mapping=None, block_device=None,
            swap=None, ephemeral=None, hint=None, nic=None, config_drive=None):
        """Expected input for parameters

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

        no_service_net = True if no_service_net else False
        no_public = True if no_public else False
        meta = self._multiplicable_flag_data_to_string('meta', meta)
        image_with = self._dict_to_string(image_with)
        file_ = self._dict_to_string(file_)
        block_device = self._dict_to_string(block_device)
        ephemeral = self._dict_to_string(ephemeral)
        hint = self._dict_to_string(hint)
        nic = self._dict_to_string(nic)
        block_device_mapping = self._dict_to_string(block_device_mapping)

        _response_type = responses.ServerResponse
        return self._process_command()

    def show(self, server_id):
        _cmd = 'show'
        _response_type = responses.ServerResponse
        return self._process_command()

    def list(self):
        _cmd = 'list'
        _response_type = responses.ServerListResponse
        return self._process_command()

    def image_list(self):
        _cmd = 'image-list'
        _response_type = responses.ImageListResponse
        return self._process_command()

    def image_show(self, image_id):
        _cmd = 'image-show'
        _response_type = responses.ImageShowResponse
        return self._process_command()

    def flavor_list(self):
        _cmd = 'flavor-list'
        _response_type = responses.FlavorListResponse
        return self._process_command()

    def flavor_show(self, flavor_id):
        _cmd = 'flavor-show'
        _response_type = responses.FlavorShowResponse
        return self._process_command()

    def volume_attach(self, server_id, volume_id, device):
        _cmd = 'volume-attach'
        _response_type = responses.VolumeAttachResponse
        return self._process_command()

    def volume_create(
            self, size, snapshot_id=None, image_id=None, display_name=None,
            display_description=None, volume_type=None,
            availability_zone=None):
        _cmd = 'volume-create'
        _kwmap = {
            'snapshot_id': 'snapshot-id',
            'image_id': 'image-id',
            'display_name': 'display-name',
            'display_description': 'display-description',
            'volume_type': 'volume-type',
            'availability_zone': 'availability-zone'}

        _response_type = responses.VolumeCreateResponse
        return self._process_command()

    def volume_delete(self, volume_id):
        _cmd = 'volume-delete'
        return self._process_command()

    def volume_detach(self, server_id, volume_id, device):
        _cmd = 'volume-detach'
        return self._process_command()

    def volume_list(self):
        _cmd = 'volume-list'
        _response_type = responses.VolumeListResponse
        return self._process_command()

    def volume_show(self, volume_id):
        _cmd = 'volume-show'
        _response_type = responses.VolumeCreateResponse
        return self._process_command()

    def volume_snapshot_create(
            self, volume_id, force=False, display_name=None,
            display_description=None):

        _cmd = 'volume-snapshot-create'

        force = True if force else False

        _response_type = responses.VolumeSnapshotCreateResponse
        return self._process_command()

    def volume_snapshot_delete(self, snapshot_id):
        _cmd = 'volume-snapshot-delete'
        return self._process_command()

    def volume_snapshot_list(self):
        _cmd = 'volume-snapshot-list'
        _response_type = responses.VolumeSnapshotListResponse
        return self._process_command()

    def volume_snapshot_show(self, snapshot_id):
        _cmd = 'volume-snapshot-show'
        _response_type = responses.VolumeSnapshotShowResponse
        return self._process_command()

    def volume_type_create(self, name):
        _cmd = 'volume-type-create'
        _response_type = responses.VolumeTypeCreateResponse
        return self._process_command()

    def volume_type_delete(self, volume_type_id):
        _cmd = 'volume-type-delete'

    def volume_type_list(self):
        _cmd = 'volume-type-list'
        _response_type = resposnes.VolumeTypeListResponse
        return self._process_command()

    def volume_update(self, server_id, attachment_id, volume_id):
        # TODO: Investigate this method.  It's possibly a bug that this
        # updates the volume attachment.  Currently seems broken.
        # Performs a PUT against
        # servers/{server-id}/os-volume_attachments/{volume-atachment-id}:
        # with this payload: '{"volumeAttachment": {"volumeId": "<a vol id>"}}'
        _cmd = 'volume-update'
        return self._process_command()
