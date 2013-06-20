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


class QuotasMockResponse():

    def __init__(self, format):
        self.format = format

    def _get_quota(self):
        return getattr(self, '_{0}_quota'.format(self.format))()

    def _json_quota(self):
        return '{"quota_set":' \
               ' {"cores": 20,' \
               '"floating_ips": 10,' \
               '"id": "fake_tenant",' \
               '"injected_file_content_bytes": 10240,' \
               '"injected_file_path_bytes": 255,' \
               '"injected_files": 5,' \
               '"instances": 10,' \
               '"key_pairs": 100,' \
               '"metadata_items": 128,' \
               '"ram": 51200,' \
               '"security_group_rules": 20,' \
               '"security_group_rules": 10}}'

    def _xml_quota(self):
        return '<?xml version="1.0" encoding="UTF-8"?>' \
               '<quota_set id="fake_tenant">' \
               '<cores>20</cores>' \
               '<floating_ips>10</floating_ips>' \
               '<injected_file_content_bytes>10240' \
               '</injected_file_content_bytes>' \
               '<injected_file_path_bytes>255</injected_file_path_bytes>' \
               '<injected_files>5</injected_files>' \
               '<instances>10</instances>' \
               '<key_pairs>100</key_pairs>' \
               '<metadata_items>128</metadata_items>' \
               '<ram>51200</ram>' \
               '<security_group_rules>20</security_group_rules>' \
               '<security_group_rules>10</security_group_rules></quota_set>'
