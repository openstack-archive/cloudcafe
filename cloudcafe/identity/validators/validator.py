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


class ValidationError(object):
    def __init__(self, error_message):
        self.error_message = error_message


class ValidatorBase(object):
    # We need the assertions defined here.

    def __init__(self, next_validators=None):
        if next_validators is not None:
            self.next_validators = next_validators
        else:
            self.next_validators = []

    def register_test_fixture(self, fixture):
        self.test_fixture = fixture

    def validate(self, response):
        return [(next_validator.validate(response) for
                 next_validator in self.next_validators)]

    @property
    def next_validators(self):
        if self._next_validators is None:
            return []
        return self._next_validators

    @next_validators.setter
    def next_validators(self, value):
        self._next_validators = value


class ValidatorStatus(object):
    def __init__(self, message, status):
        self._message = message
        self._status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
