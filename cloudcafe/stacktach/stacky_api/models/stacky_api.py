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


class StackTachEntity(AutoMarshallingModel):

    def __init__(self, **kwargs):
        """
        An object that represents a StackTach Response Entity.
        """
        super(StackTachEntity, self).__init__(**kwargs)
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
        Returns an instance of a StackTach Response Entity
        based on the json serialized_str passed in.
        """
        results = json.loads(serialized_str)
        # One or more deployments will be a list
        entities = []
        for row in results[1:]:
            entity_dict = {}
            for i in range(0, len(results[0])):
                entity_dict[results[0][i]] = row[i]
                entity = cls._dict_to_obj(entity_dict)
            entities.append(entity)
        return entities

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach Response Entity instance.
        """
        entity = StackTachEntity(**entity_dict)
        return entity

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        Not Implemented
        """
        raise NotImplementedError("Not Implemented!")

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        Not Implemented
        """
        raise NotImplementedError("Not Implemented!")
