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


class LBaaSStatusTypes(object):
    """
    @summary: Types dictating an individual Status for an LBaaS entity
    @cvar DEFERRED: An entity has been created but is not yet linked to a
        load balancer.  This is not a functioning state.
    @type DEFERRED: C{str}
    @cvar PENDING_CREATE: An entity is being created, but it is not yet
        functioning.
    @type PENDING_CREATE: C{str}
    @cvar PENDING_UPDATE: An entity has been updated.  It remains in a
        functioning state.
    @type PENDING_UPDATE: C{str}
    @cvar PENDING_DELETE: An entity is in the process of being deleted.
    @type PENDING_DELETE: C{str}
    @cvar ACTIVE: An entity is in a normal functioning state.
    @type ACTIVE: C{str}
    @cvar INACTIVE: Applies to members that fail health checks.
    @type INACTIVE: C{str}
    @cvar ERROR: Something has gone wrong.  This may be either a functioning
        or non-functioning state.
    @type ERROR: C{str}
    @note: This is essentially an Enumerated Type
    """
    DEFERRED = "DEFERRED"
    PENDING_CREATE = "PENDING_CREATE"
    PENDING_UPDATE = "PENDING_UPDATE"
    PENDING_DELETE = "PENDING_DELETE"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"
