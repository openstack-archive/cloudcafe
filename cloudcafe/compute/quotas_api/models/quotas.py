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


class Quota(AutoMarshallingModel):

    def __init__(self, cores, floating_ips, id,
                 injected_file_content_bytes, injected_file_path_bytes,
                 injected_files, instances, key_pairs,
                 metadata_items, ram, security_group_rules,
                 security_groups):
        super(Quota, self).__init__()
        self.cores = cores
        self.floating_ips = floating_ips
        self.id = id
        self.injected_file_content_bytes = injected_file_content_bytes
        self.injected_file_path_bytes = injected_file_path_bytes
        self.injected_files = injected_files
        self.instances = instances
        self.key_pairs = key_pairs
        self.metadata_items = metadata_items
        self.ram = ram
        self.security_group_rules = security_group_rules
        self.security_groups = security_groups

    @classmethod
    def _dict_to_obj(self, quota_dict):
        return Quota(quota_dict.get('cores'),
                     quota_dict.get('floating_ips'),
                     quota_dict.get('id'),
                     quota_dict.get('injected_file_content_bytes'),
                     quota_dict.get('injected_file_path_bytes'),
                     quota_dict.get('injected_files'),
                     quota_dict.get('instances'),
                     quota_dict.get('key_pairs'),
                     quota_dict.get('metadata_items'),
                     quota_dict.get('ram'),
                     quota_dict.get('security_group_rules'),
                     quota_dict.get('security_groups'))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Quota
         based on the json serialized_str passed in.
        @param serialized_str: json serialized string.
        @type serialized_str: String.
        @return: Quota.
        @rtype: Quota.
         """
        quota_dict = json.loads(serialized_str)
        quota = cls._dict_to_obj(quota_dict.get('quota_set'))
        return quota

    @classmethod
    def _xml_ele_to_obj(cls, element):
        quota_dict = dict((x.tag, x.text) for x in element._children)
        quota_dict.update(element.attrib)
        quota = cls._dict_to_obj(quota_dict)
        return quota

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Quota
         based on the xml serialized_str passed in.
        @param serialized_str: xml serialized string.
        @type serialized_str: String.
        @return: Quota.
        @rtype: Quota.
         """
        element = ET.fromstring(serialized_str)
        quota = cls._xml_ele_to_obj(element)
        return quota
