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


class VerificationRequest(AutoMarshallingModel):

    def __init__(self,
                 resource_action=None,
                 resource_ref=None,
                 impersonation_allowed=False,
                 resource_type=None):
        super(VerificationRequest, self).__init__()
        self.resource_action = resource_action
        self.resource_ref = resource_ref
        self.impersonation_allowed = impersonation_allowed
        self.resource_type = resource_type

    def get_id_from_ref(self, ref):
        """Returns id from reference."""
        ref_id = None
        if ref is not None and len(ref) > 0:
            ref_id = path.split(ref)[1]
        return ref_id

    def get_id(self):
        """Returns verification id."""
        return self.get_id_from_ref(ref=self.verification_ref)

    def _obj_to_json(self):
        the_dict = {
            'resource_action': self.resource_action,
            'resource_ref': self.resource_ref,
            'impersonation_allowed': self.impersonation_allowed,
            'resource_type': self.resource_type
        }
        return dict_to_str(the_dict)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        args = {
            'resource_action': json_dict.get('resource_action'),
            'resource_ref': json_dict.get('resource_ref'),
            'impersonation_allowed': json_dict.get('impersonation_allowed'),
            'resource_type': json_dict.get('resource_type')
        }
        return Verification(**args)


class Verification(AutoMarshallingModel):

    def __init__(self, status=None, updated=None, created=None,
                 resource_action=None, resource_ref=None,
                 impersonation_allowed=False, verification_ref=None,
                 is_verified=None, resource_type=None):
        super(Verification, self).__init__()
        self.status = status
        self.updated = updated
        self.created = created
        self.resource_action = resource_action
        self.resource_ref = resource_ref
        self.impersonation_allowed = impersonation_allowed
        self.verification_ref = verification_ref
        self.is_verified = is_verified
        self.resource_type = resource_type

    def get_id_from_ref(self, ref):
        """Returns id from reference."""
        ref_id = None
        if ref is not None and len(ref) > 0:
            ref_id = path.split(ref)[1]
        return ref_id

    def get_id(self):
        """Returns verification id."""
        return self.get_id_from_ref(ref=self.verification_ref)

    def _obj_to_json(self):
        return dict_to_str(self._obj_to_dict())

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        args = {
            'status': json_dict.get('status'),
            'updated': json_dict.get('updated'),
            'created': json_dict.get('created'),
            'resource_action': json_dict.get('resource_action'),
            'resource_ref': json_dict.get('resource_ref'),
            'impersonation_allowed': json_dict.get('impersonation_allowed'),
            'verification_ref': json_dict.get('verification_ref'),
            'is_verified': json_dict.get('is_verified'),
            'resource_type': json_dict.get('resource_type')
        }
        return Verification(**args)


class VerificationRef(AutoMarshallingModel):

    def __init__(self, reference):
        super(VerificationRef, self).__init__()
        self.reference = reference

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return VerificationRef(reference=json_dict.get('verification_ref'))


class VerificationGroup(AutoMarshallingModel):

    def __init__(self, verifications, next_list=None, previous_list=None):
        super(VerificationGroup, self).__init__()

        self.verifications = verifications
        self.next = next_list
        self.previous = previous_list

    def get_ids(self):
        return [verification.get_id() for verification in self.verifications]

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
        verifications, next_list, prev_list = [], None, None

        for verification_dict in json_dict.get('verifications'):
            verifications.append(Verification._dict_to_obj(verification_dict))

        if 'next' in json_dict:
            next_list = json_dict.get('next')
        if 'previous' in json_dict:
            prev_list = json_dict.get('previous')
        return VerificationGroup(verifications, next_list, prev_list)
