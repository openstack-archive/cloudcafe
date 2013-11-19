from cloudcafe.openstackcli.common.client import BaseOpenstackPythonCLI_Client
from cloudcafe.openstackcli.cindercli.models import responses as \
    CinderResponses


class CinderCLI(BaseOpenstackPythonCLI_Client):

    _KWMAP = {
        'volume_service_name': 'volume-service-name',
        'os_volume_api_version': 'os-volume-api-version'}
    _KWMAP.update(BaseOpenstackPythonCLI_Client._KWMAP)

    _CMD = 'cinder'

    def _generate_cmd(self, flag, *values):
        return " --{0}{1}".format(
            flag, "".join([" {0}".format(v) for v in values]))

    def __init__(
            self, volume_service_name=None, os_volume_api_version=None,
            **kwargs):
        super(CinderCLI, self).__init__(**kwargs)
        self.volume_service_name = volume_service_name
        self.os_volume_api_version = os_volume_api_version
        #This is not ideal, but it's the only way that the current cinderclient
        #can support rackspace auth
        self.env_var_dict = {'CINDER_RAX_AUTH': '1'}
        self.set_environment_variables(self.env_var_dict)

    def create_volume(
            self, size, snapshot_id=None, source_volid=None, image_id=None,
            display_name=None, display_description=None, volume_type=None,
            availability_zone=None, metadata=None):

        metadata = self._dict_to_metadata_cmd_string(metadata)
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
        return self.send(CinderResponses.Volume)

    def list_volumes(self, display_name=None, status=None, all_tenants=False):
        _cmd = 'list'
        _kwmap = {
            'display_name': 'display-name',
            'status': 'status',
            'all_tenants': 'all-tenants'}
        all_tenants = 1 if all_tenants is True else 0
        return self.send(CinderResponses.VolumeList)

    def list_volume_types(self):
        _cmd = 'type-list'
        return self.send(CinderResponses.VolumeTypeList)
