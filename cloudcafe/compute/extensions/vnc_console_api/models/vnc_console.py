import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.constants import Constants


class VncConsole(AutoMarshallingModel):

    def __init__(self, type, url):
        self.type = type
        self.url = url

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get("console"))

    @classmethod
    def _dict_to_obj(cls, dict):
        return VncConsole(type=dict.get("type"),
                          url=dict.get("url"))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        return VncConsole(type=element.find("type").text,
                          url=element.find("url").text)
