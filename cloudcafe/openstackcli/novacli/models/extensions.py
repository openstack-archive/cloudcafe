from cloudcafe.openstackcli.common.models.extensions import (
    ResponseExtensionType, SimpleResponseExtension,
    AttributeAggregatingResponseExtension)

# Extensions defined here are registered in this list
extensions = []


class OS_DCF_show(SimpleResponseExtension):
    __extends__ = ['ServerResponse', 'ImageShowResponse']
    _sub_attr_map = {'OS-DCF:diskConfig': 'os_dcf_disk_config'}


class ConfigDrive(SimpleResponseExtension):
    __extends__ = ['ServerResponse']
    _sub_attr_map = {'config_drive': 'config_drive'}


class OS_EXT_STS_show(SimpleResponseExtension):
    __extends__ = ['ServerResponse']
    _prefix = 'OS-EXT-STS'
    _sub_attr_map = {
        'OS-EXT-STS:power_state': 'os_ext_sts_power_state',
        'OS-EXT-STS:task_state': 'os_ext_sts_task_state',
        'OS-EXT-STS:vm_state': 'os_ext_sts_vm_state'}


class OS_EXT_IMG_SIZE(SimpleResponseExtension):
    __extends__ = ['ImageShowResponse']
    _prefix = 'OS_EXT_IMG_SIZE'
    _sub_attr_map = {'OS-EXT-STS:size': 'os_ext_img_size'}


class OS_EXT_STS_list(SimpleResponseExtension):
    __extends__ = ['_ServerListItem']
    _sub_attr_map = {
        'Power State': 'power_state',
        'Task State': 'task_state'}


class OS_FLV_EXT_DATA(SimpleResponseExtension):
    __extends__ = ['FlavorShowResponse']
    _sub_attr_map = {
        'OS-FLV-EXT-DATA:ephemeral': 'os_flv_ext_data_ephemeral'}


class OS_FLV_WITH_EXT_SPECS(SimpleResponseExtension):
    __extends__ = ['FlavorShowResponse']
    _sub_attr_map = {
        'OS-FLV-WITH-EXT-SPECS:extra_specs':
        'os_flv_with_ext_specs_extra_specs'}


class os_vol_mig_status_attr(SimpleResponseExtension):
    __extends__ = ['VolumeCreateResponse']
    _prefix = 'os-vol-mig-status-attr'
    _sub_attr_map = {
        'os-vol-mig-status-attr:migstat': 'os_vol_mig_status_attr_migstat',
        'os-vol-mig-status-attr:name_id': 'os_vol_mig_status_attr_name_id'}


class os_vol_tenant_attr(SimpleResponseExtension):
    __extends__ = ['VolumeCreateResponse']
    _sub_attr_map = {
        'os-vol-tenant-attr:tenant_id': 'os_vol_tenant_attr_tenant_id'}


class os_extended_snapshot_attributes(SimpleResponseExtension):
    __extends__ = ['VolumeSnapshotShowResponse']
    _prefix = 'os-extended-snapshot-attributes'
    _sub_attr_map = {
        'os-extended-snapshot-attributes:progress':
        'os_extended_snapshot_attributes_progress',

        'os-extended-snapshot-attributes:project_id':
        'os_extended_snapshot_attributes_project_id'}


class image_show_metadata_aggregator(AttributeAggregatingResponseExtension):
    __extends__ = ["ImageShowResponse"]
    _prefix = "metadata "  # The space after metadata is intentional
    _new_dict_attribute_name = "metadata"
