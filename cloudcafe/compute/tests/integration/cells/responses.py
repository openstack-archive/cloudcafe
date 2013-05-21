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


class CellsClientMockResponse():

    @classmethod
    def get_cell_capacity_by_cellname(cls):
        return '{"cell":' \
               ' { "capacities":' \
               ' {"ram_free": ' \
               '{"units_by_mb": ' \
               '{"8192": 0, "512": 13, "4096": 1, "2048": 3, "16384": 0},' \
               '"total_mb": 7680},' \
               '"disk_free":' \
               '{"units_by_mb": {"81920": 11, "20480": 46, ' \
               '"40960": 23, "163840": 5, "0": 0},' \
               '"total_mb": 1052672}}}}'

    @classmethod
    def get_aggr_cell_capacity(cls):
        return '{"cell":' \
               ' { "capacities":' \
               ' {"ram_free": ' \
               '{"units_by_mb": ' \
               '{"8192": 0, "512": 13, "4096": 1, "2048": 3, "16384": 0},' \
               '"total_mb": 7680},' \
               '"disk_free":' \
               '{"units_by_mb": {"81920": 11, "20480": 46, ' \
               '"40960": 23, "163840": 5, "0": 0},' \
               '"total_mb": 1052672}}}}'
