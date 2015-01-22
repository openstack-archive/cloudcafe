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

import unittest

from cloudcafe.events.utilities import (
    bind, box_data, process_parallel, process_sequential, Result,
    validator_and, validator_or)


class Validators(object):
    """Example validators and usage methods to support workflow testing"""

    INVALID_ENTITY = {'check_entity': 'empty entity'}
    INVALID_SCHEMA = {'check_schema': 'schema validation failed'}
    INVALID_NAME = {'check_name': 'empty name'}
    INVALID_EMAIL = {'check_email': 'empty email'}
    INVALID_ID = {'check_id': 'negative id'}

    @staticmethod
    @bind
    def check_entity(data):
        if data:
            return Result(True, data)
        else:
            return Result(False, Validators.INVALID_ENTITY)

    @staticmethod
    @bind
    def check_schema(data):
        if 'name' in data and 'email' in data and 'id' in data:
            return Result(True, data)
        else:
            return Result(False, Validators.INVALID_SCHEMA)

    @staticmethod
    @bind
    def check_name(data):
        if data.get('name'):
            return Result(True, data)
        else:
            return Result(False, Validators.INVALID_NAME)

    @staticmethod
    @bind
    def check_email(data):
        if data.get('email'):
            return Result(True, data)
        else:
            return Result(False, Validators.INVALID_EMAIL)

    @staticmethod
    @bind
    def check_id(data):
        if data.get('id') >= 0:
            return Result(True, data)
        else:
            return Result(False, Validators.INVALID_ID)

    @staticmethod
    def check_all(message):
        # Convert message to Result
        data = box_data(message)

        # Do these checks in order
        # Failures pass through and skip subsequent steps
        data = process_sequential(
            [Validators.check_entity, Validators.check_schema], data)

        # Do these checks in "parallel"
        # Failures are compiled into a dictionary
        data = process_parallel(
            [Validators.check_name,
             Validators.check_email,
             Validators.check_id], data, validator_and)

        return data

    @staticmethod
    def check_parallel_or(message):
        # Convert message to Result
        data = box_data(message)

        # Do these checks in "parallel"
        # Failures are discarded if any pass
        data = process_parallel(
            [Validators.check_name, Validators.check_email, Validators.check_id],
            data, validator_or)

        return data


class BaseUtilitiesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseUtilitiesTest, cls).setUpClass()

        cls.message_valid = {
            'name': 'John',
            'email': 'john@doe.com',
            'id': 1}

        cls.message_invalid_schema = {
            'name': 'John',
            'email': 'john@doe.com'}

        cls.message_invalid_values = {
            'name': 'John',
            'email': '',
            'id': -1}

        cls.result_success = Result(True, 'Success')
        cls.result_failure = Result(False, {'name': 'Failure'})
        cls.result_failure_alt = Result(False, {'alt': 'Failure'})


class TestValidatorCombinationMethods(BaseUtilitiesTest):
    """Test the methods for combining Results"""

    def test_and_both_success(self):
        result = validator_and(self.result_success, self.result_success)
        self.assertTrue(result.success)
        self.assertEqual(result.payload, self.result_success.payload)

    def test_and_first_failure(self):
        result = validator_and(self.result_failure, self.result_success)
        self.assertFalse(result.success)
        self.assertEqual(result.payload, self.result_failure.payload)

    def test_and_second_failure(self):
        result = validator_and(self.result_success, self.result_failure)
        self.assertFalse(result.success)
        self.assertEqual(result.payload, self.result_failure.payload)

    def test_and_both_failure(self):
        result = validator_and(self.result_failure, self.result_failure_alt)
        self.assertFalse(result.success)
        self.assertEqual(result.payload, dict(
            self.result_failure.payload, **self.result_failure_alt.payload))

    def test_or_both_success(self):
        result = validator_or(self.result_success, self.result_success)
        self.assertTrue(result.success)
        self.assertEqual(result.payload, self.result_success.payload)

    def test_or_first_failure(self):
        result = validator_or(self.result_failure, self.result_success)
        self.assertTrue(result.success)
        self.assertEqual(result.payload, self.result_success.payload)

    def test_or_second_failure(self):
        result = validator_or(self.result_success, self.result_failure)
        self.assertTrue(result.success)
        self.assertEqual(result.payload, self.result_success.payload)

    def test_or_both_failure(self):
        result = validator_or(self.result_failure, self.result_failure_alt)
        self.assertFalse(result.success)
        self.assertEqual(result.payload, dict(
            self.result_failure.payload, **self.result_failure_alt.payload))


class TestValidationWorkflow(BaseUtilitiesTest):
    """End to end testing of a validation workflow"""

    def test_valid(self):
        result = Validators.check_all(self.message_valid)
        self.assertTrue(result.success)
        self.assertEqual(result.payload, self.message_valid)

    def test_invalid_sequential(self):
        result = Validators.check_all(self.message_invalid_schema)
        self.assertFalse(result.success)
        self.assertEqual(result.payload, Validators.INVALID_SCHEMA)

    def test_invalid_parallel_and(self):
        result = Validators.check_all(self.message_invalid_values)
        self.assertFalse(result.success)
        payload = dict(Validators.INVALID_EMAIL, **Validators.INVALID_ID)
        self.assertEqual(result.payload, payload)

    def test_invalid_parallel_or(self):
        result = Validators.check_parallel_or(self.message_invalid_values)
        self.assertTrue(result.success)
        self.assertEqual(result.payload, self.message_invalid_values)
