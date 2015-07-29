import json
from cafe.engine.models.base import \
    AutoMarshallingDictModel, AutoMarshallingModel


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
