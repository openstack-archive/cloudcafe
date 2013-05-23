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
from os import path
from json import dumps as dict_to_str, loads as str_to_dict
from cafe.engine.models.base import AutoMarshallingModel


class Secret(AutoMarshallingModel):

    def __init__(self, name, mime_type, expiration, algorithm, bit_length,
                 cypher_type, plain_text=None):
        super(Secret, self).__init__()

        self.name = name
        self.mime_type = mime_type
        self.expiration = expiration
        self.algorithm = algorithm
        self.bit_length = bit_length
        self.cypher_type = cypher_type
        self.plain_text = plain_text

    def _obj_to_json(self):
        return dict_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        """ This is a rather ugly way of doing this, but I need a quick way of
        making all of these optional
        """
        converted = {}
        if self.name is not None:
            converted['name'] = self.name
        if self.mime_type is not None:
            converted['mime_type'] = self.mime_type
        if self.expiration is not None:
            converted['expiration'] = self.expiration
        if self.algorithm is not None:
            converted['algorithm'] = self.algorithm
        if self.bit_length is not None:
            converted['bit_length'] = self.bit_length
        if self.cypher_type is not None:
            converted['cypher_type'] = self.cypher_type
        if self.plain_text is not None:
            converted['plain_text'] = self.plain_text

        return converted

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        """ This overridden by SecretMetadata """
        return Secret(**json_dict)


class SecretMetadata(Secret):

    def __init__(self, name, mime_type, expiration, algorithm, bit_length,
                 cypher_type, plain_text=None, status=None, updated=None,
                 created=None, secret_ref=None, content_types=None):
        super(SecretMetadata, self).__init__(name, mime_type, expiration,
                                             algorithm, bit_length,
                                             cypher_type, plain_text)
        self.status = status
        self.updated = updated
        self.created = created
        self.secret_ref = secret_ref

    def __eq__(self, other):
        return other.secret_ref == self.secret_ref

    def __ne__(self, other):
        return not self == other

    def get_id(self):
        ref_id = None
        if len(self.secret_ref) > 0:
            ref_id = path.split(self.secret_ref)[1]
        return ref_id

    def _obj_to_dict(self):
        converted = super(SecretMetadata, self)._obj_to_dict()

        if self.status is not None:
            converted['status'] = self.status
        if self.updated is not None:
            converted['updated'] = self.status
        if self.created is not None:
            converted['created'] = self.status
        if self.secret_ref is not None:
            converted['secret_ref'] = self.status

        return converted

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return SecretMetadata(**json_dict)


class SecretRef(AutoMarshallingModel):

    def __init__(self, reference):
        super(SecretRef, self).__init__()
        self.reference = reference

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return SecretRef(reference=json_dict.get('secret_ref'))


class UpdateSecret(AutoMarshallingModel):

    def __init__(self, plain_text):
        super(UpdateSecret, self).__init__()
        self.plain_text = plain_text

    def _obj_to_json(self):
        return dict_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        return {'plain_text': self.plain_text}


class SecretGroup(AutoMarshallingModel):

    def __init__(self, secrets, next_list=None, previous_list=None):
        super(SecretGroup, self).__init__()

        self.secrets = secrets
        self.next = next_list
        self.previous = previous_list

    def get_ids(self):
        return [sec.get_id() for sec in self.secrets]

    def get_next_query_data(self):
        matches = re.search('.*\?(.*?)\=(\d*)&(.*?)\=(\d*)', self.next)
        return {
            'limit': matches.group(2),
            'offset': matches.group(4)
        }

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        secrets, next_list, prev_list = [], None, None

        for secret_dict in json_dict.get('secrets'):
            secrets.append(SecretMetadata._dict_to_obj(secret_dict))

        if 'next' in json_dict:
            next_list = json_dict.get('next')
        if 'previous' in json_dict:
            prev_list = json_dict.get('previous')
        return SecretGroup(secrets, next_list, prev_list)
