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
from cloudcafe.bare_metal.common.models.metadata import MetadataBase, Extra


class Node(AutoMarshallingModel):

    def __init__(
            self, instance_uuid=None, target_power_state=None,
            properties=None, maintenance=None, links=None, driver_info=None,
            extra=None, last_error=None, console_enabled=None,
            target_provision_state=None, driver=None, updated_at=None,
            ports=None, provision_updated_at=None, chassis_uuid=None,
            provision_state=None, reservation=None, power_state=None,
            created_at=None, uuid=None):
        super(Node, self).__init__()

        self.instance_uuid = instance_uuid
        self.target_power_state = target_power_state
        self.properties = properties
        self.maintenance = maintenance
        self.links = links
        self.driver_info = driver_info
        self.extra = extra
        self.last_error = last_error
        self.console_enabled = console_enabled
        self.target_provision_state = target_provision_state
        self.driver = driver
        self.updated_at = updated_at
        self.ports = ports
        self.provision_updated_at = provision_updated_at
        self.chassis_uuid = chassis_uuid
        self.provision_state = provision_state
        self.reservation = reservation
        self.power_state = power_state
        self.created_at = created_at
        self.uuid = uuid

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        properties = None
        if 'properties' in json_dict:
            properties = Properties._dict_to_obj(
                json_dict.get(Properties.METADATA_TYPE))

        driver_info = None
        if DriverInfo.METADATA_TYPE in json_dict:
            driver_info = DriverInfo._dict_to_obj(
                json_dict.get(DriverInfo.METADATA_TYPE))

        links = None
        if Links.RESOURCE_TYPE in json_dict:
            links = Links._list_to_obj(json_dict.get(Links.RESOURCE_TYPE))

        ports = None
        if Ports.RESOURCE_TYPE in json_dict:
            ports = Ports._list_to_obj(json_dict.get(Ports.RESOURCE_TYPE))

        extra = None
        if Extra.METADATA_TYPE in json_dict:
            extra = Extra._dict_to_obj(json_dict.get(Extra.METADATA_TYPE))

        node = Node(
            instance_uuid=json_dict.get('instance_uuid'),
            target_power_state=json_dict.get('target_power_state'),
            properties=properties,
            maintenance=json_dict.get('maintenance'),
            links=links,
            driver_info=driver_info,
            extra=extra,
            last_error=json_dict.get('last_error'),
            console_enabled=json_dict.get('console_enabled'),
            target_provision_state=json_dict.get('target_provision_state'),
            driver=json_dict.get('driver'),
            updated_at=json_dict.get('updated_at'),
            ports=ports,
            provision_updated_at=json_dict.get('provision_updated_at'),
            chassis_uuid=json_dict.get('chassis_uuid'),
            provision_state=json_dict.get('provision_state'),
            reservation=json_dict.get('reservation'),
            power_state=json_dict.get('power_state'),
            created_at=json_dict.get('created_at'),
            uuid=json_dict.get('uuid'))
        return node


class Nodes(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('nodes'))

    @classmethod
    def _list_to_obj(cls, node_dict_list):
        nodes = Nodes()
        for node_dict in node_dict_list:
            node = Node._dict_to_obj(node_dict)
            nodes.append(node)
        return nodes


class Port(Link):
    RESOURCE_TYPE = 'port'


class Ports(Links):
    RESOURCE_TYPE = 'ports'


class Properties(MetadataBase):
    METADATA_TYPE = 'properties'


class DriverInfo(MetadataBase):
    METADATA_TYPE = 'driver_info'


class DriverInterfaceResult(AutoMarshallingModel):

    def __init__(self, result=None, reason=None):
        self.result = result
        self.reason = reason

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return DriverInterfaceResult(
            result=json_dict.get('result'),
            reason=json_dict.get('reason'))


class DriverInterfaces(AutoMarshallingModel):

    def __init__(self, console=None, power=None, deploy=None):
        self.console = console
        self.power = power
        self.deploy = deploy

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        console = DriverInterfaceResult._dict_to_obj(json_dict.get('console'))
        power = DriverInterfaceResult._dict_to_obj(json_dict.get('power'))
        deploy = DriverInterfaceResult._dict_to_obj(json_dict.get('deploy'))
        return DriverInterfaces(console=console, power=power, deploy=deploy)
