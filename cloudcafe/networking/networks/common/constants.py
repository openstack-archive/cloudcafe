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
    MAC_GENERATION_FAILURE = 503
