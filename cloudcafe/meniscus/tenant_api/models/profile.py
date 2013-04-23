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
from json import dumps as json_to_str, loads as str_to_json
from cafe.engine.models.base import AutoMarshallingModel


class UpdateProfile(AutoMarshallingModel):

    def __init__(self, name=None, producer_ids=None):
        super(UpdateProfile, self).__init__()

        if name is not None:
            self.name = name
        if producer_ids is not None:
            self.producer_ids = producer_ids

    def _obj_to_json(self):
        body = self._auto_to_dict()
        return json_to_str(body)


# Create requires all parameters, whereas update they are optional
class CreateProfile(UpdateProfile):

    def __init__(self, name, producer_ids):
        super(CreateProfile, self).__init__(name, producer_ids)


class Profile(AutoMarshallingModel):
    ROOT_TAG = 'profile'

    def __init__(self, name=None, id=None, event_producers=None):
        super(Profile, self).__init__()
        self.event_producers = event_producers
        self.id = id
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Profile(**json_dict)


class AllProfiles(AutoMarshallingModel):
    ROOT_TAG = 'profiles'

    def __init__(self):
        super(AllProfiles, self).__init__()

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)

        converted = []
        json_profile_list = json_dict.get(cls.ROOT_TAG)

        for json_profile in json_profile_list:
            profile = Profile._dict_to_obj(json_profile)
            converted.append(profile)

        return converted
