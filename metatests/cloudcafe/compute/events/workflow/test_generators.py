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
import uuid

import raxcafe.common.workflow.base as wf
from raxcafe.common.workflow.generators import api_call
from raxcafe.common.workflow.generators import dd_api_call
from raxcafe.common.workflow.generators import check_response_code
from raxcafe.common.workflow.generators import check_item_is_uuid
from raxcafe.common.workflow.generators import check_item_is_instance_of
from raxcafe.common.workflow.generators import check_item_is_valid_ip_address
from raxcafe.common.workflow.generators import check_item_is_valid_datetime
from raxcafe.common.workflow.generators import check_item_is_valid_url
from raxcafe.common.workflow.generators import check_iterable
from raxcafe.common.workflow.generators import extract_item
from raxcafe.common.workflow.generators import check_number_in_range
from raxcafe.common.workflow.generators import (
    check_number_within_absolute_tolerance)
from raxcafe.common.workflow.generators import (
    check_number_within_percent_tolerance)


class TestApiCallGenerator(unittest.TestCase):
    def setUp(self):
        self.client_args = dict(data=42)
        self.client_object = self.Client()
        self.data_dict = dict(client=self.client_object)

    class Client(object):
        def passthrough(self, data):
            return data

    @staticmethod
    def _passthrough(data):
        return data

    @staticmethod
    def _exception_method(data):
        raise IOError('Test')

    def test_api_call_success(self):
        """Check happy path"""
        method = api_call(client_method=self._passthrough)
        result = method(self.client_args)
        self.assertEqual(result, self.client_args['data'])

    def test_client_object_api_call_success(self):
        """Check happy path with client object"""
        method = api_call(client_method=self.client_object.passthrough)
        result = method(self.client_args)
        self.assertEqual(result, self.client_args['data'])

    def test_api_call_failure(self):
        """Check failure case of API call failing with exception"""
        method = api_call(client_method=self._exception_method)
        result = method(self.client_args)
        self.assertIsInstance(result, wf.Error)


class TestCheckResponseCallGenerator(unittest.TestCase):
    def setUp(self):
        self.response_code = 200
        self.response = self.Response(status_code=self.response_code)

    class Response(object):
        def __init__(self, status_code):
            self.status_code = status_code

    def test_check_response_success(self):
        """Check happy path"""
        method = check_response_code(expected=self.response_code)
        result = method(self.response)
        self.assertEqual(result, self.response)

    def test_check_response_wrong_response_code(self):
        """Check failure case of wrong response code"""
        method = check_response_code(expected=42)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_check_response_bad_accessor(self):
        """Check failure case of invalid accessor"""
        method = check_response_code(expected=self.response_code,
                                     accessor=None)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestCheckItemIsUuidGenerator(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.valid_uuid = str(uuid.uuid4())
            self.invalid_uuid = '12345'

    def test_check_uuid_success(self):
        """Check happy path"""
        method = check_item_is_uuid(item_name='test-uuid',
                                    accessor=lambda x: x.valid_uuid)
        result = method(self.response)
        self.assertEqual(result, self.response)

    def test_check_uuid_invalid(self):
        """Check failure case of invalid UUID"""
        method = check_item_is_uuid(item_name='test-uuid',
                                    accessor=lambda x: x.invalid_uuid)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_check_uuid_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_item_is_uuid(item_name='test-uuid',
                                    accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestCheckItemIsInstanceOfGenerator(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.foo = 42
            self.optional = None

    def test_check_instance_success(self):
        """Check happy path"""
        method = check_item_is_instance_of(
            item_name='test-item', expected_type=int,
            accessor=lambda x: x.foo, optional=False)
        result = method(self.response)
        self.assertEqual(result, self.response)

    def test_check_instance_optional_success(self):
        """Check happy path with optional item"""
        method = check_item_is_instance_of(
            item_name='test-item', expected_type=int,
            accessor=lambda x: x.optional, optional=True)
        result = method(self.response)
        self.assertEqual(result, self.response)

    def test_check_instance_wrong_type(self):
        """Check failure case of unexpected type"""
        method = check_item_is_instance_of(
            item_name='test-item', expected_type=bool,
            accessor=lambda x: x.foo, optional=False)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_check_instance_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_item_is_instance_of(
            item_name='test-item', expected_type=int,
            accessor=lambda x: x.bar, optional=False)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestCheckItemIsValidIpGenerator(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.valid_ip = '192.168.1.1'
            self.invalid_ip = '1.1.1.1.1'
            self.optional = None

    def test_check_ip_success(self):
        """Check happy path"""
        method = check_item_is_valid_ip_address(
            item_name='test-item', accessor=lambda x: x.valid_ip)
        result = method(self.response)
        self.assertEqual(result, self.response)

    def test_check_ip_optional_success(self):
        """Check happy path with optional item"""
        method = check_item_is_valid_ip_address(
            item_name='test-item', accessor=lambda x: x.optional,
            optional=True)
        result = method(self.response)
        self.assertEqual(result, self.response)

    def test_check_ip_invalid(self):
        """Check failure case of invalid IP address"""
        method = check_item_is_valid_ip_address(
            item_name='test-item', accessor=lambda x: x.invalid_ip)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_check_ip_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_item_is_valid_ip_address(item_name='test-item',
                                                accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestCheckItemIsValidDatetime(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.valid_datetime = '2015-01-01T00:00:00Z'
            self.invalid_datetime = '2015-00-00T00:00:00Z'

    def test_check_datetime_success(self):
        """Check happy path"""
        method = check_item_is_valid_datetime(
            item_name='test-item', accessor=lambda x: x.valid_datetime)
        result = method(self.response)
        self.assertEqual(result, self.response)

    def test_check_datetime_invalid(self):
        """Check failure case of invalid datetime"""
        method = check_item_is_valid_datetime(
            item_name='test-item', accessor=lambda x: x.invalid_datetime)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_check_datetime_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_item_is_valid_datetime(
            item_name='test-item', accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestCheckItemIsValidUrl(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.valid_url = 'http://www.valid.com'
            self.invalid_url = 42

    def test_check_url_success(self):
        """Check happy path"""
        method = check_item_is_valid_url(
            item_name='test-item', accessor=lambda x: x.valid_url)
        result = method(self.response)
        self.assertEqual(result, self.response)

    def test_check_url_invalid(self):
        """Check failure case of invalid URL"""
        method = check_item_is_valid_url(
            item_name='test-item', accessor=lambda x: x.invalid_url)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_check_url_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_item_is_valid_url(
            item_name='test-item', accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestCheckIterable(unittest.TestCase):
    def setUp(self):
        self.validator = wf.WorkflowRunner('test-validator',
                                           tasks=[self._pass])
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.list_iterable = [1, 2, 3]
            self.dict_iterable = dict(a=1, b=2, c=3)

    @staticmethod
    def _pass(data):
        return data

    def test_check_iterable_list_success(self):
        """Check happy path with list iterable"""
        method = check_iterable(
            validator=self.validator, obj_name='list_iterable',
            accessor=lambda x: x.list_iterable)
        result = method(self.response)
        self.assertIsInstance(result, tuple)
        validator_results = result[0].results
        self.assertEqual(len(validator_results), 3)

    def test_check_iterable_dict_success(self):
        """Check happy path with dict iterable"""
        method = check_iterable(
            validator=self.validator, obj_name='dict_iterable',
            accessor=lambda x: x.dict_iterable)
        result = method(self.response)
        self.assertIsInstance(result, tuple)
        validator_results = result[0].results
        self.assertEqual(len(validator_results), 3)

    def test_check_iterable_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_iterable(validator=self.validator, obj_name='iterable',
                                accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestExtractItemGenerator(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.foo = 42

    def test_extract_item_success(self):
        """Check happy path"""
        method = extract_item(item_name='foo', accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertEqual(result, 42)

    def test_extract_item_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = extract_item(item_name='bar', accessor=lambda x: x.bar)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestNumberInRange(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.integer = 7
            self.floating = 1.2
            self.invalid = 'invalid'

    def test_int_in_range_success(self):
        """Check happy path for int"""
        method = check_number_in_range(
            upper_bound=10, lower_bound=0, accessor=lambda x: x.integer)
        result = method(self.response)
        self.assertEqual(result, 7)

    def test_float_in_range_success(self):
        """Check happy path for float"""
        method = check_number_in_range(
            upper_bound=10, lower_bound=0, accessor=lambda x: x.floating)
        result = method(self.response)
        self.assertEqual(result, 1.2)

    def test_int_in_range_failure(self):
        """Check failure case of int out of range"""
        method = check_number_in_range(
            upper_bound=1, lower_bound=0, accessor=lambda x: x.integer)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_float_in_range_failure(self):
        """Check failure case of float out of range"""
        method = check_number_in_range(
            upper_bound=0, lower_bound=-1, accessor=lambda x: x.floating)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_non_numeric_failure(self):
        """Check failure case of non-numeric input"""
        method = check_number_in_range(
            upper_bound=10, lower_bound=0, accessor=lambda x: x.invalid)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_invalid_range(self):
        """Check failure case of invalid range"""
        with self.assertRaises(ValueError):
            check_number_in_range(upper_bound=0, lower_bound=1)

    def test_number_in_range_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_number_in_range(
            upper_bound=1, lower_bound=0, accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestNumberWithinAbsoluteTolerance(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()

    class Response(object):
        def __init__(self):
            self.integer = 7
            self.floating = 5.5
            self.invalid = 'invalid'

    def test_int_within_tolerance_success(self):
        """Check happy path for int"""
        method = check_number_within_absolute_tolerance(
            expected=6, tolerance=2, accessor=lambda x: x.integer)
        result = method(self.response)
        self.assertEqual(result, 7)

    def test_float_within_tolerance_success(self):
        """Check happy path for float"""
        method = check_number_within_absolute_tolerance(
            expected=5, tolerance=1, accessor=lambda x: x.floating)
        result = method(self.response)
        self.assertEqual(result, 5.5)

    def test_int_within_tolerance_failure(self):
        """Check failure case of int exceeding tolerance"""
        method = check_number_within_absolute_tolerance(
            expected=10, tolerance=1, accessor=lambda x: x.integer)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_float_within_tolerance_failure(self):
        """Check failure case of float exceeding tolerance"""
        method = check_number_within_absolute_tolerance(
            expected=10, tolerance=1, accessor=lambda x: x.floating)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_non_numeric_failure(self):
        """Check failure case of non-numeric input"""
        method = check_number_within_absolute_tolerance(
            expected=10, tolerance=0, accessor=lambda x: x.invalid)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_invalid_tolerance(self):
        """Check failure case of negative tolerance value"""
        with self.assertRaises(ValueError):
            check_number_within_absolute_tolerance(expected=10, tolerance=-1)

    def test_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_number_within_absolute_tolerance(
            expected=10, tolerance=1, accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)


class TestNumberWithinPercentTolerance(unittest.TestCase):
    def setUp(self):
        self.response = self.Response()
    
    class Response(object):
        def __init__(self):
            self.integer = 7
            self.floating = 5.5
            self.invalid = 'invalid'

    def test_int_within_tolerance_success(self):
        """Check happy path for int"""
        method = check_number_within_percent_tolerance(
            expected=6, tolerance=50.0, accessor=lambda x: x.integer)
        result = method(self.response)
        self.assertEqual(result, 7)

    def test_float_within_tolerance_success(self):
        """Check happy path for float"""
        method = check_number_within_percent_tolerance(
            expected=5, tolerance=50.0, accessor=lambda x: x.floating)
        result = method(self.response)
        self.assertEqual(result, 5.5)

    def test_int_within_tolerance_failure(self):
        """Check failure case of int exceeding tolerance"""
        method = check_number_within_percent_tolerance(
            expected=10, tolerance=1, accessor=lambda x: x.integer)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_float_within_tolerance_failure(self):
        """Check failure case of float exceeding tolerance"""
        method = check_number_within_percent_tolerance(
            expected=10, tolerance=1, accessor=lambda x: x.floating)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_non_numeric_failure(self):
        """Check failure case of non-numeric input"""
        method = check_number_within_percent_tolerance(
            expected=10, tolerance=10, accessor=lambda x: x.invalid)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)

    def test_invalid_tolerance(self):
        """Check failure case of negative tolerance value"""
        with self.assertRaises(ValueError):
            check_number_within_percent_tolerance(expected=10, tolerance=-1)

    def test_bad_accessor(self):
        """Check failure case of invalid accessor method"""
        method = check_number_within_percent_tolerance(
            expected=10, tolerance=1, accessor=lambda x: x.foo)
        result = method(self.response)
        self.assertIsInstance(result, wf.Error)
