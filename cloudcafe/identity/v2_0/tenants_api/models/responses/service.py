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
from cloudcafe.identity.v2_0.common.models.base import BaseIdentityListModel, \
    BaseIdentityModel
from cloudcafe.identity.v2_0.common.models.constants import AdminExtensions

_admin_extensions = AdminExtensions.OS_KS_ADM


class Services(BaseIdentityListModel):
    def __init__(self, services=None):
        """ An object that represents a services response object. """
        super(Services, self).__init__()
        self.extend(services or [])

    @classmethod
    def _list_to_obj(cls, service_dict_list):
        services = Services()
        for service_dict in service_dict_list:
            service = Service._dict_to_obj(service_dict)
            services.append(service)

        return services

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        admin_services = '{0}:services'.format(_admin_extensions)
        service_dict_list = json_dict.get(admin_services)

        return cls._list_to_obj(service_dict_list)


class Service(BaseIdentityModel):
    def __init__(self, id_=None, name=None, type_=None, description=None):
        """ An object that represents a service response object. """
        super(Service, self).__init__()
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.description = description

    def _obj_to_json(self):
        admin_service = '{0}:service'.format(_admin_extensions)
        json_dict = {admin_service: {"name": self.name,
                                     "type": self.type_,
                                     "description": self.description}}

        return json.dumps(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        service = Service(name=json_dict.get("name"),
                          type_=json_dict.get("type"),
                          description=json_dict.get("description"))

        return service

    @classmethod
    def _json_to_obj(cls, serialized_str):
        admin_service = '{0}:service'.format(_admin_extensions)
        json_dict = json.loads(serialized_str)

        return cls._dict_to_obj(json_dict.get(admin_service))
