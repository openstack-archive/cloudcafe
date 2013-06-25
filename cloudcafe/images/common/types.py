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


class ImageStatus(object):
    """
    @summary: Types denoting an Image's status
    @cvar QUEUED: Image identifier has been reserved
    @type QUEUED: C{str}
    @cvar SAVING: Image's raw data is currently being uploaded
    @type SAVING: C{str}
    @cvar ACTIVE: Image is active and available
    @type ACTIVE: C{str}
    @cvar KILLED: An error occured during upload of image data
    @type KILLED: C{str}
    @cvar PENDING_DELETE: Image data is not yet removed
    @type PENDING_DELETE: C{str}
    @cvar DELETED: Image information has been retained but image is no longer \
            available
    @type DELETED: C{str}
    """

    QUEUED = "queued"
    SAVING = "saving"
    ACTIVE = "active"
    KILLED = "killed"
    PENDING_DELETE = "pending_delete"
    DELETED = "deleted"


class ImageDiskFormat(object):
    """
    @summary: Types denoting an Image's disk format.
    """

    RAW = "raw"
    VHD = "vhd"
    VMDK = "vmdk"
    VDI = "vdi"
    ISO = "iso"
    QCOW2 = "qcow2"
    AKI = "aki"
    AMI = "ami"
    ARI = "ari"


class ImageContainerFormat(object):
    """
    @summary: Types denoting an Image's container format.
    """

    BARE = "bare"
    OVF = "ovf"
    AKI = "aki"
    ARI = "ari"
    AMI = "ami"


class ImageVisibility(object):
    PUBLIC = 'public'
    PRIVATE = 'private'
