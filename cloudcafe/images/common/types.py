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


class ImageContainerFormat(object):
    """@summary: Types denoting an Image's container format"""

    BARE = "bare"
    OVF = "ovf"
    AKI = "aki"
    ARI = "ari"
    AMI = "ami"


class ImageDiskFormat(object):
    """@summary: Types denoting an Image's disk format"""

    RAW = "raw"
    VHD = "vhd"
    VMDK = "vmdk"
    VDI = "vdi"
    ISO = "iso"
    QCOW2 = "qcow2"
    AKI = "aki"
    AMI = "ami"
    ARI = "ari"


class ImageMemberStatus(object):
    """@summary: Types denoting an Image member's status"""

    ACCEPTED = 'accepted'
    PENDING = 'pending'
    REJECTED = 'rejected'


class ImageStatus(object):
    """@summary: Types denoting an Image's status"""

    QUEUED = "queued"
    SAVING = "saving"
    ACTIVE = "active"
    KILLED = "killed"
    PENDING_DELETE = "pending_delete"
    DELETED = "deleted"
    ERROR = "error"


class ImageVisibility(object):
    """@summary: Types denoting an Image's visibility"""

    PUBLIC = 'public'
    PRIVATE = 'private'


class Schemas(object):
    """@summary: Types denoting a schema"""

    IMAGE_SCHEMA = '/v2/schemas/image'
    IMAGES_SCHEMA = '/v2/schemas/images'
    IMAGE_MEMBER_SCHEMA = '/v2/schemas/member'
    IMAGE_MEMBERS_SCHEMA = '/v2/schemas/members'
    TASK_SCHEMA = '/v2/schemas/task'
    TASKS_SCHEMA = '/v2/schemas/tasks'
