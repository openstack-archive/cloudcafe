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


class SecurityGroupRulesMockResponse():

    def __init__(self, format):
        self.format = format

    def _get_sec_group_rule(self):
        return getattr(self, '_{0}_sec_group_rule'.format(self.format))()

    def _json_sec_group_rule(self):
        return ('{"security_group_rule":'
                ' {"from_port": 80,'
                ' "ip_protocol": "tcp",'
                ' "to_port": 8080,'
                ' "parent_group_id": 2,'
                ' "ip_range": {"cidr": "0.0.0.0/0"},'
                ' "id": 1'
                ' "group": {}}}')

    def _xml_sec_group_rule(self):
        return ('<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
                '<security_group_rule '
                'parent_group_id=2 id=1>'
                '<from_port>80</from_port>'
                '<ip_protocol>tcp</ip_protocol>'
                '<to_port>8080</to_port>'
                '<ip_range>'
                '<cidr>0.0.0.0/0</cidr>'
                '</ip_range>'
                '<group>'
                '<name>None</name>'
                '<tenant_id>None</tenant_id>'
                '</group>'
                '</security_group_rule>')
