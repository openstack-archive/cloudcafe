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

from json import loads as str_to_json
from cafe.engine.models.base import AutoMarshallingModel


class RouteTarget(AutoMarshallingModel):

    def __init__(self, worker_id, ip_address_v4, ip_address_v6, status):
        super(RouteTarget, self).__init__()

        self.worker_id = worker_id
        self.ip_address_v4 = ip_address_v4
        self.ip_address_v6 = ip_address_v6
        self.status = status

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return RouteTarget(**json_dict)


class Route(AutoMarshallingModel):

    def __init__(self, service_domain, targets):
        super(Route, self).__init__()

        self.service_domain = service_domain
        self.targets = targets

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        domain = json_dict.get('service_domain')
        targets_dict = json_dict.get('targets')
        targets = [RouteTarget._dict_to_obj(child) for child in targets_dict]
        return Route(service_domain=domain, targets=targets)


class AllRoutes(AutoMarshallingModel):
    ROOT_TAG = 'routes'

    def __init__(self, routes=None):
        super(AllRoutes, self).__init__()
        self.routes = routes

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        routes = [Route._dict_to_obj(child) for child in json_dict]
        return AllRoutes(routes=routes)
