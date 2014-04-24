"""
Copyright 2013 Rackspace

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
from xml.etree import ElementTree

from cafe.engine.models.base import (AutoMarshallingModel,
                                     AutoMarshallingListModel)

from cloudcafe.identity.v2_0.common.models.constants import V2_0Constants


class BaseIdentity(object):
    @classmethod
    def _remove_identity_xml_namespaces(cls, element):
        ns_list = [key for key in V2_0Constants.__dict__ if "__" not in key]
        for ns in ns_list:
            element = cls._remove_namespace(
                element, getattr(V2_0Constants, ns))
        return element

    @classmethod
    def _remove_namespace(cls, element, XML_NS):
        return cls._remove_xml_etree_namespace(element, XML_NS)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(
            cls._remove_identity_xml_namespaces(element))

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        return ElementTree.tostring(element)


class BaseIdentityModel(BaseIdentity, AutoMarshallingModel):
    pass


class BaseIdentityListModel(BaseIdentity, AutoMarshallingListModel):
    pass
