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
import re

from cafe.engine.models.base import AutoMarshallingModel


class BaseBarbicanCLIModel(AutoMarshallingModel):
    """ Creating a custom AutoMarshallingModel due to the unique nature
    of the output for the Barbican command-line client"""

    marshal_type = 'str'

    @classmethod
    def deserialize(cls, serialized_str):
        return super(BaseBarbicanCLIModel, cls).deserialize(serialized_str,
                                                            cls.marshal_type)

    @classmethod
    def serialize(cls):
        return super(BaseBarbicanCLIModel, cls).serialize(cls.marshal_type)

    @classmethod
    def convert_cli_str_to_dict(cls, response_str):
        """ Cleans and converts a response chunk str from the cli interface
        into a dict that can be used for deserialization. """
        converted = {}
        lines = [line.strip() for line in response_str.splitlines()]
        if not lines:
            return converted

        # Clean the first line:
        match = re.search('(.*?)\s-\s(.*)', line[0])
        if match:
            line[0] = match.group(2)

        # Convert to key value pairs
        for line in lines:
            key, value = line.split(': ')
            key = key.replace(' ', '_')
            converted[key] = value

        return converted


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
    def _str_to_obj(cls, str_response):
        secret_dict = cls.convert_cli_str_to_dict(str_response)
        return cls._dict_to_obj(secret_dict)

    @classmethod
    def _dict_to_obj(cls, secret_dict):
        return SecretCLIModel(**secret_dict)
