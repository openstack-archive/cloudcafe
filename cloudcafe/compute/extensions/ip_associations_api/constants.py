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
from cloudcafe.compute.common.constants import HTTPResponseCodes


class IPAssociationsResponseCodes(HTTPResponseCodes):
    """HTTP IP Associations API Expected Response codes"""

    LIST_IP_ASSOCIATIONS = 200
    GET_IP_ASSOCIATION = 200
    CREATE_IP_ASSOCIATION = 201
    DELETE_IP_ASSOCIATION = 204
