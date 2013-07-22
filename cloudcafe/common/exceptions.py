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
