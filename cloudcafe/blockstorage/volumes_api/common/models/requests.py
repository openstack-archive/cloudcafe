from cafe.engine.models.base import AutoMarshallingModel
import json


class StatusResetRequest(AutoMarshallingModel):
    def __init__(self, status=None):
        super(StatusResetRequest, self).__init__()
        self.status = status

    def _obj_to_json(self):
        data = {"os-reset_status": {"status": self.status}}
        return json.dumps(data)


class VolumeTransferRequest(AutoMarshallingModel):
    def __init__(self, volume_id=None, name=None):
        super(VolumeTransferRequest, self).__init__()
        self.volume_id = volume_id
        self.name = name

    def _obj_to_json(self):
        volume_attrs = {
            "volume_id": self.volume_id,
            "name": self.name}

        return json.dumps(
            {'transfer': self._remove_empty_values(volume_attrs)})
