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


class Links(AutoMarshallingModel):
    """
    @summary: Represents links (url) in the system
    """

    def __init__(self, links_list):
        super(Links, self).__init__()
        self.links = {}
        if links_list is not None:
            for link in links_list:
                self.links[link['rel']] = link['href']
            for key_name in self.links:
                setattr(self, key_name, self.links[key_name])

    @classmethod
    def _xml_to_object(cls, serialized_str):
        """
        @summary: Initializes the object from xml response
        @param objectified_links: links details
        @type objectified_links: objectify.Element
        """

        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """Helper method to turn ElementTree instance to Links instance."""
        links = []
        '''
        When we serialize a flavor object to XML, we generate an additional
        tag <links> for the links which is the parent to the <link> element.
        Hence we need to loop twice to get to the dictionary of links
        <links>
        <link/>
        ...
        </links>
        '''
        for child_element in element._children:
            if child_element.tag[29:] == 'link':
                links.append(child_element.attrib)
        if element.findall('link'):
            for link in element.findall('link'):
                links.append(link.attrib)
        return Links(links)

    @classmethod
    def _dict_to_obj(cls, list_of_links):
        """
        @summary: Initializes the object from json response
        @param list_of_links: links details
        @type list_of_links: list
        """
        return Links(list_of_links)

    def __repr__(self):
        values = []
        for prop in __dict__:
            values.append("%s: %s" % (prop, __dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of links based on the json
        serialized_str passed in.
        """
        json_dict = json.loads(serialized_str)
        if 'links' in json_dict.keys():
            links_list = json_dict['links']
            return Links(links_list)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Links object to compare with
        @type other: Links
        @return: True if Links objects are equal, False otherwise
        @rtype: bool
        """
        if self is None and other is None:
            return True

        if self is None or other is None:
            return False

        for key in self.links:
            # Alternate links are random, equality is impossible..ignoring it
            if key != 'alternate' and self.links[key] != other.links[key]:
                return False
        return True

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Links object to compare with
        @type other: Links
        @return: True if Links objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other
