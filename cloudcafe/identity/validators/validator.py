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


class ValidatorBase(object):
    """ Base class for validator types. """

    def __init__(self, next_validators=None):
        """
        @summary: Validator base constructor
        @return: None
        """
        if next_validators is not None:
            self.next_validators = next_validators
        else:
            self.next_validators = []

    def register_test_fixture(self, fixture):
        """
        @summary: Registers a test fixture to be used
            for any asserts or logging.
        @return: None
        """
        self.test_fixture = fixture

    def validate(self, response):
        """
        @summary: Validates a response, passes the response
            down to the next validators
        @return: list of ValidationStatuses
        """
        return [(next_validator.validate(response=response) for
                 next_validator in self.next_validators)]

    @property
    def next_validators(self):
        """
        @type ValidatorBase subclass
        """
        if self._next_validators is None:
            return []
        return self._next_validators

    @next_validators.setter
    def next_validators(self, value):
        self._next_validators = value


class ValidatorStatus(object):
    """ Holds the status result from a validation. """
    def __init__(self, message, status):
        """
        @summary Validator Status Constructor
        @param message A Descriptive message.
        @param status A short status string such as
            Passed or Failed.
        """
        self._message = message
        self._status = status

    @property
    def status(self):
        """
        @type string
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def message(self):
        """
        @type string
        """
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
