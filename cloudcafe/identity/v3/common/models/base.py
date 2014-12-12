"""
Copyright 2014 Rackspace
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
from xml.etree import ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel


class BaseIdentity(object):
    """
    Base class for Identity
    """
    def __init__(self, kwargs):
        super(BaseIdentity, self).__init__()
        for var in kwargs:
            if var != "self" and not var.startswith("_"):
                setattr(self, var, kwargs.get(var))

    @classmethod
    def _remove_namespace(cls, element, XML_NS):
        return cls._remove_xml_etree_namespace(element, XML_NS)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        return cls._xml_ele_to_obj(
            cls._remove_identity_xml_namespaces(element))

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        return ET.tostring(element)


class BaseIdentityModel(BaseIdentity, AutoMarshallingModel):
    """
    Base class for Identity Model
    """

    @classmethod
    def _remove_prefix(cls, prefix, data_dict, delimiter=':'):
        for key in data_dict.keys():
            if key.startswith(prefix):
                new_key = key.split(delimiter)[1]
                data_dict[new_key] = data_dict[key]
                del data_dict[key]
        return data_dict


class BaseIdentityListModel(list, BaseIdentity, AutoMarshallingModel):
    def __str__(self):
        return list.__str__(self)


class EmptyModel(object):
    """
    Representation of an empty model
    """
    def _obj_to_dict(self):
        return None

    def _obj_to_xml_ele(self):
        return ET.Element(None)
