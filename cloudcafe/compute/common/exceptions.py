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


class TimeoutException(Exception):
    """Exception on timeout"""
    def __init__(self, message='Request timed out'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class BuildErrorException(Exception):
    """Exception on server build"""
    def __init__(self, message='Build Error'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class DeleteException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class BadRequest(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class BadRequestHtml(Exception):
    def __init__(self):
        self.message = '400 - Bad Request.'

    def __str__(self):
        return repr(self.message)


class OverLimit(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ComputeFault(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ItemNotFound(Exception):
    def __init__(self):
        self.message = '404 - Not found.'

    def __str__(self):
        return repr(self.message)


class BadMethod(Exception):
    def __init__(self, message):
        self.message = "405 - Bad Method."

    def __str__(self):
        return repr(self.message)


class Unauthorized(Exception):
    def __init__(self):
        self.message = "401 - Unauthorized."

    def __str__(self):
        return repr(self.message)


class Forbidden(Exception):
    def __init__(self, message):
        self.message = "403 - Forbidden Operation"

    def __str__(self):
        return repr(self.message)


class ActionInProgress(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class BuildInProgress(Exception):
    def __init__(self):
        self.message = "409 - Action failed. Entity is currently building."

    def __str__(self):
        return repr(self.message)


class ServiceUnavailable(Exception):
    def __init__(self):
        self.message = "503 - The service is currently unavailable."

    def __str__(self):
        return repr(self.message)


class FileNotFoundException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class SshConnectionException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ServerUnreachable(Exception):
    def __init__(self, address):
        self.message = 'Could not reach the server at %s.' % address

    def __str__(self):
        return repr(self.message)


class InvalidJSON(Exception):
    def __init__(self, message, expected_response):
        self.message = 'Unexpected JSON response. Parsing of the following JSON failed ' + message + '. Expected response of type ' + expected_response


class AuthenticationTimeoutException(Exception):
    def __init__(self, server_id=None):
        if server_id is None:
            self.message = 'Authentication to the desired failed due to timing out.'
        else:
            self.message = 'Authentication to server ' + server_id + ' failed due to timing out.'

    def __str__(self):
        return repr(self.message)


class BadMediaType(Exception):
    def __init__(self, message):
        self.message = '415 - Bad media type.'

    def __str__(self):
        return repr(self.message)


class InternalServerError(Exception):
    def __init__(self):
        self.message = '500 - Internal Server Error.'

    def __str__(self):
        return repr(self.message)
