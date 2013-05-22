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


class UpdateQuotaRequest(AutoMarshallingModel):

    def __init__(self, cores=None, floating_ips=None, id=None,
                 injected_file_content_bytes=None,
                 injected_file_path_bytes=None,
                 injected_files=None, instances=None,
                 key_pairs=None, metadata_items=None,
                 ram=None, security_group_rules=None,
                 security_groups=None):
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

    def _obj_to_json(self):
        """
        @summary: Converts the object to json
        """
        body = {}
        for key, value in self.__dict__.iteritems():
            if value is not None:
                body[key] = value
        return json.dumps({'quota_set': body})

    def _obj_to_xml(self):
        """
        @summary: Converts the object to xml.
        """
        xml = Constants.XML_HEADER
        element = ET.Element('quota_set')
        element.set('id', self.id)
        for key, value in self.__dict__.iteritems():
            if value is not None and key != 'id':
                child = ET.Element(key)
                child.text = str(value)
                element.append(child)
        xml += ET.tostring(element)
        return xml
