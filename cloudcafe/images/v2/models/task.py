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

import dateutil.parser
import json

from cafe.engine.models.base import \
    AutoMarshallingListModel, AutoMarshallingModel
from cloudcafe.compute.common.equality_tools import EqualityTools


class Task(AutoMarshallingModel):
    """@summary: Task v2 model"""

    def __init__(self, expires_at=None, created_at=None, id_=None,
                 input_=None, message=None, owner=None, result=None,
                 schema=None, self_=None, status=None, type_=None,
                 updated_at=None):

        self.expires_at = expires_at
        self.created_at = created_at
        self.id_ = id_
        self.input_ = input_
        self.message = message
        self.owner = owner
        self.result = result
        self.schema = schema
        self.self_ = self_
        self.status = status
        self.type_ = type_
        self.updated_at = updated_at

    def __eq__(self, other):

        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):

        return not self.__eq__(other)

    def __repr__(self):

        values = []

        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))

        return '[{0}]'.format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):

        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):

        input_ = None
        result = None

        created_at = dateutil.parser.parse(json_dict.get('created_at'))
        expires_at = dateutil.parser.parse(json_dict.get('expires_at'))
        if 'input' in json_dict:
            input_ = Input._dict_to_obj(json_dict)
        if 'result' in json_dict:
            result = Result._dict_to_obj(json_dict)
        updated_at = dateutil.parser.parse(json_dict.get('updated_at'))

        task = Task(created_at=created_at, expires_at=expires_at,
                    id_=json_dict.get('id'), input_=input_,
                    owner=json_dict.get('owner'),
                    message=json_dict.get('message'), result=result,
                    schema=json_dict.get('schema'),
                    self_=json_dict.get('self'),
                    status=json_dict.get('status'),
                    type_=json_dict.get('type'), updated_at=updated_at)

        return task

    def _obj_to_json(self):

        obj_dict = {'created_at': self.created_at,
                    'expires_at': self.expires_at, 'id': self.id_,
                    'input': self.input_, 'message': self.message,
                    'owner': self.owner, 'result': self.result,
                    'schema': self.schema, 'self': self.self_,
                    'status': self.status, 'type': self.type_,
                    'updated_at': self.updated_at}

        obj_dict = self._remove_empty_values(obj_dict)

        return json.dumps(obj_dict)

    @classmethod
    def _xml_to_obj(cls):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')

    @classmethod
    def _obj_to_xml(cls):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')


class Tasks(AutoMarshallingListModel):
    """@summary: Tasks v2 model"""

    def __init__(self, tasks=None):
        super(Tasks, self).__init__()
        self.extend(tasks or [])

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('tasks'))

    @classmethod
    def _list_to_obj(cls, dict_list):
        tasks = Tasks()
        for task_dict in dict_list:
            tasks.append(Task._dict_to_obj(task_dict))
        return tasks


class Input(AutoMarshallingModel):
    """@summary: Input for Task v2 model"""

    def __init__(self, image_properties=None, import_from=None,
                 import_from_format=None):

        self.image_properties = image_properties
        self.import_from = import_from
        self.import_from_format = import_from_format

    def __eq__(self, other):

        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):

        return not self.__eq__(other)

    def __repr__(self):

        values = []

        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))

        return '[{0}]'.format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):

        json_dict = json.loads(serialized_str)

        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):

        image_properties = {}

        for key, value in json_dict['input']['image_properties'].items():
            image_properties.update({key: value})

        input_ = Input(
            image_properties=image_properties,
            import_from=json_dict['input'].get('import_from'),
            import_from_format=json_dict['input'].get('import_from_format'))

        return input_

    @classmethod
    def _xml_to_obj(cls):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')

    @classmethod
    def _obj_to_xml(cls):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')


class Result(AutoMarshallingModel):
    """@summary: Result for Task v2 model"""

    def __init__(self, image_id=None):

        self.image_id = image_id

    def __eq__(self, other):

        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):

        return not self.__eq__(other)

    @classmethod
    def _json_to_obj(cls, serialized_str):

        json_dict = json.loads(serialized_str)

        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):

        result = Result(image_id=json_dict['result'].get('image_id'))

        return result

    @classmethod
    def _xml_to_obj(cls):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')

    @classmethod
    def _obj_to_xml(cls):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')
