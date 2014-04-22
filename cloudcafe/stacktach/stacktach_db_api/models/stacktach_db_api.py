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

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel


class ServerLaunch(AutoMarshallingModel):

    def __init__(self, os_distro=None, os_version=None, instance_type_id=None,
                 instance_flavor_id=None, launched_at=None, instance=None,
                 os_architecture=None, request_id=None, rax_options=None,
                 id_=None, tenant=None):

        """An object that represents a Server Launch in Stacktach DB."""
        super(ServerLaunch, self).__init__()
        self.os_distro = os_distro
        self.os_version = os_version
        self.instance_type_id = instance_type_id
        self.instance_flavor_id = instance_flavor_id
        self.launched_at = launched_at
        self.instance = instance
        self.os_architecture = os_architecture
        self.request_id = request_id
        self.rax_options = rax_options
        self.id_ = id_
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
        if 'id' in launch_dict:
            launch_dict['id_'] = launch_dict.pop('id')
        launch = ServerLaunch(**launch_dict)
        return launch


class ServerLaunches(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get('launches'))

    @classmethod
    def _list_to_obj(cls, launch_dict_list):
        launches = ServerLaunches()
        launches.extend([ServerLaunch._dict_to_obj(launch)
                         for launch in launch_dict_list])
        return launches


class ServerDelete(AutoMarshallingModel):
    def __init__(self, raw=None, instance=None, deleted_at=None, id_=None,
                 launched_at=None):
        """An object that represents a Server Delete in Stacktach DB. """
        super(ServerDelete, self).__init__()
        self.raw = raw
        self.instance = instance
        self.deleted_at = deleted_at
        self.id_ = id_
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
        if 'id' in delete_dict:
            delete_dict['id_'] = delete_dict.pop('id')
        delete = ServerDelete(**delete_dict)
        return delete


class ServerDeletes(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get('deletes'))

    @classmethod
    def _list_to_obj(cls, delete_dict_list):
        deletes = ServerDeletes()
        deletes.extend([ServerDelete._dict_to_obj(delete)
                       for delete in delete_dict_list])
        return deletes


class ServerExist(AutoMarshallingModel):
    def __init__(self, status=None, os_distro=None, bandwidth_public_out=None,
                 received=None, instance_type_id=None, raw=None,
                 os_architecture=None, rax_options=None, deleted_at=None,
                 audit_period_beginning=None, audit_period_ending=None,
                 id_=None, tenant=None, fail_reason=None, instance=None,
                 instance_flavor_id=None, os_version=None, launched_at=None,
                 usage=None, message_id=None, send_status=None, delete=None,
                 event_id=None):
        """
        An object that represents a Server Exist in Stacktach DB.

        """
        self.status = status
        self.audit_period_beginning = audit_period_beginning
        self.os_distro = os_distro
        self.bandwidth_public_out = bandwidth_public_out
        self.usage = usage
        self.fail_reason = fail_reason
        self.raw = raw
        self.message_id = message_id
        self.received = received
        self.instance_type_id = instance_type_id
        self.instance_flavor_id = instance_flavor_id
        self.os_version = os_version
        self.launched_at = launched_at
        self.instance = instance
        self.os_architecture = os_architecture
        self.audit_period_ending = audit_period_ending
        self.rax_options = rax_options
        self.deleted_at = deleted_at
        self.send_status = send_status
        self.id_ = id_
        self.tenant = tenant
        self.delete = delete
        self.event_id = event_id

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
        if 'id' in exist_dict:
            exist_dict['id_'] = exist_dict.pop('id')
        exist = ServerExist(**exist_dict)
        return exist


class ServerExists(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get('exists'))

    @classmethod
    def _list_to_obj(cls, exist_dict_list):
        exists = ServerExists()
        exists.extend([ServerExist._dict_to_obj(exist)
                      for exist in exist_dict_list])
        return exists


class ImageUsage(AutoMarshallingModel):

    def __init__(self, id_=None, uuid=None, created_at=None, owner=None,
                 size=None, last_raw_id=None):
        """An object that represents a Image Usage in Stacktach DB."""
        self.id_ = id_
        self.uuid = uuid
        self.created_at = created_at
        self.owner = owner
        self.size = size
        self.last_raw_id = last_raw_id

    def __repr__(self):
        values = []
        for prop, value in self.__dict__.items():
            values.append("{0}: {1}".format(prop, value))
        return "image: [{0}]".format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a ImageUsage based on the json serialized_str
        passed in.
        """
        image_dict = json.loads(serialized_str)
        image = cls._dict_to_obj(image_dict)
        return image

    @classmethod
    def _dict_to_obj(cls, image_dict):
        """
        Helper method to turn dictionary into ImageUsage instance.
        """
        if 'id' in image_dict:
            image_dict['id_'] = image_dict.pop('id')
        image = ImageUsage(**image_dict)
        return image


class ImageUsages(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('images'))

    @classmethod
    def _list_to_obj(cls, image_dict_list):
        images = ImageUsages()
        images.extend([ImageUsage._dict_to_obj(image)
                      for image in image_dict_list])


class ImageDelete(AutoMarshallingModel):
    def __init__(self, id_=None, uuid=None, deleted_at=None, raw_id=None):
        """An object that represents a Image Delete in Stacktach DB."""
        super(ImageDelete, self).__init__()
        self.id_ = id_
        self.uuid = uuid
        self.deleted_at = deleted_at
        self.raw_id = raw_id

    def __repr__(self):
        values = []
        for prop, value in self.__dict__.items():
            values.append("{0}: {1}".format(prop, value))
        return "delete: [{0}]".format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an object of a Delete based on the json serialized_str
        passed in.
        """
        json_dict = json.loads(serialized_str)
        delete = cls._dict_to_obj(json_dict['delete'])
        return delete

    @classmethod
    def _dict_to_obj(cls, delete_dict):
        """
        Helper method to turn dictionary into ImageDelete instance.
        """
        if 'id' in delete_dict:
            delete_dict['id_'] = delete_dict.pop('id')
        delete = ImageDelete(**delete_dict)
        return delete


class ImageDeletes(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('deletes'))

    @classmethod
    def _list_to_obj(cls, delete_dict_list):
        deletes = ImageDeletes()
        deletes.extend([ImageDelete._dict_to_obj(delete)
                        for delete in delete_dict_list])


class ImageExist(AutoMarshallingModel):
    def __init__(self, id_=None, uuid=None, created_at=None,
                 deleted_at=None, audit_period_beginning=None,
                 audit_period_ending=None, status=None, fail_reason=None,
                 raw_id=None, usage_id=None, delete_id=None, send_status=None,
                 owner=None, size=None, message_id=None, event_id=None):
        """
        An object that represents a Image Exist in Stacktach DB.

        """
        self.id_ = id_
        self.uuid = uuid
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.audit_period_beginning = audit_period_beginning
        self.audit_period_ending = audit_period_ending
        self.status = status
        self.fail_reason = fail_reason
        self.raw_id = raw_id
        self.usage_id = usage_id
        self.delete_id = delete_id
        self.send_status = send_status
        self.owner = owner
        self.size = size
        self.message_id = message_id
        self.event_id = event_id

    def __repr__(self):
        values = []
        for prop, value in self.__dict__.items():
            values.append("{0}: {1}".format(prop, value))
        return "exist: [{0}]".format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of an ImageExist based on the json serialized_str
        passed in.
        """
        json_dict = json.loads(serialized_str)
        exist = cls._dict_to_obj(json_dict['exist'])
        return exist

    @classmethod
    def _dict_to_obj(cls, exist_dict):
        """
        Helper method to turn dictionary into ImageExist instance.
        """
        if 'id' in exist_dict:
            exist_dict['id_'] = exist_dict.pop('id')
        exist = ImageExist(**exist_dict)
        return exist


class ImageExists(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_string):
        json_dict = json.loads(serialized_string)
        return cls._list_to_obj(json_dict.get('exists'))

    @classmethod
    def _list_to_obj(cls, exist_dict_list):
        exists = ImageExists()
        exists.extend([ImageExist._dict_to_obj(exist)
                       for exist in exist_dict_list])
        return exists
