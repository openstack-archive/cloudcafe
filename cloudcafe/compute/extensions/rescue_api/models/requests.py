import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.constants import Constants


class RescueMode(AutoMarshallingModel):
    ROOT_TAG = 'rescue'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_RESCUE)
        xml += ET.tostring(element)
        return xml


class ExitRescueMode(AutoMarshallingModel):
    ROOT_TAG = 'unrescue'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_UNRESCUE)
        xml += ET.tostring(element)
        return xml