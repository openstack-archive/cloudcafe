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
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.compute.common.constants import Constants


class Limits(AutoMarshallingModel):

    def __init__(self, **kwargs):
        '''An object that represents Limits.
        Keyword arguments:
        '''
        super(Limits, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    def _obj_to_json(self):
        '''
        Automatically assigns any value that is an int or a str and is not
        None to a dictionary. Then returns the str representation of that dict.
        '''
        '''TODO: Implement serialization of lists, dictionaries, and objects'''
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        '''need to code'''
        pass

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a Limits based on the json serialized_str
        passed in.'''
        json_dict = json.loads(serialized_str)
        ret = None
        if 'limits' in json_dict.keys():
            ret = Limits(**(json_dict.get('limits')))
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns a Limits Response Object based on xml serialized str'''
        limits = {}
        rate_list = []
        absolute_dict = {}
        #Removing namespaces
        root = ET.fromstring(serialized_str)
        cls._remove_namespace(root,
                              'http://docs.openstack.org/common/api/v1.0')
        cls._remove_namespace(root,
                              'http://docs.openstack.org/common/api/v1.1')
        #Rates Limits
        rate_element_list = root.find('rates').findall('rate')
        for rate_element in rate_element_list:
            limit_element_list = rate_element.findall('limit')
            limit_list = []
            rate_dict = {}
            for limit in limit_element_list:
                limit_dict = {}
                attrib = limit.attrib
                for key in attrib.keys():
                    limit_dict[key] = attrib.get(key)
                limit_list.append(limit_dict)
            rate_dict['limit'] = limit_list

            attrib = rate_element.attrib
            for key in attrib.keys():
                rate_dict[key] = attrib.get(key)

            rate_list.append(rate_dict)
            #Absolute Limits
        absolute_list = root.find('absolute')
        cls._remove_namespace(absolute_list, Constants.XML_API_ATOM_NAMESPACE)
        used = 'http://docs.openstack.org/compute/ext/used_limits/api/v1.1'
        cls._remove_namespace(absolute_list, used)
        for element in absolute_list.findall('limit'):
            attrib = element.attrib
            absolute_dict[attrib.get('name')] = int(attrib.get('value'))

        limits['absolute'] = absolute_dict
        limits['rate'] = rate_list
        return Limits(**limits)

    @classmethod
    def _dict_to_obj(cls, limits_dict):
        '''Helper method to turn dictionary into Limits instance.'''
        limits = Limits(**limits_dict)
        return limits

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other
