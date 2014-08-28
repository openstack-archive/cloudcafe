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


class FloatingIP(AutoMarshallingModel):

    def __init__(self, instance_id=None, ip=None, fixed_ip=None,
                 id_=None, pool=None):
        self.instance_id = instance_id
        self.ip = ip
        self.fixed_ip = fixed_ip
        self.id_ = id_
        self.pool = pool

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('floating_ip'))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        floating_ip = FloatingIP(
            instance_id=json_dict.get('instance_id'),
            ip=json_dict.get('ip'),
            fixed_ip=json_dict.get('fixed_ip'),
            id_=json_dict.get('id'),
            pool=json_dict.get('pool'))
        return floating_ip


class FloatingIPs(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('floating_ips'))

    @classmethod
    def _list_to_obj(cls, ips_dict_list):
        floating_ips = FloatingIPs()
        for ip_dict in ips_dict_list:
            ip = FloatingIP._dict_to_obj(ip_dict)
            floating_ips.append(ip)
        return floating_ips
