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

from cafe.engine.models.base import AutoMarshallingModel
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
        # One or more launches will be a list
        if 'launches' in json_dict.keys():
            launches = []
            for launch_dict in json_dict['launches']:
                launch = cls._dict_to_obj(launch_dict)
                launches.append(launch)
            return launches

    @classmethod
    def _dict_to_obj(cls, launch_dict):
        """
        Helper method to turn dictionary into Launch instance.
        """
        launch = Launch(**launch_dict)
        return launch

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        Returns an instance of a Launch based on the xml serialized_str
        passed in.
        """
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'launches':
            launches = []
            for launch in element.findall('launch'):
                launch = cls._xml_ele_to_obj(launch)
                launches.append(launch)
            return launches

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        Helper method to turn ElementTree instance to Launch instance.
        """
        launch_dict = element.attrib
        launch = Launch(**launch_dict)
        return launch


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
        # One or more deletes will be a list
        if 'deletes' in json_dict.keys():
            deletes = []
            for delete_dict in json_dict['deletes']:
                delete = cls._dict_to_obj(delete_dict)
                deletes.append(delete)
            return deletes

    @classmethod
    def _dict_to_obj(cls, delete_dict):
        """
        Helper method to turn dictionary into Delete instance.
        """
        delete = Delete(**delete_dict)
        return delete

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        Returns an instance of a Delete based on the xml serialized_str
        passed in.
        """
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'deletes':
            deletes = []
            for delete in element.findall('delete'):
                delete = cls._xml_ele_to_obj(delete)
                deletes.append(delete)
            return deletes

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        Helper method to turn ElementTree instance to Delete instance.
        """
        delete_dict = element.attrib
        delete = Delete(**delete_dict)
        return delete


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
        ''' One or more exists will be a list'''
        if 'exists' in json_dict.keys():
            exists = []
            for exist_dict in json_dict['exists']:
                exist = cls._dict_to_obj(exist_dict)
                exists.append(exist)
            return exists

    @classmethod
    def _dict_to_obj(cls, exist_dict):
        """
        Helper method to turn dictionary into Exist instance.
        """
        exist = Exist(**exist_dict)
        return exist

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        Returns an instance of a Exist based on the xml serialized_str
        passed in.
        """
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'exists':
            exists = []
            for exist in element.findall('exist'):
                exist = cls._xml_ele_to_obj(exist)
                exists.append(exist)
            return exists

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        Helper method to turn ElementTree instance to Exist instance.
        """
        exist_dict = element.attrib
        exist = Exist(**exist_dict)
        return exist
