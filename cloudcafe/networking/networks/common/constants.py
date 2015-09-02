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

from cloudcafe.compute.common.types import NovaServerStatusTypes


class NeutronResource(object):
    """Neutron resource types"""

    NETWORK = 'network'
    NETWORKS = 'networks'
    SUBNET = 'subnet'
    SUBNETS = 'subnets'
    PORT = 'port'
    PORTS = 'ports'

    PLURALS = {NETWORK: NETWORKS, SUBNET: SUBNETS, PORT: PORTS}

    def __init__(self, singular_type):
        self.singular = singular_type

    @property
    def plural(self):
        return self.PLURALS.get(self.singular, self.singular)


class NetworkTypes(object):
    """Network types"""
    PUBLIC = 'public'
    SERVICE = 'service'
    ISOLATED = 'isolated'


class PortTypes(object):
    """Port types"""
    PUBLIC = 'pnet'
    SERVICE = 'snet'
    ISOLATED = 'inet'


class NeutronResponseCodes(object):
    """HTTP Neutron API Response codes"""

    LIST_NETWORKS = 200
    GET_NETWORK = 200
    CREATE_NETWORK = 201
    UPDATE_NETWORK = 200
    DELETE_NETWORK = 204
    LIST_SUBNETS = 200
    GET_SUBNET = 200
    CREATE_SUBNET = 201
    UPDATE_SUBNET = 200
    DELETE_SUBNET = 204
    LIST_PORTS = 200
    GET_PORT = 200
    CREATE_PORT = 201
    UPDATE_PORT = 200
    DELETE_PORT = 204

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    REQUEST_ENTITY_TOO_LARGE = 413
    INTERNAL_SERVER_ERROR = 500
    MAC_GENERATION_FAILURE = 503


class NeutronErrorTypes(object):
    """Neutron Error Types"""

    ADDR_FORMAT_ERROR = 'AddrFormatError'
    GATEWAY_CONFLICT_WITH_ALLOCATION_POOLS = \
        'GatewayConflictWithAllocationPools'
    HTTP_BAD_REQUEST = 'HTTPBadRequest'
    HTTP_INTERNAL_SERVER_ERROR = 'HTTPInternalServerError'
    INVALID_ALLOCATION_POOL = 'InvalidAllocationPool'
    IP_ADDRESS_GENERATION_FAILURE = 'IpAddressGenerationFailure'
    IP_ADDRESS_IN_USE = 'IpAddressInUse'
    INVALID_INPUT = 'InvalidInput'
    NETWORK_IN_USE = 'NetworkInUse'
    NETWORK_NOT_FOUND = 'NetworkNotFound'
    OUT_OF_BOUNDS_ALLOCATION_POOL = 'OutOfBoundsAllocationPool'
    OVERLAPPING_ALLOCATION_POOLS = 'OverlappingAllocationPools'
    OVER_QUOTA = 'OverQuota'
    POLICY_NOT_AUTHORIZED = 'PolicyNotAuthorized'
    PORT_NOT_FOUND = 'PortNotFound'
    SECURITY_GROUPS_NOT_IMPLEMENTED = 'SecurityGroupsNotImplemented'
    SUBNET_NOT_FOUND = 'SubnetNotFound'


class ComputeResponseCodes(object):
    """HTTP Compute API Response codes"""

    NOT_FOUND = 404
    SERVER_GET = 200


class ComputeStatus(NovaServerStatusTypes):
    """Compute server instance status"""
