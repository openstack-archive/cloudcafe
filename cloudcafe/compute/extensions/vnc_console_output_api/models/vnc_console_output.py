import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.constants import Constants


class VncConsoleOutput(AutoMarshallingModel):

    def __init__(self, output):
        self.output = output

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return VncConsoleOutput(output=json_dict.get("output"))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        return VncConsoleOutput(output=element.text)
