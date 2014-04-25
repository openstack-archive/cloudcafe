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

from cafe.engine.models.base import AutoMarshallingModel, \
    AutoMarshallingListModel

from cloudcafe.bare_metal.common.models.links import Links


class Driver(AutoMarshallingModel):

    def __init__(
            self, hosts=None, name=None, links=None):
        super(Driver, self).__init__()
        self.hosts = hosts
        self.name = name
        self.links = links

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):

        links = None
        if Links.RESOURCE_TYPE in json_dict:
            links = Links._list_to_obj(json_dict.get(Links.RESOURCE_TYPE))

        return Driver(
            hosts=json_dict.get('hosts'),
            name=json_dict.get('name'),
            links=links)


class Drivers(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('drivers'))

    @classmethod
    def _list_to_obj(cls, driver_dict_list):
        drivers = Drivers()
        for driver_dict in driver_dict_list:
            driver = Driver._dict_to_obj(driver_dict)
            drivers.append(driver)
        return drivers
