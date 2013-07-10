import json

from cafe.engine.models.base import AutoMarshallingModel


class GetConsole(AutoMarshallingModel):

    def __init__(self, vnc_type=None, tenant_id=None):

        super(GetConsole, self).__init__()
        self.vnc_type = vnc_type
        self.tenant_id = tenant_id

    def _obj_to_json(self):
        ret = {'os-getVNCConsole': self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        ret['type'] = self.vnc_type
        ret['tenant_id'] = self.tenant_id
        self._remove_empty_values(ret)
        return ret


class VncConsole(AutoMarshallingModel):

    def __init__(self, vnc_type=None, url=None):
        super(VncConsole, self).__init__()
        self.type = vnc_type
        self.url = url

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        console_dict = json_dict.get('console')
        console = VncConsole(vnc_type=console_dict.get('type'),
                             url=console_dict.get('url'))
        return console
