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

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.equality_tools import EqualityTools


class Resource(AutoMarshallingModel):

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Resource object to compare with
        @type other: Resource
        @return: True if Host objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Resource object to compare with
        @type other: Resource
        @return: True if Host objects are not equal, False otherwise
        @rtype: bool
        """
        return not self.__eq__(other)

    @classmethod
    def _dict_to_obj(cls, resource_dict):
        """
        @summary: Returns an instance of a Resource based on Resource
        dictionary passed.
        @param resource_dict: resource dictionary.
        @type resource_dict: Dictionary.
        @return: Resource.
        @rtype: Resource.
         """
        resource = Resource(**resource_dict)
        return resource

    @classmethod
    def _xml_to_obj(cls, element):
        """
        @summary: Returns an instance of a Resource based on Element
         passed.
        @param element: xml element.
        @type element: Element.
        @return: Resource.
        @rtype: Resource.
         """
        resource_dict = dict((x.tag, x.text) for x in element._children)
        resource = Resource(**resource_dict)
        return resource
