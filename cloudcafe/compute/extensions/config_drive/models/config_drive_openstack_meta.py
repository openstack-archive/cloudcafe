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

import json

from cafe.engine.models.base import AutoMarshallingModel


class OpenStackMeta(AutoMarshallingModel):

    def __init__(self, availability_zone=None, hostname=None,
                 launch_index=None, name=None, admin_pass=None,
                 uuid=None, files=None, public_keys=None, meta=None):
        self.availability_zone = availability_zone
        self.hostname = hostname
        self.launch_index = launch_index
        self.name = name
        self.admin_pass = admin_pass
        self.uuid = uuid
        self.files = files
        self.public_keys = public_keys
        self.meta = meta

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        open_meta = cls._dict_to_obj(json_dict)
        return open_meta

    @classmethod
    def _dict_to_obj(cls, json_dict):
        openstack_meta = OpenStackMeta(
            availability_zone=json_dict.get('availability_zone'),
            hostname=json_dict.get('hostname'),
            admin_pass=json_dict.get('admin_pass'),
            launch_index=json_dict.get('launch_index'),
            name=json_dict.get('name'), meta=json_dict.get('meta'),
            public_keys=json_dict.get('public_keys'),
            uuid=json_dict.get('uuid'))
        if 'files' in json_dict:
            openstack_meta.files = Files._dict_to_obj(json_dict)
        if 'public_keys' in json_dict:
            openstack_meta.public_keys = Keys._dict_to_obj(json_dict)
        return openstack_meta


class File(AutoMarshallingModel):

    def __init__(self, content_path, path):

        super(File, self).__init__()
        self.content_path = content_path
        self.path = path

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a File based on the json serialized_str
        passed in.
        """

        json_dict = json.loads(serialized_str)
        file = cls._dict_to_obj(json_dict)
        return file

    @classmethod
    def _dict_to_obj(cls, file_dict):
        """Helper method to turn dictionary into File instance."""
        file = File(content_path=file_dict.get('content_path'),
                    path=file_dict.get('path'))
        return file


class Files(AutoMarshallingModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a Files based on the json serialized_str
        passed in.
        """
        json_dict = json.loads(serialized_str)
        files = cls._dict_to_obj(json_dict)
        return files

    @classmethod
    def _dict_to_obj(cls, file_dict):
        """Helper method to turn dictionary into Files instance."""
        files = []
        for file_dict in file_dict['files']:
            file = File._dict_to_obj(file_dict)
            files.append(file)
        return files


class Keys(AutoMarshallingModel):

    def __init__(self, ssh_keys):

        super(Keys, self).__init__()
        for key_name in ssh_keys:
            setattr(self, key_name, ssh_keys[key_name])

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a Key based on the json serialized_str
        passed in.
        """

        json_dict = json.loads(serialized_str)
        key = cls._dict_to_obj(json_dict)
        return key

    @classmethod
    def _dict_to_obj(cls, key_dict):
        """Helper method to turn dictionary into Key instance."""
        if 'public-keys' in key_dict:
            keys = Keys(ssh_keys=key_dict.get('public-keys')['0'])
        if 'public_keys' in key_dict:
            keys = Keys(ssh_keys=key_dict.get('public_keys'))
        return keys
