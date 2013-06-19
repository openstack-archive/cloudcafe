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
from cloudcafe.compute.cells_api.model.capacity import CellCapacity


class Cell(AutoMarshallingModel):

    def __init__(self, disk_capacity=None, ram_capacity=None):
        super(Cell, self).__init__()
        self.disk_capacity = disk_capacity
        self.ram_capacity = ram_capacity

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Host object to compare with
        @type other: Host
        @return: True if Host objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Host object to compare with
        @type other: Host
        @return: True if Host objects are not equal, False otherwise
        @rtype: bool
        """
        return not self.__eq__(other)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Cell or a collection of Cells
         based on the json serialized_str passed in.
        @param serialized_str: json serialized string.
        @type serialized_str: String.
        @return: Cell.
        @rtype: Cell.
         """

        json_dict = json.loads(serialized_str)
        disk_capacity_dict = json_dict.get('cell').\
            get('capacities').get('disk_free')
        disk_capacity = CellCapacity._dict_to_obj(disk_capacity_dict)
        ram_capacity_dict = json_dict.get('cell').\
            get('capacities').get('ram_free')
        ram_capacity = CellCapacity._dict_to_obj(ram_capacity_dict)
        cell = Cell(disk_capacity, ram_capacity)
        return cell

    @classmethod
    def _dict_to_obj(cls, cell_dict):
        """
        @summary: Returns an instance of a Cell based on Cell dictionary
         passed.
        @param cell_dict: Cell dictionary.
        @type cell_dict: Dictionary.
        @return: Cell.
        @rtype: Cell.
         """
        cell = Cell(**cell_dict)
        return cell

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Cell.
        @param serialized_str: xml serialized string.
        @type serialized_str: String.
        @return: Cell.
        @rtype: Cell.
         """
        element = ET.fromstring(serialized_str)
        capacity = element.find('capacities')
        ram_capacity_xml = capacity.find('ram_free')
        ram_capacity = CellCapacity._xml_to_obj(ram_capacity_xml)
        disk_capacity_xml = capacity.find("disk_free")
        disk_capacity = CellCapacity._xml_to_obj(disk_capacity_xml)
        cell = Cell(disk_capacity, ram_capacity)
        return cell
