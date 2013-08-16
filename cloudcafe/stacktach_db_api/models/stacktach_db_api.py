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

    def __init__(self, **kwargs):
        """
        An object that represents a Launch.
        """
        super(Launch, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))
        return "[{0}]".format(', '.join(values))

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
        if 'id' in launch_dict:
            launch_dict['id'] = launch_dict.get('id')
        if 'instance' in launch_dict:
            launch_dict['instance'] = launch_dict.get('instance')
        if 'instance_type_id' in launch_dict:
            launch_dict['instance_type_id'] = \
                launch_dict.get('instance_type_id')
        if 'launched_at' in launch_dict:
            launch_dict['launched_at'] = launch_dict.get('launched_at')
        if 'request_id' in launch_dict:
            launch_dict['swap'] = launch_dict.get('request_id')
        launch = Launch(**launch_dict)
        return launch


class Delete(AutoMarshallingModel):

    def __init__(self, **kwargs):
        """
        An object that represents a Delete.

        """
        super(Delete, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))
        return "[{0}]".format(', '.join(values))

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
        if 'deleted_at' in delete_dict:
            delete_dict['deleted_at'] = delete_dict.get('deleted_at')
        if 'id' in delete_dict:
            delete_dict['id'] = delete_dict.get('id')
        if 'instance' in delete_dict:
            delete_dict['instance'] = delete_dict.get('instance')
        if 'launched_at' in delete_dict:
            delete_dict['launched_at'] = delete_dict.get('launched_at')
        if 'raw' in delete_dict:
            delete_dict['raw'] = delete_dict.get('raw')
        delete = Delete(**delete_dict)
        return delete


class Exist(AutoMarshallingModel):

    def __init__(self, **kwargs):
        """
        An object that represents an Exist.

        """
        super(Exist, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))
        return "[{0}]".format(', '.join(values))

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
        if 'delete' in exist_dict:
            exist_dict['delete'] = exist_dict.get('delete')
        if 'deleted_at' in exist_dict:
            exist_dict['deleted_at'] = exist_dict.get('deleted_at')
        if 'id' in exist_dict:
            exist_dict['id'] = exist_dict.get('id')
        if 'instance' in exist_dict:
            exist_dict['instance'] = exist_dict.get('instance')
        if 'instance_type_id' in exist_dict:
            exist_dict['instance_type_id'] = exist_dict.get('instance_type_id')
        if 'launched_at' in exist_dict:
            exist_dict['launched_at'] = exist_dict.get('launched_at')
        if 'message_id' in exist_dict:
            exist_dict['message_id'] = exist_dict.get('message_id')
        if 'raw' in exist_dict:
            exist_dict['raw'] = exist_dict.get('raw')
        if 'status' in exist_dict:
            exist_dict['status'] = exist_dict.get('status')
        if 'usage' in exist_dict:
            exist_dict['usage'] = exist_dict.get('usage')
        exist = Exist(**exist_dict)
        return exist
