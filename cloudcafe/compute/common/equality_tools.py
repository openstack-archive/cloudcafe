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

from datetime import timedelta


class EqualityTools:

    @classmethod
    def are_not_equal(expected, actual):
        return expected is not None and expected != actual

    @classmethod
    def are_lists_equal(expected, actual):
        if expected is None and actual is None:
            return True
        if expected is None or actual is None:
            return False
        if len(expected) != len(actual):
            return False
        for i in range(len(expected)):
            if not expected[i].equals(actual[i]):
                return False
        return True

    @classmethod
    def sanitized_dict(self, dict_to_sanitize={}, keys_not_to_include=[]):
        #make a shallow copy
        sanitized_dict = dict_to_sanitize.copy()
        for key in keys_not_to_include:
            try:
                del sanitized_dict[str(key)]
            except:
                continue
            return sanitized_dict

    @classmethod
    def are_objects_equal(cls, expected_object, actual_object,
                          keys_to_exclude=[]):

        if expected_object is None and actual_object is None:
            return True

        if expected_object is None or actual_object is None:
            return False

        for key, expected_value in expected_object.__dict__.items():
            if (key not in keys_to_exclude
                    and expected_value != actual_object.__dict__[key]):
                return False
        return True

    @classmethod
    def are_sizes_equal(cls, size1, size2, leeway):
        return abs(size1 - size2) <= leeway

    @classmethod
    def is_true(cls, value):
        return value is not None and (str(value) == '1'
                                      or str.lower(value) == 'true')

    @classmethod
    def are_datetimes_equal(cls, datetime1, datetime2,
                            leeway=timedelta(seconds=0)):
        return abs(datetime1 - datetime2) <= leeway
