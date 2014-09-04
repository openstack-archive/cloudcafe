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


class BaseNetworkingException(Exception):
    MSG = 'No error msg set'

    def __init__(self, msg=None):
        self.message = msg or self.MSG

    def __str__(self):
        return repr(self.message)


class NetworkIDMissingException(BaseNetworkingException):
    MSG = 'Network ID is required'


class NetworkGETException(BaseNetworkingException):
    MSG = 'Unable to GET Network'


class SubnetGETException(BaseNetworkingException):
    MSG = 'Unable to GET Subnet'


class InvalidIPException(BaseNetworkingException):
    MSG = 'Invalid IP cidr'


class ResourceBuildException(BaseNetworkingException):
    MSG = 'Unable to create resource'


class TimeoutException(BaseNetworkingException):
    MSG = 'Request timed out'


class UnsupportedTypeException(BaseNetworkingException):
    MSG = 'Type not supported'
