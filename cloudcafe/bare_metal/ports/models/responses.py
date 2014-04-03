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
from cloudcafe.bare_metal.common.models.metadata import Metadata


class Port(AutoMarshallingModel):

    def __init__(
            self, node_uuid=None, uuid=None, links=None, extra=None,
            created_at=None, updated_at=None, address=None):
        super(Port, self).__init__()
        self.node_uuid = node_uuid
        self.uuid = uuid
        self.links = links
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at
        self.address = address

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):

        links = None
        if 'links' in json_dict:
            links = Links._list_to_obj(json_dict.get('links'))

        extra = None
        if 'extra' in json_dict:
            extra = Metadata._dict_to_obj(json_dict.get('extra'))

        return Port(
            node_uuid=json_dict.get('node_uuid'),
            uuid=json_dict.get('uuid'),
            links=links,
            extra=extra,
            created_at=json_dict.get('created_at'),
            updated_at=json_dict.get('updated_at'),
            address=json_dict.get('address'))


class Ports(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('ports'))

    @classmethod
    def _list_to_obj(cls, port_dict_list):
        ports = Ports()
        for port_dict in port_dict_list:
            port = Port._dict_to_obj(port_dict)
            ports.append(port)
        return ports
