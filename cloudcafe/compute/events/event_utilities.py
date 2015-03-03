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

import string

from cloudcafe.compute.events.pipeline_utilities import PipelineTask


def generate_field_validators(validator_params):
    """Generate pipeline tasks to validate dictionary fields

    Generate a list of validation PipelineTask objects based on
    a list of input tuples.

    Args:
        validator_params (list): List of tuples of the form
            (key, expected_value). The key can be for a nested value,
            in which case the full path is delimited with '/' chars.

    Returns:
        list: A list of PipelineTask objects that expect a 'payload'
            and check that the value corresponding to the provided
            key matches the expected value.

    Example:
        validator_params = [('a': 'Item 1'), ('b/c': 'Item 2')]
        payload = {
            'a': 'Item 1',
            'b': {'c': 'Item 2'}
            }
        This input would produce pipeline tasks that would
        successfully validate the payload.
    """
    validators = []

    for v in validator_params:
        field, expected = v

        def make_check(field, expected):
            class Check(PipelineTask):
                inputs = ['payload']

                @classmethod
                def task(cls, data):
                    value = _get_nested_dict_value(data['payload'], field)

                    if value == expected:
                        return cls.succeeded(data)
                    else:
                        msg = '{field} was {value}, expected {expected}'
                        return cls.failed(msg.format(
                            field=field, value=value, expected=expected))

            return Check

        check = make_check(field, expected)
        name = string.capwords(field, '_').replace('_', '')
        check.__name__ = 'Check{}'.format(name)

        validators.append(check)

    return validators


def _get_nested_dict_value(input_dict, key):

    parts = key.split('/')

    try:
        value = reduce(dict.__getitem__, parts, input_dict)
    except KeyError:
        value = None
    return value
