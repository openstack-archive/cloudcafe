import json
from cafe.engine.models.base import \
    AutoMarshallingDictModel, AutoMarshallingModel
from cloudcafe.blockstorage.volumes_api.common.models.automarshalling import \
    _VolumesAPIBaseModel, _VolumesAPIBaseListModel


class _LinksItem(_VolumesAPIBaseModel):
    kwarg_map = {
        "href": "href",
        "rel": "rel"}

    def __init__(self, href=None, rel=None):
        super(_LinksItem, self).__init__()
        self.href = href
        self.rel = rel


class _LinksList(_VolumesAPIBaseListModel):
    list_model_key = 'links'
    ObjectModel = _LinksItem


class QuotaUsageResponse(AutoMarshallingDictModel):
    """ This model represents the content of a dictionary of dictionaries.
    The key-names are arbitrary, and so no conversion to a namespace is
    attempted
    """

    @classmethod
    def _json_to_obj(cls, json_dict):
        quotaset = QuotaListResponse()

        data = json.loads(json_dict).get('quota_set')
        quotaset['id'] = data.get('id')
        for k, v in data.items():
            if type(v) == type(dict()):
                quotaset[k] = _QuotaUsageResponseItem(**v)

        return quotaset


class _QuotaUsageResponseItem(object):

    def __init__(self, in_use=None, limit=None, reserved=None):
        self.in_use = in_use
        self.limit = limit
        self.reserved = reserved


class QuotaListResponse(AutoMarshallingDictModel):
    """ This model represents the content of a dictionary of dictionaries.
    The key-names are arbitrary, and so no conversion to a namespace is
    attempted
    """

    @classmethod
    def _json_to_obj(cls, json_dict):
        return QuotaListResponse(**json.loads(json_dict).get('quota_set'))


class QuotaSet(AutoMarshallingModel):
    """ This model represents the content of a dictionary of dictionaries.
    The key-names are arbitrary, and so no conversion to a namespace is
    attempted
    """

    @classmethod
    def _json_to_obj(cls, json_dict):

        data = json.loads(json_dict).get('quota_set')
        theid = data.get('id')
        quotaset = cls()
        setattr(quotaset, 'id', theid)
        for k, v in data.items():
            setattr(quotaset, k, v)
        return quotaset


class VolumeTransferResponse(_VolumesAPIBaseModel):
    obj_model_key = 'transfer'
    kwarg_map = {
        "id_": "id",
        "created_at": "created_at",
        "name": "name",
        "volume_id": "volume_id",
        "auth_key": "auth_key",
        "links": "links"}

    def __init__(
            self, id_=None, created_at=None, name=None, volume_id=None,
            auth_key=None, links=None):

        super(VolumeTransferResponse, self).__init__()
        self.id_ = id_
        self.created_at = created_at
        self.name = name
        self.volume_id = volume_id
        self.auth_key = auth_key
        self.links = links

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume_transfer = cls._map_values_to_kwargs(json_dict)
        volume_transfer.links = _LinksList._json_dict_to_obj(
            volume_transfer.links)
        return volume_transfer


class _VolumeTransfersListResponseItem(_VolumesAPIBaseModel):
    kwarg_map = {
        "id_": "id",
        "name": "name",
        "volume_id": "volume_id",
        "links": "links"}

    def __init__(
            self, id_=None, name=None, volume_id=None, links=None):

        super(_VolumeTransfersListResponseItem, self).__init__()
        self.id_ = id_
        self.name = name
        self.volume_id = volume_id
        self.links = links

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume_transfer = cls._map_values_to_kwargs(json_dict)
        volume_transfer.links = _LinksList._json_dict_to_obj(
            volume_transfer.links)
        return volume_transfer


class VolumeTransfersListResponse(_VolumesAPIBaseListModel):
    list_model_key = 'transfers'
    ObjectModel = _VolumeTransfersListResponseItem


class _VolumeTransfersListDetailedResponseItem(_VolumesAPIBaseModel):
    kwarg_map = {
        "id_": "id",
        "created_at": "created_at",
        "name": "name",
        "volume_id": "volume_id",
        "links": "links"}

    def __init__(
            self, id_=None, created_at=None, name=None, volume_id=None,
            links=None):

        super(_VolumeTransfersListDetailedResponseItem, self).__init__()
        self.id_ = id_
        self.created_at = created_at
        self.name = name
        self.volume_id = volume_id
        self.links = links

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume_transfer = cls._map_values_to_kwargs(json_dict)
        volume_transfer.links = _LinksList._json_dict_to_obj(
            volume_transfer.links)
        return volume_transfer


class VolumeTransfersListDetailedResponse(_VolumesAPIBaseListModel):
    list_model_key = 'transfers'
    ObjectModel = _VolumeTransfersListDetailedResponseItem


class VolumeTransferDetailedResponse(_VolumesAPIBaseModel):
    kwarg_map = {
        "id_": "id",
        "created_at": "created_at",
        "name": "name",
        "volume_id": "volume_id",
        "links": "links"}

    def __init__(
            self, id_=None, created_at=None, name=None, volume_id=None,
            links=None):

        super(VolumeTransferDetailedResponse, self).__init__()
        self.id_ = id_
        self.created_at = created_at
        self.name = name
        self.volume_id = volume_id
        self.links = links

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume_transfer = cls._map_values_to_kwargs(json_dict)
        volume_transfer.links = _LinksList._json_dict_to_obj(
            volume_transfer.links)
        return volume_transfer


class VolumeTransferAcceptResponse(_VolumesAPIBaseModel):
    kwarg_map = {
        "id_": "id",
        "name": "name",
        "volume_id": "volume_id",
        "links": "links"}

    def __init__(
            self, id_=None, name=None, volume_id=None, links=None):

        super(VolumeTransferAcceptResponse, self).__init__()
        self.id_ = id_
        self.name = name
        self.volume_id = volume_id
        self.links = links

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume_transfer = cls._map_values_to_kwargs(json_dict)
        volume_transfer.links = _LinksList._json_dict_to_obj(
            volume_transfer.links)
        return volume_transfer
