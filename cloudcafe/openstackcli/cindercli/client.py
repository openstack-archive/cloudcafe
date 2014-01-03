from cloudcafe.openstackcli.common.client import BaseOpenstackPythonCLI_Client
from cloudcafe.openstackcli.cindercli.models import responses as \
    CinderResponses


class CinderCLI(BaseOpenstackPythonCLI_Client):

    _KWMAP = {
        'volume_service_name': 'volume-service-name',
        'os_volume_api_version': 'os-volume-api-version'}

    # Make sure to include all openstack common cli paramaters in addition to
    # the cinder specific ones
    _KWMAP.update(BaseOpenstackPythonCLI_Client._KWMAP)

    #The client command the must precede any call to the cli
    _CMD = 'cinder'

    def __init__(
            self, volume_service_name=None, os_volume_api_version=None,
            **kwargs):
        super(CinderCLI, self).__init__(**kwargs)
        self.volume_service_name = volume_service_name
        self.os_volume_api_version = os_volume_api_version

# Volumes
    def create_volume(
            self, size, snapshot_id=None, source_volid=None, image_id=None,
            display_name=None, display_description=None, volume_type=None,
            availability_zone=None, metadata=None):

        metadata = self._dict_to_string(metadata)

        _response_type = CinderResponses.VolumeResponse
        _cmd = 'create'
        _kwmap = {
            'snapshot_id': 'snapshot-id',
            'source_volid': 'source-volid',
            'image_id': 'image-id',
            'display_name': 'display-name',
            'display_description': 'display-description',
            'volume_type': 'volume-type',
            'availability_zone': 'availability-zone',
            'metadata': 'metadata'}
        return self._process_command()

    def show_volume(self, volume_id):
        _cmd = 'show'
        _response_type = CinderResponses.VolumeResponse
        return self._process_command()

    def delete_volume(self, volume_name_or_id):
        _cmd = 'delete'
        return self._process_command()

    def list_volumes(self, display_name=None, status=None, all_tenants=False):

        all_tenants = 1 if all_tenants is True else 0
        _response_type = CinderResponses.VolumeListResponse
        _cmd = 'list'
        _kwmap = {
            'display_name': 'display-name',
            'status': 'status',
            'all_tenants': 'all-tenants'}
        return self._process_command()

# Snapshots
    def create_snapshot(
            self, volume_id, force=True, display_name=None,
            display_description=None):

        force = 'True' if force else 'False'
        _kwmap = {
            'force': 'force',
            'display_name': 'display-name',
            'display_description': 'display-description'}
        _cmd = 'snapshot-create'
        _response_type = CinderResponses.SnapshotResponse
        return self._process_command()

    def list_snapshots(self):
        _cmd = 'snapshot-list'
        _response_type = CinderResponses.SnapshotListResponse
        return self._process_command()

    def show_snapshot(self, snapshot_id):
        _cmd = 'snapshot-show'
        _response_type = CinderResponses.SnapshotResponse
        return self._process_command()

# Volume Types
    def list_volume_types(self):
        _cmd = 'type-list'
        _response_type = CinderResponses.VolumeTypeListResponse
        return self._process_command()
