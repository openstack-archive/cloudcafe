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


class ImageContainerFormat(object):
    """@summary: Types denoting an Image's container format"""

    BARE = 'bare'
    OVF = 'ovf'
    AKI = 'aki'
    ARI = 'ari'
    AMI = 'ami'


class ImageDiskFormat(object):
    """@summary: Types denoting an Image's disk format"""

    RAW = 'raw'
    VHD = 'vhd'
    VMDK = 'vmdk'
    VDI = 'vdi'
    ISO = 'iso'
    QCOW2 = 'qcow2'
    AKI = 'aki'
    AMI = 'ami'
    ARI = 'ari'


class ImageMemberStatus(object):
    """@summary: Types denoting an Image member's status"""

    ACCEPTED = 'accepted'
    PENDING = 'pending'
    REJECTED = 'rejected'
    ALL = 'all'


class ImageOSType(object):
    """@summary: Types denoting an Image's os type"""

    LINUX = 'linux'
    WINDOWS = 'windows'


class ImageStatus(object):
    """@summary: Types denoting an Image's status"""

    QUEUED = 'queued'
    SAVING = 'saving'
    ACTIVE = 'active'
    KILLED = 'killed'
    PENDING_DELETE = 'pending_delete'
    DELETED = 'deleted'
    ERROR = 'error'
    DEACTIVATED = 'deactivated'


class ImageType(object):
    """@summary: Types denoting an Image's type"""

    BASE = 'base'
    IMPORT = 'import'
    SNAPSHOT = 'snapshot'


class ImageVisibility(object):
    """@summary: Types denoting an Image's visibility"""

    PUBLIC = 'public'
    PRIVATE = 'private'
    SHARED = 'shared'


class Schemas(object):
    """@summary: Types denoting a schema"""

    IMAGE_SCHEMA = '/v2/schemas/image'
    IMAGES_SCHEMA = '/v2/schemas/images'
    IMAGE_MEMBER_SCHEMA = '/v2/schemas/member'
    IMAGE_MEMBERS_SCHEMA = '/v2/schemas/members'
    TASK_SCHEMA = '/v2/schemas/task'
    TASKS_SCHEMA = '/v2/schemas/tasks'


class SortDirection(object):
    """@summary: Types denoting a sort direction"""

    ASCENDING = 'asc'
    DESCENDING = 'desc'


class TaskStatus(object):
    """@summary: Types denoting a Task's status"""

    PENDING = 'pending'
    PROCESSING = 'processing'
    SUCCESS = 'success'
    FAILURE = 'failure'


class TaskTypes(object):
    """@summary: Types denoting a Task's types"""

    IMPORT = 'import'
