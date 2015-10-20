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

import re
import urlparse
from numbers import Number

from IPy import IP
import dateutil.parser

import raxcafe.common.workflow.base as wf


def api_call(client_method):
    """Generate a method to make API calls.

    This method generates a closure that sets the API method
    that will be called. The generated method will be named
    according to the provided method name.

    Args:
        client_method (function): API method to be called.

    Returns:
        function: Renamed function closure.
    """
    method_name = 'API Call: {0}'.format(client_method.__name__)

    def method(kwargs):
        """Make an API call with provided arguments.

        Args:
            kwargs (dict): Dict of arguments used by the API method.

        Returns:
            Response from the API call or an Error object if the
            call raised an exception.
        """
        try:
            response = client_method(**kwargs)
        except Exception as e:
            return wf.Error(expected='Response object', actual='Exception',
                            message='API call failed: {0}'.format(e))

        return response

    method.__name__ = method_name
    return method


def check_response_code(expected, accessor=lambda x: x.status_code):
    """Generate a method to check a response code.

    This method generates a closure that checks a response code
    against an expected value. The generated method will be
    named according to the provided response code.

    Args:
        expected (int): Expected response code.

        accessor (Optional[function]): Function that returns the
            status code given a Response object.

    Returns:
        function: Renamed function closure.
    """
    method_name = 'check_response_code_is_{0}'.format(expected)

    def method(response):
        """Check that a response code matches the expected value.

        Args:
            response (Response): The response object to check.

        Returns:
            Response object that was provided or an Error object
            if the response code did not match the expected value
            or if the accessor method failed.
        """
        try:
            actual = accessor(response)
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return status_code'
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        if actual != expected:
            return wf.Error(expected=expected, actual=actual)

        return response

    method.__name__ = method_name
    return method


def check_item_in_iterable(expected_item):
    """Generate a method to check if an item is in an iterable.

    Note:
        If the iterable is a dictionary, the builtin behavior is to check if a
        value is in the dictionaries values.
        I.e., expected_item in dict.values()

    Args:
        expected (anything): Expected value.

    Returns:
        Input value or Error object if the value was not contained in the list.
    """
    method_name = 'check_{0}_in_iterable'.format(expected_item)

    def method(iterable):

        if expected_item not in iterable:
            return wf.Error(
                expected=expected_item, actual=iterable,
                message='The expected item was not present in the iterable.')

        return iterable

    method.__name__ = method_name
    return method


def check_item_is_uuid(item_name, accessor=None):
    """Generate a method to check if an item is a valid UUID.

    This method generates a closure that checks if an item is
    a valid UUID. The generated method will be named
    according to the provided method name.

    Args:
        item_name (str): Name of the item to check.

        accessor (Optional[function]): Function that returns the
            item to check given an enclosing object.

    Returns:
        function: Renamed function closure.
    """
    method_name = 'check_{0}_is_valid_uuid'.format(item_name)
    uuid_regex = re.compile(
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

    def method(item):
        """Check that an item is a valid UUID.

        Args:
            item (object): Object to compare to the expected value.

        Returns:
            Item that was provided or an Error object if the item
            was not a valid UUID or if the accessor method failed.
        """
        try:
            actual = accessor(item) if accessor else item
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return {0}'.format(item_name)
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        if not uuid_regex.match(actual.lower()):
            return wf.Error(expected='Valid UUID', actual=actual)

        return item

    method.__name__ = method_name
    return method


def check_item_is_instance_of(item_name, expected_type, accessor=None,
                              optional=False):
    """Generate a method to check if an item is of a specified type.

    This method generates a closure that checks if an item is
    an instance of the expected type. The generated method will
    be named according to the provided method name.

    Args:
        item_name (str): Name of the item to check.

        expected_type (class): Expected type of the item.

        accessor (Optional[function]): Function that returns the
            item to check given the enclosing object.

        optional (Optional[bool]): Item can also be None if True, but
            must be of the expected type if False.

    Returns:
        function: Renamed function closure.
    """
    optional_str = ' (or None)' if optional else ''
    method_name = 'check_{name}_is_instance_of_{expected}{optional}'.format(
        optional=optional_str, name=item_name, expected=expected_type)

    def method(item):
        """Check that an item is an instance of the expected type.

        Args:
            item (object): Object to check for expected type.

        Returns:
            Item that was provided or an Error object if the item
            was not of the expected type or if the accessor method
            failed.
        """
        try:
            actual = accessor(item) if accessor else item
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return {0}'.format(item_name)
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        if not isinstance(actual, expected_type):
            if optional and actual is None:
                pass
            else:
                err_actual = '{type} -- value: {value}'.format(
                    type=type(actual), value=actual)
                return wf.Error(expected=expected_type, actual=err_actual)

        return item

    method.__name__ = method_name
    return method


def check_item_is_valid_ip_address(item_name, accessor=None, optional=False):
    """Generate a method to check if an item is a valid IP address.

    This method generates a closure that checks if an item is
    a valid IP address. The generated method will be named according
    to the provided method name.

    Args:
        item_name (str): Name of the item to check.

        accessor (Optional[function]): Function that returns the
            item to check given the enclosing object.

        optional (Optional[bool]): Item can also be None if True, but
            must be a valid IP address if False.

    Returns:
        function: Renamed function closure
    """
    optional_str = ' (or None)' if optional else ''
    method_name = 'check_{name}_is_valid_ip_address{optional}'.format(
        name=item_name, optional=optional_str)

    def method(item):
        """Check that an item is a valid IP address.

        Args:
            item (object): Object that should be a valid IP address.

        Returns:
            Item that was provided or an Error object if the item
            was not a valid IP address or if the accessor method
            failed.
        """
        try:
            actual = accessor(item) if accessor else item
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return {0}'.format(item_name)
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)
        try:
            IP(actual)
        except Exception:
            if optional and actual is None:
                pass
            else:
                return wf.Error(expected='Valid IP Address', actual=actual)

        return item

    method.__name__ = method_name
    return method


def check_item_is_valid_datetime(item_name, accessor=None):
    """Generate a method to check if an item is a valid datetime.

    This method generates a closure that checks if an item is
    a valid datetime. The generated method will be named according
    to the provided method name.

    Args:
        item_name (str): Name of the item to check.

        accessor (Optional[function]): Function that returns the
            item to check given the enclosing object.

    Returns:
        function: Renamed function closure
    """
    method_name = 'check_{0}_is_valid_datetime'.format(item_name)

    def method(response):
        """Check that an item is a valid datetime.

        Args:
            item (object): Object that should be a valid datetime.

        Returns:
            Item that was provided or an Error object if the item
            was not a valid datetime or if the accessor method
            failed.
        """
        try:
            actual = accessor(response) if accessor else response
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return {0}'.format(item_name)
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        try:
            dateutil.parser.parse(actual)
        except Exception:
            return wf.Error(expected='Valid datetime string', actual=actual)

        return response

    method.__name__ = method_name
    return method


def check_item_is_valid_url(item_name, accessor=None):
    """Generate a method to check if an item is a valid URL.

    This method generates a closure that checks if an item is
    a valid URL. The generated method will be named according
    to the provided method name.

    Args:
        item_name (str): Name of the item to check.

        accessor (Optional[function]): Function that returns the
            item to check given the enclosing object.

    Returns:
        function: Renamed function closure
    """
    method_name = 'check_{0}_is_valid_url'.format(item_name)

    def method(response):
        """Check that an item is a valid URL.

        Args:
            item (object): Object that should be a valid URL.

        Returns:
            Item that was provided or an Error object if the item
            was not a valid URL or if the accessor method failed.
        """
        try:
            actual = accessor(response) if accessor else response
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return {0}'.format(item_name)
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        try:
            parsed = urlparse.urlparse(actual)
        except Exception:
            return wf.Error(expected='Valid URL', actual=actual)

        if not parsed.netloc:
            return wf.Error(expected='Valid URL', actual=actual)

        return response

    method.__name__ = method_name
    return method


def check_iterable(validator, obj_name, accessor=None, name_accessor=None):
    """Generate a method to apply a validator to items in an iterable.

    This method generates a closure that applies a validator to items
    in an iterable. The generated method will be named according
    to the provided object name.

    Args:
        validator (WorkflowRunner): Validator to apply to each item.

        obj_name (str): Name of the iterable to check.

        accessor (Optional[function]): Function that returns the
            iterable given the enclosing object.

        name_accessor (Optional[function]): Function that returns a
            name for an item in the iterable given the item.

    Returns:
        function: Renamed function closure
    """
    method_name = 'check_iterable_of_{0}'.format(obj_name)

    def method(data):
        """Apply validator to items in iterable.

        Args:
            data (object): Iterable object of items to validate.

        Returns:
            ParallelWorkflow: Results of validation. Each item in the
                iterable will be validated, and this result contains
                the aggregate.
        """
        try:
            items = accessor(data) if accessor else data
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return {0}'.format(obj_name)
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        results = []
        description = validator.description
        for item in items:
            v = validator
            task_name = name_accessor(item) if name_accessor else item
            v.description = '{0} -- {1}'.format(description, task_name)
            val = items[item] if isinstance(items, dict) else item
            result, _ = v.run(val, log_result=False)
            results.append(result)

        validator.description = description
        workflow_name = 'Check {0}'.format(obj_name)
        return wf.ParallelWorkflow(workflow_name, results), data

    method.__name__ = method_name
    return method


def extract_item(item_name, accessor):
    """Generate a method to extract an item from an object.

    This method generates a closure that extracts and returns an
    item from an object. The generated method will be named
    according to the provided item name.

    Args:
        item_name (str): Name of the item to extract.

        accessor (Optional[function]): Function that returns the
            item given the enclosing object.

    Returns:
        function: Renamed function closure
    """
    method_name = 'extract_{0}_from_workflow_data'.format(item_name)

    def method(data):
        """Extract and return an item.

        Args:
            data (object): Object enclosing the item to extract.

        Returns:
            Extracted item or Error object if the extraction failed.
        """
        try:
            item = accessor(data)
        except (AttributeError, TypeError) as e:
            return wf.Error(expected='Extracted item',
                            actual='Extraction failed', message=e)

        return item

    method.__name__ = method_name
    return method


def extract_item_to_kwargs(item_name, accessor):
    """Generate a dictionary with the item_name as the key.

     This method will use the accessor function to pull out the value that
     will be stored for the item_name key.

    :item_name: A string representation of the item name that will be used
                to extract the value form an object. It will also serve as the
                key for the kwargs that will be returned by the function
                closure.

    :param accessor: Function that will extract the desired entity from the
                     current workflow data object.

    :return: A function that will process the workflow data object that is
             active when this method is called.

    :rtype: function that creates and returns a keyword arguments dictionary.
    """

    method_name = 'extract_{0}_to_kwargs_from_workflow_data'.format(item_name)

    get_item = extract_item(item_name, accessor)

    def method(data):
        """ Extract a value and combine it with item_name to create a kwargs.

        :param data: The object that contains the value to be extracted by the
                     accessor function.

        :return: A keyword arguments object using the item_name as a key and the
                 object returned by the accessor as the value.

        :rtype: keyword arguments dictionary
        """
        try:
            item = get_item(data)

            # If there was a workflow error returned by get_item there
            # is no need to continue processing.  Signal the workflow to move
            # on.
            if isinstance(item, wf.Error):
                return item

        except (AttributeError, TypeError) as e:
            print "Error extracting item for kwargs: {0}: {1}".format(item_name, e)
            return wf.Error(expected='Extracted item to kwargs',
                            actual='Extraction failed', message=e)

        return {item_name: item}

    method.__name__ = method_name
    return method


def check_number_in_range(upper_bound, lower_bound, accessor=None):
    """Generate a method to check if a number is in a specified range.

    This method generates a closure that checks if an input value is
    a number is in a specified range. The generated method will be
    named according to the provided range's bounds.

    Args:
        upper_bound (Number): Upper bound of the range.

        lower_bound (Number): Lower bound of the range.

        accessor(Optional[function]): Function that returns the
            item given the enclosing object.

    Returns:
        Input value or Error object if the value was not in the
        specified range.
    """
    if lower_bound >= upper_bound:
        raise ValueError('Lower bound must be less than upper bound')

    method_name = ('check_number_in_range_'
                   '{lower} <= number <= {upper}').format(upper=upper_bound,
                                                          lower=lower_bound)

    def method(value):
        try:
            value = accessor(value) if accessor else value
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return value'
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        if not isinstance(value, Number):
            return wf.Error(expected='<numeric type>', actual=value)

        if not (lower_bound <= value <= upper_bound):
            expected_str = '{lower} <= number <= {upper}'.format(
                lower=lower_bound, upper=upper_bound)
            return wf.Error(expected=expected_str, actual=value)

        return value

    method.__name__ = method_name
    return method


def check_number_within_absolute_tolerance(expected, tolerance, accessor=None):
    """Generate a method to check if number is within specified tolerance.

    This method generates a closure that checks if an input value is
    a number within an absolute tolerance range. The generated method
    will be named according to the expected value and tolerance.

    Args:
        expected (Number): Expected value.

        tolerance (Number): Maximum acceptable tolerance from the expected
            value specified as an absolute quantity.

        accessor (Optional[function]): Function that returns the
            item given the enclosing object.

    Returns:
        Input value or Error object if the value was not within the
        specified tolerance range.
    """
    if tolerance < 0:
        raise ValueError('Tolerance value must be > 0.')

    method_name = ('check_number_within_tolerance '
                   '{expected}+/-{tolerance}').format(expected=expected,
                                                      tolerance=tolerance)

    def method(value):
        try:
            value = accessor(value) if accessor else value
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return value'
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        if not isinstance(value, Number):
            return wf.Error(expected='<numeric type>', actual=value)

        upper_bound = expected + tolerance
        lower_bound = expected - tolerance

        if not (lower_bound <= value <= upper_bound):
            expected_str = '{lower} <= number <= {upper}'.format(
                lower=lower_bound, upper=upper_bound)
            return wf.Error(expected=expected_str, actual=value)

        return value

    method.__name__ = method_name
    return method


def check_number_within_percent_tolerance(expected, tolerance, accessor=None):
    """Generate a method to check if number is within specified tolerance.

    This method generates a closure that checks if an input value is
    a number within a percentage range of an expected value.
    The generated method will be named according to the expected
    value and tolerance.

    Args:
        expected (Number): Expected value.

        tolerance (Number): Maximum acceptable tolerance from the expected
            value specified as percent value between 0 and 100.

        accessor (Optional[function]): Function that returns the
            item given the enclosing object.

    Returns:
        Input value of Error object if the value was not within the
        specified tolerance range.
    """
    if not (0 <= tolerance <= 100):
        raise ValueError('Tolerance value must be in range 0..100')

    method_name = ('check_number_within_tolerance '
                   '{expected}+/-{tolerance}%').format(expected=expected,
                                                       tolerance=tolerance)

    def method(value):
        try:
            value = accessor(value) if accessor else value
        except (AttributeError, TypeError) as e:
            err_expected = 'Provided accessor to return value'
            err_actual = 'Provided accessor method failed'
            return wf.Error(expected=err_expected, actual=err_actual, message=e)

        if not isinstance(value, Number):
            return wf.Error(expected='<numeric type>', actual=value)

        multiplier = tolerance / 100.0
        upper_bound = expected + (multiplier * expected)
        lower_bound = expected - (multiplier * expected)

        if not (lower_bound <= value <= upper_bound):
            expected_str = '{lower} <= number <= {upper}'.format(
                lower=lower_bound, upper=upper_bound)
            return wf.Error(expected=expected_str, actual=value)

        return value

    method.__name__ = method_name
    return method
