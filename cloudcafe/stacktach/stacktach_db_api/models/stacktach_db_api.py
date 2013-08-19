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
import xml.etree.ElementTree as ET

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel
from cloudcafe.compute.common.constants import Constants


class Launch(AutoMarshallingModel):

    def __init__(self, os_distro, os_version, instance_type_id,
                 launched_at, instance, os_architecture, request_id,
                 rax_options, id, tenant):
        """
        An object that represents a Launch.
        """
        super(Launch, self).__init__()
        self.os_distro = os_distro
        self.os_version = os_version
        self.instance_type_id = instance_type_id
        self.launched_at = launched_at
        self.instance = instance
        self.os_architecture = os_architecture
        self.request_id = request_id
        self.rax_options = rax_options
        self.id = id
        self.tenant = tenant

    def __repr__(self):
        values = []
        for prop, value in self.__dict__.items():
            values.append("{0}: {1}".format(prop, value))
        return "launch: [{0}]".format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a Launch based on the json serialized_str
        passed in.
        """
        json_dict = json.loads(serialized_str)
        launch = cls._dict_to_obj(json_dict['launch'])
        return launch

    @classmethod
    def _dict_to_obj(cls, launch_dict):
        """
        Helper method to turn dictionary into Launch instance.
        """
        launch = Launch(**launch_dict)
        return launch


class Launches(AutoMarshallingListModel):

    launch_type = Launch

    @classmethod
    def _json_to_obj(cls, serialized_string):
        print "in json to obj"
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get('launches'))

    @classmethod
    def _list_to_obj(cls, launch_dict_list):
        launches = Launches()
        for launch_dict in launch_dict_list:
            launch = cls.launch_type._dict_to_obj(launch_dict)
            launches.append(launch)
        return launches


class Delete(AutoMarshallingModel):

    def __init__(self, raw, instance, deleted_at, id, launched_at):
        """
        An object that represents a Delete.

        """
        super(Delete, self).__init__()
        self.raw = raw
        self.instance = instance
        self.deleted_at = deleted_at
        self.id = id
        self.launched_at = launched_at

    def __repr__(self):
        values = []
        for prop, value in self.__dict__.items():
            values.append("{0}: {1}".format(prop, value))
        return "delete: [{0}]".format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a Delete based on the json serialized_str
        passed in.
        """
        json_dict = json.loads(serialized_str)
        delete = cls._dict_to_obj(json_dict['delete'])
        return delete

    @classmethod
    def _dict_to_obj(cls, delete_dict):
        """
        Helper method to turn dictionary into Delete instance.
        """
        delete = Delete(**delete_dict)
        return delete


class Deletes(AutoMarshallingListModel):

    delete_type = Delete

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get('deletes'))

    @classmethod
    def _list_to_obj(cls, delete_dict_list):
        deletes = Deletes()
        for delete_dict in delete_dict_list:
            delete = cls.delete_type._dict_to_obj(delete_dict)
            deletes.append(delete)
        return deletes


class Exist(AutoMarshallingModel):

    def __init__(self, status, audit_period_beginning, os_distro, usage,
                 fail_reason, raw, message_id, received, instance_type_id,
                 os_version, launched_at, instance, os_architecture,
                 audit_period_ending, rax_options, deleted_at, send_status,
                 id, tenant, delete):
        """
        An object that represents an Exist.

        """
        self.status = status
        self.audit_period_beginning = audit_period_beginning
        self.os_distro = os_distro
        self.usage = usage
        self.fail_reason = fail_reason
        self.raw = raw
        self.message_id = message_id
        self.received = received
        self.instance_type_id = instance_type_id
        self.os_version = os_version
        self.launched_at = launched_at
        self.instance = instance
        self.os_architecture = os_architecture
        self.audit_period_ending = audit_period_ending
        self.rax_options = rax_options
        self.deleted_at = deleted_at
        self.send_status = send_status
        self.id = id
        self.tenant = tenant
        self.delete = delete

    def __repr__(self):
        values = []
        for prop, value in self.__dict__.items():
            values.append("{0}: {1}".format(prop, value))
        return "exist: [{0}]".format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of an Exist based on the json serialized_str
        passed in.
        """
        json_dict = json.loads(serialized_str)
        exist = cls._dict_to_obj(json_dict['exist'])
        return exist

    @classmethod
    def _dict_to_obj(cls, exist_dict):
        """
        Helper method to turn dictionary into Exist instance.
        """
        exist = Exist(**exist_dict)
        return exist


class Exists(AutoMarshallingListModel):

    exist_type = Exist

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get('exists'))

    @classmethod
    def _list_to_obj(cls, exist_dict_list):
        exists = Exists()
        for exist_dict in exist_dict_list:
            exist = cls.exist_type._dict_to_obj(exist_dict)
            exists.append(exist)
        return exists
