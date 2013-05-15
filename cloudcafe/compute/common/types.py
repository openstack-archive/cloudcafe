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
