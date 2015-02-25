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


class NovaServerStatusTypes(object):
    """
    @summary: Types dictating an individual Server Status
    @cvar ACTIVE: Server is active and available
    @type ACTIVE: C{str}
    @cvar BUILD: Server is being built
    @type BUILD: C{str}
    @cvar ERROR: Server is in error
    @type ERROR: C{str}
    @note: This is essentially an Enumerated Type
    """
    ACTIVE = "ACTIVE"
    BUILD = "BUILD"
    REBUILD = "REBUILD"
    ERROR = "ERROR"
    DELETING = "DELETING"
    DELETED = "DELETED"
    RESCUE = "RESCUE"
    PREP_RESCUE = "PREP_RESCUE"
    INVALID_OPTION = "INVALID_OPTION"
    RESIZE = "RESIZE"
    VERIFY_RESIZE = "VERIFY_RESIZE"
    SUSPENDED = "SUSPENDED"
    SHUTOFF = "SHUTOFF"
    PAUSED = "PAUSED"


class ComputeTaskStates(object):
    NONE = 'none'

    # Basic server lifecycle
    SCHEDULING = 'scheduling'
    SPAWNING = 'spawning'
    BLOCK_DEVICE_MAPPING = 'block_device_mapping'
    DELETING = 'deleting'
    SOFT_DELETING = 'soft-deleting'
    RESTORING = 'restoring'
    SHELVING = 'shelving'
    SHELVING_IMAGE_PENDING_UPLOAD = 'shelving_image_pending_upload'
    SHELVING_IMAGE_UPLOADING = 'shelving_image_uploading'
    SHELVING_OFFLOADING = 'shelving_offloading'
    UNSHELVING = 'unshelving'

    # Server Actions
    REBUILDING = 'rebuilding'
    REBUILD_BLOCK_DEVICE_MAPPING = 'rebuild_block_device_mapping'
    REBUILD_SPAWNING = 'rebuild_spawning'
    RESIZE_PREP = 'resize_prep'
    RESIZE_MIGRATING = 'resize_migrating'
    RESIZE_MIGRATED = 'resize_migrated'
    RESIZE_FINISH = 'resize_finish'
    RESIZE_REVERTING = 'resize_reverting'
    RESIZE_CONFIRMING = 'resize_confirming'
    RESCUING = 'rescuing'
    UNRESCUING = 'unrescuing'
    UPDATING_PASSWORD = 'updating_password'
    PAUSING = 'pausing'
    UNPAUSING = 'unpausing'
    SUSPENDING = 'suspending'
    RESUMING = 'resuming'
    STOPPING = 'stopping'
    STARTING = 'starting'
    POWERING_OFF = 'powering-off'
    POWERING_ON = 'powering-on'
    MIGRATING = 'migrating'
    REBOOTING = 'rebooting'
    REBOOTING_HARD = 'rebooting_hard'

    # Imaging
    IMAGE_SNAPSHOT = 'image_snapshot'
    IMAGE_SNAPSHOT_PENDING = 'image_snapshot_pending'
    IMAGE_PENDING_UPLOAD = 'image_pending_upload'
    IMAGE_UPLOADING = 'image_uploading'


class NovaImageStatusTypes(object):
    """
    @summary: Types dictating an individual Server Status
    @cvar ACTIVE: Server is active and available
    @type ACTIVE: C{str}
    @cvar BUILD: Server is being built
    @type BUILD: C{str}
    @cvar ERROR: Server is in error
    @type ERROR: C{str}
    @note: This is essentially an Enumerated Type
    """
    ACTIVE = "ACTIVE"
    SAVING = "SAVING"
    ERROR = "ERROR"
    DELETED = "DELETED"
    UNKNOWN = "UNKNOWN"


class NovaServerRebootTypes(object):
    """
    @summary: Types dictating server reboot types
    @cvar HARD: Hard reboot
    @type HARD: C{str}
    @cvar SOFT: Soft reboot
    @type SOFT: C{str}
    @note: This is essentially an Enumerated Type
    """
    HARD = "HARD"
    SOFT = "SOFT"


class NovaVolumeStatusTypes(object):
    """
    @summary: Types dictating an individual Volume Status
    @cvar AVAILABLE: Volume is active and available
    @type AVAILABLE: C{str}
    @cvar CREATING: Volume is being created
    @type CREATING: C{str}
    @cvar ERROR: Volume is in error
    @type ERROR: C{str}
    @cvar DELETING: Volume is being deleted
    @type DELETING: C{str}
    @cvar ERROR_DELETING: Volume is in error while being deleted
    @type ERROR_DELETING: C{str}
    @cvar IN_USE: Volume is active and available
    @type IN_USE: C{str}
    @note: This is essentially an Enumerated Type
    """
    AVAILABLE = "available"
    ATTACHING = "attaching"
    CREATING = "creating"
    DELETING = "deleting"
    ERROR = "error"
    ERROR_DELETING = "error_deleting"
    IN_USE = "in-use"


class BackupTypes(object):
    """
    @summary: Types dictating server backup types
    @cvar DAILY: Daily backup
    @type DAILY: C{str}
    @cvar WEEKLY: Weekly backup
    @type WEEKLY: C{str}
    @note: This is essentially an Enumerated Type
    """
    DAILY = "daily"
    WEEKLY = "weekly"


class HostServiceTypes(object):
    """
    @summary: Types dictating host service types
    @cvar COMPUTE: compute service
    @type COMPUTE: C{str}
    @cvar NETWORK: network service
    @type NETWORK: C{str}
    @note: This is essentially an Enumerated Type
    """
    COMPUTE = "compute"
    NETWORK = "network"


class ComputeHypervisors(object):
    XEN_SERVER = 'xen_server'
    KVM = 'kvm'
    QEMU = 'qemu'
    HYPER_V = 'hyper_v'
    DOCKER = 'docker'
    IRONIC = 'ironic'
    LXC_LIBVIRT = 'lxc_libvirt'
    ON_METAL = 'rackspace_onmetal'


class InstanceAuthStrategies(object):
    PASSWORD = 'password'
    KEY = 'key'


class VncConsoleTypes(object):
    NOVNC = 'novnc'
    XVPVNC = 'xvpvnc'


class SourceTypes(object):
    IMAGE = 'image'
    SNAPSHOT = 'snapshot'


class DestinationTypes(object):
    VOLUME = 'volume'
