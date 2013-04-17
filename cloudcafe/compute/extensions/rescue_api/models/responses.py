import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel


class RescueResponse(AutoMarshallingModel):


    def __init__(self, admin_pass):
        self.admin_pass = admin_pass

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return RescueResponse(json_dict.get('adminPass'))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplemented

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        raise NotImplemented