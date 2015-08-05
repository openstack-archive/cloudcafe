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
import os
import ast


def _get_cl_args():
    dict_string = '{}'
    data_dict = {}

    try:
        dict_string = os.environ['DICT_STRING']
    except KeyError:
        pass

    try:
        data_dict = ast.literal_eval(dict_string)
    except ValueError:
        pass
    except SyntaxError:
        pass

    return data_dict


def get_value(dict_key, default_value=None):
    data_dict = _get_cl_args()

    return data_dict.get(dict_key, default_value)
