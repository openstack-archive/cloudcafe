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

import unittest
import itertools

from cloudcafe.identity.validators.validator import (ValidatorBase,
                                                     ValidatorStatus)


class FakeResponse(object):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2


class ValidateArg1(ValidatorBase):
    def __init__(self, arg1, next_validators=None):
        super(ValidateArg1, self).__init__(next_validators)
        self.arg1 = arg1

    def validate(self, response):
        if response.arg1 == self.arg1:
            result = ValidatorStringStatus("Arg1 equal to blah", "Passed")
        else:
            result = ValidatorStringStatus("Arg1:{0} not equal to blah"
                                           "".format(self.arg1), "Failed")
        if not self.next_validators:
            return result
        return([result] + list(
            itertools.chain.from_iterable(
                [(next_validator.validate(response) for
                    next_validator in self.next_validators)])))


class ValidateArg2(ValidatorBase):
    def __init__(self, arg2, next_validators=None):
        super(ValidateArg2, self).__init__(next_validators)
        self.arg2 = arg2

    def validate(self, response):
        if response.arg2 == self.arg2:
            result = ValidatorStringStatus("Arg2 equal to blah", "Passed")
        else:
            result = ValidatorStringStatus("Arg2:{0} not equal to blah"
                                           "".format(self.arg2), "Failed")
        if not self.next_validators:
            return result
        return([result] + list(
            itertools.chain.from_iterable(
                [(next_validator.validate(response) for
                    next_validator in self.next_validators)])))


class ValidatorStringStatus(ValidatorStatus):
    def __init__(self, message, status):
        super(ValidatorStringStatus, self).__init__(message, status)

    def __str__(self):
        return "message:{0}, status:{1}".format(self.message, self.status)


class ValidatorTests(unittest.TestCase):

    def test_simple_success(self):
        self.assertEqual("Passed", ValidateArg1("blah").validate(
            FakeResponse("blah", "blah2")).status)

    def test_simple_failure(self):
        self.assertEqual("Failed", ValidateArg1("blah2").validate(
            FakeResponse("blah", "blah2")).status)

    def test_next_validators(self):
        both_success_validator = ValidateArg1("blah", [ValidateArg2("blah2")])
        for status_item in both_success_validator.validate(
                FakeResponse("blah", "blah2")):
            self.assertEqual("Passed", status_item.status)
        arg1_failure_validator = ValidateArg1("blahs",
                                              [ValidateArg2("blah2")])
        status_list = list(arg1_failure_validator.validate(
            FakeResponse("blah", "blah2")))
        self.assertEqual("Failed", status_list[0].status)
        self.assertEqual("Passed", status_list[1].status)

        arg2_failure_validator = ValidateArg1("blah",
                                              [ValidateArg2("blahs2")])
        status_list = list(arg2_failure_validator.validate(
                           FakeResponse("blah", "blah2")))
        self.assertEqual("Passed", status_list[0].status)
        self.assertEqual("Failed", status_list[1].status)


if __name__ == '__main__':
    unittest.main()
