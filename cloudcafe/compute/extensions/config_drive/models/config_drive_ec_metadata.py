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

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.extensions.config_drive.models.\
    config_drive_openstack_meta import Keys


class EcMetadata(AutoMarshallingModel):
    """Elastic Cloud Metadata supported by config drive"""
    def __init__(self, ami_id=None, ami_launch_index=None,
                 ami_manifest_path=None, block_device_mapping=None,
                 hostname=None, instance_action=None, instance_id=None,
                 instance_type=None, kernel_id=None, local_hostname=None,
                 local_ipv4=None, placement=None, public_hostname=None,
                 public_ipv4=None, public_keys=None, ramdisk_id=None,
                 reservation_id=None, security_groups=None):
        self.ami_id = ami_id
        self.ami_launch_index = ami_launch_index
        self.ami_manifest_path = ami_manifest_path
        self.block_device_mapping = block_device_mapping
        self.hostname = hostname
        self.instance_action = instance_action
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.kernel_id = kernel_id
        self.local_hostname = local_hostname
        self.local_ipv4 = local_ipv4
        self.placement = placement
        self.public_hostname = public_hostname
        self.public_ipv4 = public_ipv4
        self.public_keys = public_keys
        self.ramdisk_id = ramdisk_id
        self.reservation_id = reservation_id
        self.security_groups = security_groups

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ec_meta = cls._dict_to_obj(json_dict)
        return ec_meta

    @classmethod
    def _dict_to_obj(cls, json_dict):
        ec_meta = EcMetadata(
            ami_id=json_dict.get('ami-id'),
            ami_launch_index=json_dict.get('ami-launch-index'),
            ami_manifest_path=json_dict.get('ami-manifest-path'),
            hostname=json_dict.get('hostname'),
            instance_action=json_dict.get('instance-action'),
            instance_id=json_dict.get('instance-id'),
            instance_type=json_dict.get('instance-type'),
            kernel_id=json_dict.get('kernel-id'),
            local_hostname=json_dict.get('local-hostname'),
            local_ipv4=json_dict.get('local-ipv4'),
            placement=json_dict.get('placement'),
            public_hostname=json_dict.get('public-hostname'),
            public_ipv4=json_dict.get('public-ipv4'),
            ramdisk_id=json_dict.get('ramdisk-id'),
            reservation_id=json_dict.get('reservation-id'),
            security_groups=json_dict.get('security-groups'))
        if 'block-device-mapping' in json_dict:
            ec_meta.block_device_mapping = \
                BlockDeviceMapping._dict_to_obj(
                    json_dict.get('block-device-mapping'))
        if 'public-keys' in json_dict:
            ec_meta.public_keys = Keys._dict_to_obj(json_dict)
        return ec_meta


class BlockDeviceMapping(AutoMarshallingModel):

    def __init__(self, ami, root, ephemeral=None, swap=None):

        super(BlockDeviceMapping, self).__init__()
        self.ami = ami
        self.root = root
        self.ephemeral = ephemeral
        self.swap = swap

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Return an instance of a Device Mapping based on the json serialized_str
        passed in.
        """
        json_dict = json.loads(serialized_str)
        block_mapping = cls._dict_to_obj(json_dict)
        return block_mapping

    @classmethod
    def _dict_to_obj(cls, file_dict):
        """Helper method to turn dictionary into Device Mapping instance."""
        bdm = BlockDeviceMapping(ami=file_dict.get('ami'),
                                 root=file_dict.get('root'),
                                 ephemeral=file_dict.get('ephemeral'),
                                 swap=file_dict.get('swap'))
        return bdm
