from cloudcafe.openstackcli.common.client import BaseOpenstackPythonCLI_Client
from cloudcafe.openstackcli.cindercli.models import responses as \
    CinderResponses


class CinderCLI(BaseOpenstackPythonCLI_Client):

    _KWMAP = {
        'volume_service_name': 'volume-service-name',
        'os_volume_api_version': 'os-volume-api-version',
        'os_auth_system': 'os-auth-system'}

    # Make sure to include all openstack common cli paramaters in addition to
    # the cinder specific ones
    _KWMAP.update(BaseOpenstackPythonCLI_Client._KWMAP)

    # The client command the must precede any call to the cli
    _CMD = 'cinder'

    def __init__(
            self, volume_service_name=None, os_volume_api_version=None,
            os_auth_system=None, **kwargs):
        super(CinderCLI, self).__init__(**kwargs)
        self.volume_service_name = volume_service_name
        self.os_volume_api_version = os_volume_api_version
        self.os_auth_system = os_auth_system

# Volumes
    def create(
            self, size, snapshot_id=None, source_volid=None, image_id=None,
            display_name=None, display_description=None, volume_type=None,
            availability_zone=None, metadata=None):
        """Create a new volume via the cinder command line client"""

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

    def show(self, volume_id):
        """Get details for a volume via the cinder command line client"""
        _cmd = 'show'
        _response_type = CinderResponses.VolumeResponse
        return self._process_command()

    def delete(self, volume_name_or_id):
        """delete a volume via the cinder command line client"""
        _cmd = 'delete'
        return self._process_command()

    def list(self, display_name=None, status=None, all_tenants=False):
        """List all volumes via the cinder command line client"""
        all_tenants = 1 if all_tenants is True else 0
        _response_type = CinderResponses.VolumeListResponse
        _cmd = 'list'
        _kwmap = {
            'display_name': 'display-name',
            'status': 'status',
            'all_tenants': 'all-tenants'}
        return self._process_command()

# Snapshots
    def snapshot_create(
            self, volume_id, force=True, display_name=None,
            display_description=None):
        """Create a snapshot of a volume via the cinder command line client"""
        force = 'True' if force else 'False'
        _kwmap = {
            'force': 'force',
            'display_name': 'display-name',
            'display_description': 'display-description'}
        _cmd = 'snapshot-create'
        _response_type = CinderResponses.SnapshotResponse
        return self._process_command()

    def snapshot_list(self):
        """List all snapshots via the cinder command line client"""
        _cmd = 'snapshot-list'
        _response_type = CinderResponses.SnapshotListResponse
        return self._process_command()

    def snapshot_show(self, snapshot_id):
        """Get details for a snapshot via the cinder command line client"""
        _cmd = 'snapshot-show'
        _response_type = CinderResponses.SnapshotResponse
        return self._process_command()

    def snapshot_delete(self, snapshot_id):
        """Delete a snapshot via the cinder command line client"""
        _cmd = 'snapshot-delete'
        return self._process_command()

# Volume Types
    def type_list(self):
        """Get a list of all volume types via the cinder command line client"""
        _cmd = 'type-list'
        _response_type = CinderResponses.VolumeTypeListResponse
        return self._process_command()
