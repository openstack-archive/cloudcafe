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
from cloudcafe.networking.networks.common.constants \
    import NeutronResource, NeutronResponseCodes, NeutronErrorTypes


class IPAddressesResource(NeutronResource):
    """IP addresses resource types"""

    # Resources to be used by the behavior
    IP_ADDRESS = 'ip_address'
    IP_ADDRESSES = 'ip_addresses'

    PLURALS = NeutronResource.PLURALS
    PLURALS.update({IP_ADDRESS: IP_ADDRESSES})


class IPAddressesResponseCodes(NeutronResponseCodes):
    """HTTP IP Address API Response codes"""

    LIST_IP_ADDRESSES = 200
    GET_IP_ADDRESS = 200

    # Using HTTP 200 instead of 201 till NCP-1577 is fixed
    CREATE_IP_ADDRESS = 200
    UPDATE_IP_ADDRESS = 200
    DELETE_IP_ADDRESS = 204


class IPAddressesErrorTypes(NeutronErrorTypes):
    """IP Address Error Types"""

    IP_ADDRESS_NOT_FOUND = 'IPAddressNotFound'


class IPAddressesServerZone(object):
    """
    Scheduler hint keys for targeting the same or different cell/host for
    server builds
    """

    PUBLIC_IP_ZONE_NEAR = 'public_ip_zone:near'
    PUBLIC_IP_ZONE_FAR = 'public_ip_zone:far'
    DIFFERENT_HOST = 'different_host'
