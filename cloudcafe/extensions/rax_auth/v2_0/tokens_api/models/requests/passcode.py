import json
import xml.etree.ElementTree as ET
from cloudcafe.identity.v2_0.common.models.base import BaseIdentityModel
from cloudcafe.identity.v2_0.common.models.constants import V2_0Constants


class PasscodeCredentials(BaseIdentityModel):
    PREFIX = 'RAX-AUTH:'
    ROOT_TAG = 'passcodeCredentials'
    PASSCODE_KEY = 'passcode'
    RAW_NAME = '{0}{1}'.format(PREFIX, ROOT_TAG)

    rax_auth_xmlns = V2_0Constants.XML_NS_RAX_AUTH

    def __init__(self, passcode=''):
        super(PasscodeCredentials, self).__init__()
        self.passcode = '' if passcode is None else str(passcode)

    def _obj_to_dict(self, remove_root=True):
        attrs = {self.PASSCODE_KEY: self.passcode}
        return attrs if remove_root else {self.RAW_NAME: attrs}

    def _obj_to_xml_ele(self):
        element = ET.Element(
            "{{{0}}}{1}".format(self.rax_auth_xmlns, self.ROOT_TAG))
        return self._set_xml_etree_element(element,
                                           {self.PASSCODE_KEY: self.passcode})

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element is None:
            return None
        return cls(passcode=element.attrib.get(cls.PASSCODE_KEY))

    @classmethod
    def _dict_to_obj(cls, data):
        if data is None:
            return None
        return cls(passcode=data.get(cls.PASSCODE_KEY))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._dict_to_obj(data.get(cls.PREFIX + cls.ROOT_TAG))
