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
import re

from cafe.engine.models.base import AutoMarshallingModel
from cafe.engine.models.base import AutoMarshallingListModel


class BaseBarbicanCLIModel(AutoMarshallingModel):
    """ Creating a custom AutoMarshallingModel due to the unique nature
    of the output for the Barbican command-line client"""

    marshal_type = 'cli_str'

    @classmethod
    def convert_cli_str_to_dict(cls, response_str):
        """ Cleans and converts a response chunk str from the cli interface
        into a dict that can be used for deserialization. """
        converted = {}
        lines = [line.strip() for line in response_str.splitlines()]
        if not lines:
            return converted

        # Clean the first line:
        match = re.search('(.*?)\s-\s(.*)', lines[0])
        if match:
            lines[0] = match.group(2)

        # Convert to key value pairs
        for line in lines:
            capture = re.match('(.*?):\s(.*)', line)
            key, value = capture.groups()
            key = key.replace(' ', '_')
            converted[key] = value

        return converted

    @classmethod
    def _cli_str_to_obj(cls, str_response):
        converted = cls.convert_cli_str_to_dict(str_response)
        return cls._dict_to_obj(converted)

    @classmethod
    def _dict_to_obj(cls, input_dict):
        raise NotImplementedError()


class BarbicanCLIListModel(AutoMarshallingListModel):
    MODEL_TYPE = None
    marshal_type = 'cli_str'

    def __init__(self, model_list=[]):
        super(BarbicanCLIListModel, self).__init__()
        self.extend(model_list)

    @classmethod
    def _cli_str_to_obj(cls, str_response):
        serialized_list = str_response.split('\n\n')
        serialized_list.pop(-1)
        models = [cls.MODEL_TYPE._cli_str_to_obj(serial_str)
                  for serial_str in serialized_list]
        return cls(model_list=models)


class SecretCLIModel(BaseBarbicanCLIModel):

    def __init__(self, name=None, content_types=None, algorithm=None,
                 bit_length=None, mode=None, expiration=None, created=None,
                 status=None, href=None):
        super(SecretCLIModel, self).__init__()
        self.name = name
        self.created = created
        self.status = status
        self.content_types = content_types
        self.algorithm = algorithm
        self.bit_length = bit_length
        self.mode = mode
        self.expiration = expiration
        self.href = href

    @classmethod
    def _dict_to_obj(cls, input_dict):
        return SecretCLIModel(**input_dict)


class OrderCLIModel(BaseBarbicanCLIModel):

    def __init__(self, order_href=None, secret_href=None, created=None,
                 status=None):
        super(OrderCLIModel, self).__init__()
        self.order_ref = order_href
        self.secret_ref = secret_href
        self.created = created
        self.status = status

    @classmethod
    def _dict_to_obj(cls, input_dict):
        return OrderCLIModel(**input_dict)


class SecretCLIListModel(BarbicanCLIListModel):
    MODEL_TYPE = SecretCLIModel


class OrderCLIListModel(BarbicanCLIListModel):
    MODEL_TYPE = OrderCLIModel
