
import json
from xml.etree import ElementTree

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel


class _VolumesAPIBaseModel(AutoMarshallingModel):
    obj_model_key = None
    kwarg_map = {}

    @classmethod
    def _map_values_to_kwargs(cls, deserialized_obj):
        kwargs = {}
        for local_kw, deserialized_obj_kw in cls.kwarg_map.iteritems():
            kwargs[local_kw] = deserialized_obj.get(deserialized_obj_kw)

        return cls(**kwargs)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        volume_dict = json_dict.get(cls.obj_model_key)
        return cls._json_dict_to_obj(volume_dict)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        return cls._map_values_to_kwargs(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        return cls._map_values_to_kwargs(element)


class _VolumesAPIBaseListModel(AutoMarshallingListModel):
    list_model_key = None
    ObjectModel = None

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        list_of_dicts = json_dict.get(cls.list_model_key)
        return cls._json_dict_to_obj(list_of_dicts)

    @classmethod
    def _json_dict_to_obj(cls, list_of_dicts):
        obj_list = cls()
        for obj_dict in list_of_dicts:
            obj_list.append(cls.ObjectModel._json_dict_to_obj(obj_dict))
        return obj_list

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        list_element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(list_element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_etree_element):
        obj_list = cls()
        for element in xml_etree_element:
            if element.tag.endswith(cls.list_model_key):
                for obj_element in element:
                    obj_list.append(
                        cls.ObjectModel._xml_ele_to_obj(obj_element))
        return obj_list


class _XMLDictionary(_VolumesAPIBaseModel):
    dict_model_key = 'metadata'
    key_name = 'key'

    @classmethod
    def _xml_ele_to_obj(
            cls, xml_etree_element, dict_model_key=None, key_name=None):
        dict_model_key = dict_model_key or cls.dict_model_key
        key_name = key_name or cls.key_name
        obj_dict = {}
        for element in xml_etree_element:
            if element.tag.endswith(dict_model_key):
                for obj_element in element:
                    obj_dict[obj_element.get(key_name)] = obj_element.text
        return obj_dict


class CommonModelProperties(object):

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def display_name(self):
        return self._name

    @property
    def display_description(self):
        return self._description

    @name.setter
    def name(self, value):
        self._name = value

    @description.setter
    def description(self, value):
        self._description = value

    @display_name.setter
    def display_name(self, value):
        self._name = value

    @display_description.setter
    def display_description(self, value):
        self._description = value
