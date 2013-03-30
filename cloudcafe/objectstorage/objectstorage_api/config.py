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

from cloudcafe.common.models.configuration import ConfigSectionInterface


class ObjectStorageAPIConfig(ConfigSectionInterface):

    SECTION_NAME = 'objectstorage_api'

    @property
    def default_content_length(self):
        return self.get('default_content_length')

    @property
    def base_container_name(self):
        return self.get('base_container_name')

    @property
    def base_object_name(self):
        return self.get('base_object_name')

    @property
    def http_headers_per_request_count(self):
        return self.get('http_headers_per_request_count')

    @property
    def http_headers_combined_max_len(self):
        return self.get('http_headers_combined_max_len')

    @property
    def http_request_line_max_len(self):
        return self.get('http_request_line_max_len')

    @property
    def http_request_max_content_len(self):
        return self.get('http_request_max_content_len')

    @property
    def containers_name_max_len(self):
        return self.get('containers_name_max_len')

    @property
    def containers_list_default_count(self):
        return self.get('containers_list_default_count')

    @property
    def containers_list_default_max_count(self):
        return self.get('containers_list_default_max_count')

    @property
    def containers_max_count(self):
        return self.get('containers_max_count')

    @property
    def object_name_max_len(self):
        return self.get('object_name_max_len')

    @property
    def object_max_size(self):
        return self.get('object_max_size')

    @property
    def object_metadata_max_count(self):
        return self.get('object_metadata_max_count')

    @property
    def object_metadata_combined_byte_len(self):
        return self.get('object_metadata_combined_byte_len')

    @property
    def object_list_default_count(self):
        return self.get('object_list_default_count')

    @property
    def object_list_default_max_count(self):
        return self.get('object_list_default_max_count')

    @property
    def metadata_name_max_len(self):
        return self.get('metadata_name_max_len')

    @property
    def metadata_value_max_len(self):
        return self.get('metadata_value_max_len')

    @property
    def tempurl_key_cache_time(self):
        return self.get('tempurl_key_cache_time')

    @property
    def formpost_key_cache_time(self):
        return self.get('formpost_key_cache_time')
