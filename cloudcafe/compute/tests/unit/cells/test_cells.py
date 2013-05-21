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

import unittest2 as unittest

from cloudcafe.compute.cells_api.model.cells import Cell


class CellDomainTest(object):

    def test_cell_ram_capacity(self):
        self.assertEqual(str(self.cell.ram_capacity.total_mb), '7680')
        eight_gb_units = next(unit.unit for unit in
                              self.cell.ram_capacity.units
                              if unit.size == '8192')
        two_gb_units = next(unit.unit for unit in
                            self.cell.ram_capacity.units
                            if unit.size == '2048')
        four_gb_units = next(unit.unit for unit in
                             self.cell.ram_capacity.units
                             if unit.size == '4096')
        half_gb_units = next(unit.unit for unit in
                             self.cell.ram_capacity.units
                             if unit.size == '512')
        self.assertEqual(str(eight_gb_units), '0')
        self.assertEqual(str(two_gb_units), '3')
        self.assertEqual(str(four_gb_units), '1')
        self.assertEqual(str(half_gb_units), '13')

    def test_cell_disk_capacity(self):
        self.assertEqual(str(self.cell.disk_capacity.total_mb), '1052672')
        eighty_gb_units = next(unit.unit for unit in
                               self.cell.disk_capacity.units
                               if unit.size == '81920')
        twenty_gb_units = next(unit.unit for unit in
                               self.cell.disk_capacity.units
                               if unit.size == '20480')
        fourty_gb_units = next(unit.unit for unit in
                               self.cell.disk_capacity.units
                               if unit.size == '40960')
        one_and_half_tb_units = next(unit.unit for unit in
                                     self.cell.disk_capacity.units
                                     if unit.size == '163840')
        self.assertEqual(str(eighty_gb_units), '11')
        self.assertEqual(str(twenty_gb_units), '46')
        self.assertEqual(str(fourty_gb_units), '23')
        self.assertEqual(str(one_and_half_tb_units), '5')


class CellDomainJSONTest(unittest.TestCase, CellDomainTest):

    @classmethod
    def setUp(cls):
        cls.cell_json = '{"cell": ' \
                        '{"capacities": ' \
                        '{"ram_free": ' \
                        '{"units_by_mb": ' \
                        '{"8192": 0, "512": 13, "4096": 1, ' \
                        '"2048": 3, "16384": 0},' \
                        '"total_mb": 7680},' \
                        '"disk_free": ' \
                        '{"units_by_mb": {"81920": 11, "20480": 46, ' \
                        '"40960": 23, "163840": 5},' \
                        '"total_mb": 1052672}}}}'
        cls.cell = Cell.deserialize(cls.cell_json, "json")


class CellDomainXMLTest(unittest.TestCase, CellDomainTest):

    @classmethod
    def setUp(cls):
        cls.cell_xml = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<cell>' \
                       '<capacities>' \
                       '<ram_free total_mb="7680">' \
                       '<unit_by_mb unit="0"  mb="8192"/>' \
                       '<unit_by_mb unit="13" mb="512"/>' \
                       '<unit_by_mb unit="1"  mb="4096"/>' \
                       '<unit_by_mb unit="3"  mb="2048"/>' \
                       '<unit_by_mb unit="0"  mb="16384"/>' \
                       '</ram_free><disk_free total_mb="1052672">' \
                       '<unit_by_mb unit="11" mb="81920"/>' \
                       '<unit_by_mb unit="46" mb="20480"/>' \
                       '<unit_by_mb unit="23" mb="40960"/>' \
                       '<unit_by_mb unit="5"  mb="163840"/>' \
                       '<unit_by_mb unit="0"  mb="0"/>' \
                       '</disk_free></capacities></cell>'
        cls.cell = Cell.deserialize(cls.cell_xml, "xml")

if __name__ == '__main__':
    unittest.main()
