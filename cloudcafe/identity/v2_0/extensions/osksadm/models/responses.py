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

from cloudcafe.identity.common.models.base import (
    BaseIdentityModel, BaseIdentityListModel)


class ServiceList(BaseIdentityListModel):
    @classmethod
    def _xml_ele_to_obj(cls, element):
        services = cls()
        if element.tag.lower() != "services":
            raise Exception("wrong element")
        for service in element.getchildren():
            services.append(Service._xml_ele_to_obj(service))
        return services

    @classmethod
    def _dict_to_obj(cls, data_dict):
        services = cls()
        for service in data_dict.get('OS-KSADM:services'):
            services.append(Service._dict_to_obj(service))
        return services


class Service(BaseIdentityModel):
    def __init__(self, description=None, type_=None, name=None, id_=None):
        self.description = description
        self.type_ = type_
        self.name = name
        self.id_ = id_

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element.tag.lower() != "service":
            raise Exception("wrong element")
        return cls(description=element.attrib.get('description'),
                   type_=element.attrib.get('type'),
                   name=element.attrib.get('name'),
                   id_=element.attrib.get('id'))

    @classmethod
    def _dict_to_obj(cls, data_dict):
        return cls(description=data_dict.get('description'),
                   type_=data_dict.get('type'),
                   name=data_dict.get('name'),
                   id_=data_dict.get('id'))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get('OS-KSADM:service'))
