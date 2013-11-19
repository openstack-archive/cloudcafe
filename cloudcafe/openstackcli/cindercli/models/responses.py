from cafe.engine.models.base import BaseModel
from cloudcafe.openstackcli.common.models.responses import \
    BasePrettyTableResponseModel, BasePrettyTableResponseListModel


class VolumeResponse(BasePrettyTableResponseModel):
    def __init__(
            self, id_=None, display_name=None, size=None, volume_type=None,
            display_description=None, metadata=None, availability_zone=None,
            snapshot_id=None, attachments=None, created_at=None, status=None):

        self.id_ = id_
        self.display_name = display_name
        self.size = size
        self.volume_type = volume_type
        self.display_description = display_description
        self.metadata = metadata
        self.availability_zone = availability_zone
        self.snapshot_id = snapshot_id
        self.attachments = attachments
        self.created_at = created_at
        self.status = status

    @classmethod
    def _prettytable_str_to_obj(cls, prettytable_string):
        datatuple = cls._load_prettytable_string(prettytable_string)
        volume_dict = {}
        for datadict in datatuple:
            volume_dict[datadict['Property']] = datadict['Value']
        kwargs = {
            'id_': volume_dict.get('id'),
            'display_name': volume_dict.get('display_name'),
            'size': volume_dict.get('size'),
            'volume_type': volume_dict.get('volume_type'),
            'display_description': volume_dict.get('display_description'),
            'metadata': volume_dict.get('metadata'),
            'availability_zone': volume_dict.get('availability_zone'),
            'snapshot_id': volume_dict.get('snapshot_id'),
            'attachments': volume_dict.get('attachments'),
            'created_at': volume_dict.get('created_at'),
            'status': volume_dict.get('status')}
        return VolumeResponse(**kwargs)


class _VolumeListItem(BaseModel):
    def __init__(
            self, id_=None,  display_name=None, size=None, volume_type=None,
            attached_to=None, status=None, bootable=None):

        self.id_ = id_
        self.display_name = display_name
        self.size = size
        self.volume_type = volume_type
        self.attached_to = attached_to
        self.status = status
        self.bootable = bootable


class VolumeListResponse(BasePrettyTableResponseListModel):

    @classmethod
    def _prettytable_str_to_obj(cls, prettytable_string):
        volume_list = VolumeListResponse()
        datatuple = cls._load_prettytable_string(prettytable_string)
        for datadict in datatuple:
            kwargs = {
                'status': datadict.get('Status'),
                'id_': datadict.get('ID'),
                'display_name': datadict.get('Display Name'),
                'size': datadict.get('Size'),
                'volume_type': datadict.get('Volume Type'),
                'bootable': datadict.get('Bootable'),
                'attached_to': datadict.get('Attached to')}
            volume_list.append(_VolumeListItem(**kwargs))
        return volume_list


class _VolumeTypeListItem(BaseModel):
    def __init__(
            self, id_=None,  name=None):
        self.id_ = id_
        self.name = name


class VolumeTypeListResponse(BasePrettyTableResponseListModel):

    @classmethod
    def _prettytable_str_to_obj(cls, prettytable_string):
        volume_type_list = VolumeTypeListResponse()
        datatuple = cls._load_prettytable_string(prettytable_string)
        for datadict in datatuple:
            kwargs = {
                'id_': datadict.get('ID'),
                'name': datadict.get('Name')}
            volume_type_list.append(_VolumeTypeListItem(**kwargs))
        return volume_type_list
