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

import json

from cafe.engine.models.base import (
    AutoMarshallingModel, AutoMarshallingListModel)


class DeserializationError(Exception):
    pass


class EventBaseModel(AutoMarshallingModel):
    """Base class for Event models

    This class provides default implementations for common
    model functionality. Child classes will need to
    override the kwarg_map and possibly the obj_model_key
    attributes. Additionally, models with submodels will
    need to override the _dict_to_obj method.

    Example:

        {
            "foo": {
                "key1": "value1",
                "key2": "value2",
                "id": "id_value"
            }
        }

        obj_model_key = 'foo'
        kwarg_map = {'key1': 'key1', 'key2': 'key2', 'id_': 'id'}

        (This mapping will generate: self.key1, self.key2, self.id_)
    """
    obj_model_key = None  # (Optional) Name of model's JSON schema
    kwarg_map = {}  # Mapping of JSON keys to model attribute names
    optional_kwargs = []  # (Optional) Model attributes that are not required
    strict_checking = True  # Raise exception for unexpected attributes if True

    def __init__(self, kwargs):
        super(EventBaseModel, self).__init__()

        # Set class attributes from input kwargs
        # Ignore "private" kwargs (e.g. _foo) and kwargs
        # matching existing attributes (allows overriding)
        for var in kwargs:
            if (var != 'self' and not var.startswith('_') and
                    not hasattr(self, var)):
                setattr(self, var, kwargs.get(var))

    @classmethod
    def _map_values_to_kwargs(cls, deserialized_obj):
        """Map input dict to class attributes"""

        cls._validate_attributes(deserialized_obj)

        kwargs = {}
        for local_kw, deserialized_obj_kw in cls.kwarg_map.iteritems():
            kwargs[local_kw] = deserialized_obj.get(deserialized_obj_kw, None)

        if not cls.strict_checking:
            for key in cls._extra_args:
                kwargs[key] = deserialized_obj[key]

        return cls(**kwargs)

    @classmethod
    def _validate_attributes(cls, deserialized_obj):
        """Validate expected deserialization"""

        expected = set(cls.kwarg_map.values())
        actual = set(deserialized_obj.keys())

        missing_args = list(expected.difference(actual))
        cls._extra_args = list(actual.difference(expected))

        # Don't validate optional parameters
        missing_args = [arg for arg in missing_args
                        if arg not in cls.optional_kwargs]
        cls._extra_args = [arg for arg in cls._extra_args
                           if arg not in cls.optional_kwargs]

        msg = ''
        if cls._extra_args and cls.strict_checking:
            msg = '{msg} Found unexpected attributes: {attrs}'.format(
                msg=msg, attrs=cls._extra_args)
        if missing_args:
            msg = '{msg} Missing expected attributes: {attrs}'.format(
                msg=msg, attrs=missing_args)

        if msg:
            raise DeserializationError(msg)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Deserialize a JSON string"""
        json_dict = json.loads(serialized_str)
        model_dict = json_dict.get(cls.obj_model_key) or json_dict
        return cls._dict_to_obj(model_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        """Default dict_to_obj implementation

        Default implementation works for simple cases. Override
        for instances with sub-models.
        """
        return cls._map_values_to_kwargs(json_dict)

    def is_empty(self):
        """Check if all object values are False

        Example:
            obj_json = {
                "foo": []
                "bar": 0
            }

            obj.foo = []
            obj.bar = 0
            # obj.is_empty() returns True
        """
        for key in self.kwarg_map.keys():
            value = getattr(self, key)

            # Recursively check sub-models
            if value:
                return value.is_empty() if hasattr(value, 'is_empty') else False

        return True


class EventBaseListModel(AutoMarshallingListModel):
    """Base class for Event list models

    This class provides default implementations for common
    list model functionality. Child classes will need to
    override the list_model_key and ObjectModel attributes.

    Example:

        {
            "foo": [
                {
                    "key1": "value1",
                    "key2": "value2"
                }
            ]
        }

        list_model_key = 'foo'
        ObjectModel = Foo
    """
    list_model_key = None  # Name of model's JSON array
    ObjectModel = None  # Name of model class for list elements

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Deserialize a JSON string"""
        json_dict = json.loads(serialized_str)

        cls._validate_attributes(json_dict)

        list_of_dicts = json_dict.get(cls.list_model_key)
        return cls._list_to_obj(list_of_dicts)

    @classmethod
    def _list_to_obj(cls, list_of_dicts):
        """Create list of objects from list of dicts"""
        obj_list = cls()
        for obj_dict in list_of_dicts:
            obj_list.append(cls.ObjectModel._dict_to_obj(obj_dict))
        return obj_list

    @classmethod
    def _validate_attributes(cls, json_dict):
        """Validate expected deserialization"""
        if len(json_dict) > 1:
            extras = [key for key in json_dict.keys()
                      if key != cls.list_model_key]

            raise DeserializationError(
                'Unexpected attributes in deserialized string: {0}'.format(
                    extras))

        elif len(json_dict) < 1:
            raise DeserializationError(
                'Missing expected attribute: {0}'.format(cls.list_model_key))
