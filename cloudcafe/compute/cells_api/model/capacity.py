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


class Unit():

    def __init__(self, size, unit):
        self.size = size
        self.unit = unit

    @classmethod
    def _dict_to_obj(cls, unit_dict):
        return Unit(unit_dict.get('mb'),
                    unit_dict.get('unit'))


class CellCapacity(AutoMarshallingModel):

    def __init__(self, total_mb=None,
                 units_by_mb=None):
        super(CellCapacity, self).__init__()
        self.total_mb = total_mb
        self.units = units_by_mb

    @classmethod
    def _dict_to_obj(cls, capacity_dict):
        """
        @summary: Returns an instance of a CellCapacity
         based on CellCapacity dictionary passed.
        @param capacity_dict: CellCapacity dictionary.
        @type capacity_dict: Dictionary.
        @return: CellCapacity.
        @rtype: CellCapacity.
         """
        units = []
        for key, value in capacity_dict.get("units_by_mb").iteritems():
            units.append(Unit._dict_to_obj({'mb': key, 'unit': value}))
        return CellCapacity(capacity_dict.get('total_mb'), units)

    @classmethod
    def _xml_to_obj(cls, capacity_element):
        """
        @summary: Returns an instance of a CellCapacity
         based on CellCapacity xml element passed.
        @param capacity_element: CellCapacity element.
        @type capacity_element: Element.
        @return: CellCapacity.
        @rtype: CellCapacity.
         """
        units = []
        for unit in capacity_element.findall('unit_by_mb'):
            units.append(Unit._dict_to_obj(unit.attrib))
        return CellCapacity(capacity_element.attrib.get('total_mb'), units)
