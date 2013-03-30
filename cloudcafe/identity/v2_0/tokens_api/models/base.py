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

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel

from cloudcafe.identity.v2_0.tokens_api.models.constants import V2_0Constants


class BaseIdentityModel(AutoMarshallingModel):

    @classmethod
    def _remove_identity_xml_namespaces(cls, element):
        cls._remove_namespace(element, V2_0Constants.XML_NS)
        cls._remove_namespace(element, V2_0Constants.XML_NS_OS_KSADM)
        cls._remove_namespace(element, V2_0Constants.XML_NS_RAX_KSKEY)
        cls._remove_namespace(element, V2_0Constants.XML_NS_OS_KSEC2)
        cls._remove_namespace(element, V2_0Constants.XML_NS_RAX_KSQA)
        cls._remove_namespace(element, V2_0Constants.XML_NS_RAX_AUTH)
        cls._remove_namespace(element, V2_0Constants.XML_NS_RAX_KSGRP)
        cls._remove_namespace(element, V2_0Constants.XML_NS_OPENSTACK_COMMON)
        cls._remove_namespace(element, V2_0Constants.XML_NS_ATOM)


class BaseIdentityListModel(AutoMarshallingListModel):

    @classmethod
    def _remove_identity_xml_namespaces(cls, element):
        BaseIdentityListModel._remove_identity_xml_namespaces(element)
