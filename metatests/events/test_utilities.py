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

from cloudcafe.events.utilities import *


INVALID_ENTITY = {'check_entity': 'empty entity'}
INVALID_SCHEMA = {'check_schema': 'schema validation failed'}
INVALID_NAME = {'check_name': 'empty name'}
INVALID_EMAIL = {'check_email': 'empty email'}
INVALID_ID = {'check_id': 'negative id'}


@bind
def check_entity(data):
    if data:
        return Result(True, data)
    else:
        return Result(False, INVALID_ENTITY)


@bind
def check_schema(data):
    if 'name' in data and 'email' in data and 'id' in data:
        return Result(True, data)
    else:
        return Result(False, INVALID_SCHEMA)


@bind
def check_name(data):
    if data.get('name'):
        return Result(True, data)
    else:
        return Result(False, INVALID_NAME)


@bind
def check_email(data):
    if data.get('email'):
        return Result(True, data)
    else:
        return Result(False, INVALID_EMAIL)


@bind
def check_id(data):
    if data.get('id') >= 0:
        return Result(True, data)
    else:
        return Result(False, INVALID_ID)


def check_all(message):
    # Convert message to Result
    data = box_data(message)

    # Do these checks in order
    # Failures pass through and skip subsequent steps
    data = process_sequential([check_entity, check_schema], data)

    # Do these checks in "parallel"
    # Failures are compiled into a dictionary
    data = process_parallel_and(
        [check_name, check_email, check_id],
        data)

    return data


def check_parallel_or(message):
    # Convert message to Result
    data = box_data(message)

    # Do these checks in "parallel"
    # Failures are discarded if any pass
    data = process_parallel_or(
        [check_name, check_email, check_id],
        data)

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


class TestUtilities(BaseUtilitiesTest):

    def test_valid(self):
        result = check_all(self.message_valid)
        self.assertTrue(result.success)
        self.assertEqual(result.payload, self.message_valid)

    def test_invalid_sequential(self):
        result = check_all(self.message_invalid_schema)
        self.assertFalse(result.success)
        self.assertEqual(result.payload, INVALID_SCHEMA)

    def test_invalid_parallel_and(self):
        result = check_all(self.message_invalid_values)
        self.assertFalse(result.success)
        payload = dict(INVALID_EMAIL, **INVALID_ID)
        self.assertEqual(result.payload, payload)

    def test_invalid_parallel_or(self):
        result = check_parallel_or(self.message_invalid_values)
        self.assertTrue(result.success)
        self.assertEqual(result.payload, self.message_invalid_values)
