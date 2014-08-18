# Used by models that inherit from an *Extensible* model
from ast import literal_eval
from cloudcafe.openstackcli.novacli.models.extensions import extensions

from cloudcafe.openstackcli.common.models.responses import (
    SimplePrettyTableList, SimplePrettyTableListItem,
    KeyValuePrettyTableWithHeaders)


class ServerResponse(KeyValuePrettyTableWithHeaders):
    _attr_map = {
        'access_ipv4': 'accessIPv4',
        'access_ipv6': 'accessIPv6',
        'admin_pass': 'adminPass',
        'config_drive': 'config_drive',
        'created': 'created',
        'flavor': 'flavor',
        'host_id': 'hostId',
        'id_': 'id',
        'image': 'image',
        'key_name': 'key_name',
        'metadata': 'metadata',
        'name': 'name',
        'progress': 'progress',
        'status': 'status',
        'tenant_id': 'tenant_id',
        'updated': 'updated',
        'user_id': 'user_id'}

    def _postprocess(self):
        self.metadata = literal_eval(self.metadata)


class _ServerListItem(SimplePrettyTableListItem):
    _attrs = ['id_', 'name', 'status', 'networks']


class ServerListResponse(SimplePrettyTableList):
    _list_item_class = _ServerListItem
    _header_map = {
        'id_': 'ID',
        'name': 'Name',
        'status': 'Status',
        'networks': 'Networks'}


class _ImageListItem(SimplePrettyTableListItem):
    _attrs = ['id_', 'name', 'status', 'server']


class ImageListResponse(SimplePrettyTableList):
    _list_item_class = _ImageListItem
    _header_map = {
        'id_': 'ID',
        'name': 'Name',
        'status': 'Status',
        'server': 'Server'}


class ImageShowResponse(KeyValuePrettyTableWithHeaders):
    _attr_map = {
        'created': 'created',
        'id_': 'id',
        'min_disk': 'minDisk',
        'min_ram': 'minRam',
        'name': 'name',
        'progress': 'progress',
        'server': 'server',
        'status': 'status',
        'updated': 'updated'}


class _FlavorListItem(SimplePrettyTableListItem):
    _attrs = [
        'id_', 'name', 'memory_mb', 'disk', 'ephemeral', 'swap', 'vcpus',
        'rxtx_factor', 'is_public']


class FlavorListResponse(SimplePrettyTableList):
    _list_item_class = _FlavorListItem
    _header_map = {
        'id_': 'ID',
        'name': 'Name',
        'memory_mb': 'Memory_MB',
        'disk': 'Disk',
        'ephemeral': 'Ephemeral',
        'swap': 'Swap',
        'vcpus': 'VCPUs',
        'rxtx_factor': 'RXTX_Factor',
        'is_public': 'Is_Public'}


class FlavorShowResponse(KeyValuePrettyTableWithHeaders):
    _attr_map = {
        'disk': 'disk',
        'extra_specs': 'extra_specs',
        'id_': 'id',
        'name': 'name',
        'ram': 'ram',
        'rxtx_factor': 'rxtx_factor',
        'swap': 'swap',
        'vcpus': 'vcpus'}


class VolumeAttachResponse(KeyValuePrettyTableWithHeaders):
    _attr_map = {
        'device': 'device',
        'id_': 'id',
        'server_id': 'serverId',
        'volume_id': 'volumeId'}


class VolumeCreateResponse(KeyValuePrettyTableWithHeaders):
    _attr_map = {
        'attachments': 'attachments',
        'availability_zone': 'availability_zone',
        'bootable': 'bootable',
        'created_at': 'created_at',
        'display_description': 'display_description',
        'id_': 'id',
        'metadata': 'metadata',
        'size': 'size',
        'snapshot_id': 'snapshot_id',
        'source_volid': 'source_volid',
        'status': 'status',
        'volume_type': 'volume_type'}

    def _postprocess(self):
        self.metadata = literal_eval(self.metadata)


class _VolumeListItem(SimplePrettyTableListItem):
    _attrs = ['id_', 'display_name', 'status', 'volume_type', 'attached_to']


class VolumeListResponse(SimplePrettyTableList):
    _list_item_class = _VolumeListItem
    _header_map = {
        'id_': 'ID',
        'display_name': 'Display Name',
        'status': 'Status',
        'volume_type': 'Volume Type',
        'attached_to': 'Attached to'}


class VolumeSnapshotCreateResponse(KeyValuePrettyTableWithHeaders):
    _attr_map = {
        'created_at': 'created_at',
        'display_description': 'display_description',
        'display_name': 'display_name',
        'id_': 'id',
        'metadata': 'metadata',
        'size': 'size',
        'status': 'status',
        'volume_id': 'volume_id'}


class VolumeSnapshotShowResponse(VolumeSnapshotCreateResponse):
    """ This model is empty because it has extensions that apply only
    to this snapshot show response.  Otherwise, it is identical to the
    snapshot create response"""
    pass


class _VolumeSnapshotListItem(SimplePrettyTableListItem):
    _attrs = ['id_', 'volume_id', 'status', 'display_name', 'size']


class VolumeSnapshotListResponse(SimplePrettyTableList):
    _list_item_class = _VolumeSnapshotListItem
    _header_map = {
        'id_': 'ID',
        'volume_id': 'Volume ID',
        'status': 'Status',
        'display_name': 'Display Name',
        'size': 'Size'}


class VolumeTypeCreateResponse(SimplePrettyTableList):
    _attr_map = {
        'id_': 'ID',
        'name': 'Name'}


class _VolumeTypeListItem(SimplePrettyTableListItem):
    _attrs = ['id_', 'name']


class VolumeTypeListResponse(SimplePrettyTableList):
    _header_map = {
        'id_': 'ID',
        'name': 'Name'}
