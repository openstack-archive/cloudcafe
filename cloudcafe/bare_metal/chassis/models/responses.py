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

from cloudcafe.bare_metal.common.models.links import Link, Links


class Chassis(AutoMarshallingModel):

    def __init__(
            self, description=None, links=None, extra=None, created_at=None,
            updated_at=None, nodes=None, uuid=None):
        super(Chassis, self).__init__()
        self.description = description
        self.links = links
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at
        self.nodes = nodes
        self.uuid = uuid

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):

        links = None
        if 'links' in json_dict:
            links = Links._list_to_obj(json_dict.get(Links.RESOURCE_TYPE))
        nodes = None
        if 'nodes' in json_dict:
            nodes = Nodes._list_to_obj(json_dict.get(Nodes.RESOURCE_TYPE))

        return Chassis(
            description=json_dict.get('description'),
            links=links,
            extra=json_dict.get('extra'),
            created_at=json_dict.get('created_at'),
            updated_at=json_dict.get('updated_at'),
            nodes=nodes,
            uuid=json_dict.get('uuid'))


class ChassisList(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('chassis'))

    @classmethod
    def _list_to_obj(cls, chassis_dict_list):
        chassis_list = ChassisList()
        for chassis_dict in chassis_dict_list:
            chassis = Chassis._dict_to_obj(chassis_dict)
            chassis_list.append(chassis)
        return chassis_list


class Node(Link):
    RESOURCE_TYPE = 'node'


class Nodes(Links):
    RESOURCE_TYPE = 'nodes'
