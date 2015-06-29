from cafe.engine.models.base import AutoMarshallingModel
import json


class StatusResetRequest(AutoMarshallingModel):
    def __init__(self, status=None):
        super(StatusResetRequest, self).__init__()
        self.status = status

    def _obj_to_json(self):
        data = {"os-reset_status": {"status": self.status}}
        return json.dumps(data)
