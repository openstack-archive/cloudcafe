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


class NetworkIDMissingException(Exception):
    """Required Network ID missing exception"""
    def __init__(self, message='Network ID is required'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class InvalidIPException(Exception):
    """Invalid IPv4 or IPv6 cidr exception"""
    def __init__(self, message='Invalid IP cidr'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ResourceBuildException(Exception):
    """Unable to create resource exception, for ex. a network"""
    def __init__(self, message='Unable to create resource'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class TimeoutException(Exception):
    """Timeout exception"""
    def __init__(self, message='Request timed out'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class UnsupportedTypeException(Exception):
    """Unsupported type exception"""
    def __init__(self, message='Type not supported'):
        self.message = message

    def __str__(self):
        return repr(self.message)
