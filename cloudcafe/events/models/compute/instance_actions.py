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

from cloudcafe.events.models.base import EventBaseModel


BASE_KWARG_MAP = {
    'tenant_id': 'tenant_id',
    'user_id': 'user_id',
    'instance_id': 'instance_id',
    'instance_type': 'instance_type',
    'instance_type_id': 'instance_type_id',
    'display_name': 'display_name',
    'created_at': 'created_at',
    'launched_at': 'launched_at',
    'image_ref_url': 'image_ref_url',
    'state': 'state',
    'state_description': 'state_description',
    'fixed_ips': 'fixed_ips',
    'memory_mb': 'memory_mb',
    'disk_gb': 'disk_gb'}


class ComputeInstanceCreate(EventBaseModel):
    """Compute Instance Create Response Model

    @summary: Response model for a compute.instance.create.*
        event notification
    @note: Represents a single event notification

    JSON Example:
        {
            "tenant_id": "123456",
            "user_id": "some_user",
            "instance_id": "some_uuid",
            "instance_type": "flavor name",
            "instance_type_id": "flavor id",
            "display_name": "a display name",
            "created_at": "2015-01-09 21:26:54",
            "launched_at": "2015-01-09 21:27:54",
            "image_ref_url": "url.example",
            "state": "active",
            "state_description": "state description",
            "fixed_ips": [<FixedIps>],
            "memory_mb": 1024,
            "disk_gb": 20,
            "message": "descriptive message"
        }
    """
    kwarg_map = BASE_KWARG_MAP.copy()
    kwarg_map['message'] = 'message'

    def __init__(self, tenant_id, user_id, instance_id, instance_type,
                 instance_type_id, display_name, created_at, launched_at,
                 image_ref_url, state, state_description, fixed_ips,
                 memory_mb, disk_gb, message):
        super(ComputeInstanceCreate, self).__init__(locals())


class ComputeInstanceDelete(EventBaseModel):
    """Compute Instance Delete Response Model

    @summary: Response model for a compute.instance.delete.*
        event notification
    @note: Represents a single event notification

    JSON Example:
        {
            "tenant_id": "123456",
            "user_id": "some_user",
            "instance_id": "some_uuid",
            "instance_type": "flavor name",
            "instance_type_id": "flavor id",
            "display_name": "a display name",
            "created_at": "2015-01-09 21:26:54",
            "launched_at": "2015-01-09 21:27:54",
            "image_ref_url": "url.example",
            "state": "active",
            "state_description": "state description",
            "fixed_ips": [<FixedIps>],
            "memory_mb": 1024,
            "disk_gb": 20
        }
    """
    kwarg_map = BASE_KWARG_MAP.copy()

    def __init__(self, tenant_id, user_id, instance_id, instance_type,
                 instance_type_id, display_name, created_at, launched_at,
                 image_ref_url, state, state_description, fixed_ips,
                 memory_mb, disk_gb):
        super(ComputeInstanceDelete, self).__init__(locals())


class ComputeInstanceRebuild(EventBaseModel):
    """Compute Instance Rebuild Response Model

    @summary: Response model for a compute.instance.delete.*
        event notification
    @note: Represents a single event notification

    JSON Example:
        {
            "tenant_id": "123456",
            "user_id": "some_user",
            "instance_id": "some_uuid",
            "instance_type": "flavor name",
            "instance_type_id": "flavor id",
            "display_name": "a display name",
            "created_at": "2015-01-09 21:26:54",
            "launched_at": "2015-01-09 21:27:54",
            "image_ref_url": "url.example",
            "state": "active",
            "state_description": "state description",
            "fixed_ips": [<FixedIps>],
            "memory_mb": 1024,
            "disk_gb": 20
        }
    """
    kwarg_map = BASE_KWARG_MAP.copy()

    def __init__(self, tenant_id, user_id, instance_id, instance_type,
                 instance_type_id, display_name, created_at, launched_at,
                 image_ref_url, state, state_description, fixed_ips,
                 memory_mb, disk_gb):
        super(ComputeInstanceRebuild, self).__init__(locals())


class ComputeInstanceResizePrep(EventBaseModel):
    """Compute Instance Resize Prep Response Model

    @summary: Response model for a compute.instance.resize.prep.*
        event notification
    @note: Represents a single event notification

    JSON Example:
        {
            "tenant_id": "123456",
            "user_id": "some_user",
            "instance_id": "some_uuid",
            "instance_type": "flavor name",
            "instance_type_id": "flavor id",
            "new_instance_type": "target instance type",
            "new_instance_type_id": "target instance type id",
            "display_name": "a display name",
            "created_at": "2015-01-09 21:26:54",
            "launched_at": "2015-01-09 21:27:54",
            "image_ref_url": "url.example",
            "state": "active",
            "state_description": "state description",
            "fixed_ips": [<FixedIps>],
            "memory_mb": 1024,
            "disk_gb": 20,
        }
    """
    kwarg_map = BASE_KWARG_MAP.copy()
    kwarg_map['new_instance_type'] = 'new_instance_type'
    kwarg_map['new_instance_type_id'] = 'new_instance_type_id'

    def __init__(self, tenant_id, user_id, instance_id, instance_type,
                 instance_type_id, new_instance_type, new_instance_type_id,
                 display_name, created_at, launched_at, image_ref_url, state,
                 state_description, fixed_ips, memory_mb, disk_gb):
        super(ComputeInstanceResizePrep, self).__init__(locals())
