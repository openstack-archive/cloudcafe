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


class UsedLimitsMockResponse():

    @classmethod
    def get_used_limit(cls):
        return '{"limits":' \
               '{"absolute":' \
               '{"maxImageMeta":128,' \
               '"maxPersonality":5,' \
               '"maxPersonalitySize":10240,' \
               '"maxSecurityGroupRules":20,' \
               '"maxSecurityGroups":10,' \
               '"maxServerMeta":128,' \
               '"maxTotalCores":20,' \
               '"maxTotalFloatingIps":10,' \
               '"maxTotalInstances":10,' \
               '"maxTotalKeypairs":100,' \
               '"maxTotalRAMSize":51200,' \
               '"totalCoresUsed":0,' \
               '"totalInstancesUsed":0,' \
               '"totalRAMUsed":0,' \
               '"totalSecurityGroupsUsed":0,' \
               '"totalFloatingIpsUsed":0},' \
               '"rate":' \
               '[{"limit":' \
               '[{"next-available":' \
               '"2012-11-27T17:24:53Z",' \
               '"remaining":10,' \
               '"unit":"MINUTE",' \
               '"value":10,' \
               '"verb":"POST"},' \
               '{"next-available":' \
               '"2012-11-27T17:24:53Z",' \
               '"remaining":10,' \
               '"unit":"MINUTE",' \
               '"value":10,' \
               '"verb":"PUT"}],' \
               '"regex":".*",' \
               '"uri":"*"}]}}'
