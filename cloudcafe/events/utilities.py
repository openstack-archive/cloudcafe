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

from functools import wraps


class Result(object):
    """Result type for use in validation pipeline

    This type is the interchange format used by validators
    in the validation pipeline. This type functionally behaves
    as a union type that is switched based on the success
    attribute. If success is True, the payload will be
    the input data to the validator. If success is False,
    the payload will be the error data produced by
    validation.
    """
    def __init__(self, success=False, payload=None):
        self.success = success
        self.payload = payload

    def __repr__(self):
        status = 'Success' if self.success else 'Failure'
        return '{status}: {payload}'.format(status=status,
                                            payload=self.payload)


def box_data(data):
    """Box input data for validators

    This method 'boxes' data into the Result type
    needed by bound validator methods.

    Args:
        message: Input data for validators

    Returns:
        Result: A Result object encapsulating the input data
    """
    return Result(True, data)


def bind(method):
    """Bind a validator method for use in a pipeline

    This method adapts a validator method to work
    in a validation pipeline. Specifically, it
    routes successful Result input to the validation
    logic, and passes through failure Result without
    performing any additional actions.

    Example:
                             <Before bind>
                                              ---> Result(Success)
                             -------------    |
                        data |           |    |
                        ---> | Validator | ---|
                             |           |    |
                             -------------    |
                                              ---> Result(Failure)

    ==============================================================

                             <After bind>
                                              ---> Result(Success)
                             -------------    |
                        data |           |    |
        Result(Success) ---> | Validator | ---|
                             |           |    |
                             -------------    |
        Result(Failure) -------------------------> Result(Failure)
    """
    @wraps(method)
    def inner(result):
        if result.success:
            return method(result.payload)
        else:
            return result
    return inner


def validator_and(s1, s2=None):
    """Combine Result objects using AND logic

    This method combines Result objects using
    boolean AND logic. This is useful for combining
    the results of a batch validators run in parallel.

    Note:
        This method can be used in conjunction with
        the 'reduce' method to process a list of
        validators (checks).

    Example:

        V1<Success>
             *
        V2<Success>   ==>   Result<Success>
             *
        V3<Success>

        ====================================

        V1<Failure>
             *
        V2<Failure>   ==>   Result<Failure>
             *              (Combined V1/V2 payload)
        V3<Success>

        ====================================
        data = Result(...)
        checks = [V1, V2, V3]
        reduce(validator_and, [check(data) for check in checks])
    """
    if not s2:
        return s1

    if s1.success and s2.success:
        return Result(True, s1.payload)

    elif s1.success and not s2.success:
        return Result(False, s2.payload)

    elif not s1.success and s2.success:
        return Result(False, s1.payload)

    else:
        payload = dict(s1.payload, **s2.payload)
        return Result(False, payload)


def validator_or(s1, s2=None):
    """Combine Result objects using OR logic

    This method combines Result objects using
    boolean OR logic. This is useful for special cases
    where multiple valid options are possible. For example,
    two validators could check the same metadata field for
    a different value, but either option is a valid choice.

    Note:
        This method can be used in conjunction with
        the 'reduce' method to process a list of
        validators (checks).

    Note:
        Warning!! Error messages from failed validators will
        be discarded if any of the validators in this batch
        are successful.


    Example:

        V1<Failure>
             +
        V2<Failure>   ==>   Result<Failure>
             +              (Combined V1/V2/V3 payload)
        V3<Failure>

        ====================================

        V1<Failure>
             +
        V2<Success>   ==>   Result<Success>
             +              (**V1 payload discarded**)
        V3<Success>

        ====================================
        data = Result(...)
        checks = [V1, V2, V3]
        reduce(validator_or, [check(data) for check in checks])
    """
    if not s2:
        return s1

    if s1.success or s2.success:
        return Result(True, s1.payload)

    else:
        payload = dict(s1.payload, **s2.payload)
        return Result(False, payload)


def process_sequential(checks, data):
    """Process a list of validators sequentially

    This method processes a list of validators in sequence,
    and returns the overall result. If any validation in
    the sequence fails, any remaining validators will be
    bypassed.

    Args:
        checks (list): List of bound validators
        data (Result): 'Boxed' data input for validators

    Returns:
        Result: Result of all validations
    """
    for check in checks:
        data = check(data)

    return data


def process_parallel_and(checks, data):
    """Process a list of validators in parallel

    This method processes a list of validators and then
    combines the results using boolean AND logic

    Args:
        checks (list): List of bound validators
        data (Result): 'Boxed' data input for validators

    Returns:
        Result: Combined result of all validations
    """
    return reduce(validator_and, [check(data) for check in checks])


def process_parallel_or(checks, data):
    """Process a list of validators in parallel

    This method processes a list of validators and then
    combines the results using boolean OR logic

    Args:
        checks (list): List of bound validators
        data (Result): 'Boxed' data input for validators

    Returns:
        Result: Combined result of all validations
    """
    return reduce(validator_or, [check(data) for check in checks])
