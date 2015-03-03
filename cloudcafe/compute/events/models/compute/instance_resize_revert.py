"""
Copyright 2015 Rackspace

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

from cloudcafe.compute.events.models.base import EventBaseModel


BASE_KWARG_MAP = {
    'access_ip_v4': 'access_ip_v4',
    'access_ip_v6': 'access_ip_v6',
    'architecture': 'architecture',
    'availability_zone': 'availability_zone',
    'cell_name': 'cell_name',
    'created_at': 'created_at',
    'deleted_at': 'deleted_at',
    'disk_gb': 'disk_gb',
    'display_name': 'display_name',
    'ephemeral_gb': 'ephemeral_gb',
    'host': 'host',
    'hostname': 'hostname',
    'image_meta': 'image_meta',
    'image_ref_url': 'image_ref_url',
    'instance_flavor_id': 'instance_flavor_id',
    'instance_id': 'instance_id',
    'instance_type': 'instance_type',
    'instance_type_id': 'instance_type_id',
    'kernel_id': 'kernel_id',
    'launched_at': 'launched_at',
    'memory_mb': 'memory_mb',
    'metadata': 'metadata',
    'node': 'node',
    'os_type': 'os_type',
    'progress': 'progress',
    'ramdisk_id': 'ramdisk_id',
    'reservation_id': 'reservation_id',
    'root_gb': 'root_gb',
    'state': 'state',
    'state_description': 'state_description',
    'tenant_id': 'tenant_id',
    'terminated_at': 'terminated_at',
    'user_id': 'user_id',
    'vcpus': 'vcpus'}


class InstanceResizeRevertStart(EventBaseModel):
    """Compute Instance Resize Revert Start Response Model

    @summary: Response model for a compute.instance.resize.revert.start
        event notification
    @note: Represents a single event notification

    JSON Example:
        {
            "access_ip_v4": "10.10.0.0",
            "access_ip_v6": null,
            "architecture": "x64",
            "availability_zone": null,
            "cell_name": "cell name",
            "created_at": "2015-01-15 18:59:29",
            "deleted_at": "",
            "disk_gb": 20,
            "display_name": "server123456",
            "ephemeral_gb": 0,
            "fixed_ips": { <FixedIps> },
            "host": null,
            "hostname": "server123456",
            "image_meta": { <ImageMeta> },
            "image_ref_url": "http://127.0.0.1/images/my_image",
            "instance_flavor_id": "instance_flavor_id",
            "instance_id": "performance1-1",
            "instance_type": "1 GB Performance",
            "instance_type_id": "9",
            "kernel_id": "",
            "launched_at": "",
            "memory_mb": 1024,
            "metadata": {},
            "node": null,
            "os_type": "linux",
            "progress": "",
            "ramdisk_id": "",
            "reservation_id": "r-abcdefg",
            "root_gb": 20,
            "state": "building",
            "state_description": "",
            "tenant_id": "123456",
            "terminated_at": "",
            "user_id": "123456789",
            "vcpus": 1
        }
    """
    kwarg_map = {}
    kwarg_map.update(BASE_KWARG_MAP)

    def __init__(self, access_ip_v4, access_ip_v6, architecture,
                 availability_zone, cell_name, created_at, deleted_at,
                 disk_gb, display_name, ephemeral_gb, host, hostname,
                 image_meta, image_ref_url, instance_flavor_id, instance_id,
                 instance_type, instance_type_id, kernel_id, launched_at,
                 memory_mb, metadata, node, os_type, progress, ramdisk_id,
                 reservation_id, root_gb, state, state_description, tenant_id,
                 terminated_at, user_id, vcpus):
        super(InstanceResizeRevertStart, self).__init__(locals())


class InstanceResizeRevertEnd(EventBaseModel):
    """Compute Instance Resize Revert End Response Model

    @summary: Response model for a compute.instance.resize.revert.end
        event notification
    @note: Represents a single event notification

    JSON Example:
        {
            "access_ip_v4": "10.10.0.0",
            "access_ip_v6": null,
            "architecture": "x64",
            "availability_zone": null,
            "cell_name": "cell name",
            "created_at": "2015-01-15 18:59:29",
            "deleted_at": "",
            "disk_gb": 20,
            "display_name": "server123456",
            "ephemeral_gb": 0,
            "fixed_ips": { <FixedIps> },
            "host": null,
            "hostname": "server123456",
            "image_meta": { <ImageMeta> },
            "image_ref_url": "http://127.0.0.1/images/my_image",
            "instance_flavor_id": "instance_flavor_id",
            "instance_id": "performance1-1",
            "instance_type": "1 GB Performance",
            "instance_type_id": "9",
            "kernel_id": "",
            "launched_at": "",
            "memory_mb": 1024,
            "metadata": {},
            "node": null,
            "os_type": "linux",
            "progress": "",
            "ramdisk_id": "",
            "reservation_id": "r-abcdefg",
            "root_gb": 20,
            "state": "building",
            "state_description": "",
            "tenant_id": "123456",
            "terminated_at": "",
            "user_id": "123456789",
            "vcpus": 1
        }
    """
    kwarg_map = {}
    kwarg_map.update(BASE_KWARG_MAP)

    def __init__(self, access_ip_v4, access_ip_v6, architecture,
                 availability_zone, cell_name, created_at, deleted_at,
                 disk_gb, display_name, ephemeral_gb, host, hostname,
                 image_meta, image_ref_url, instance_flavor_id, instance_id,
                 instance_type, instance_type_id, kernel_id, launched_at,
                 memory_mb, metadata, node, os_type, progress, ramdisk_id,
                 reservation_id, root_gb, state, state_description, tenant_id,
                 terminated_at, user_id, vcpus):
        super(InstanceResizeRevertEnd, self).__init__(locals())
