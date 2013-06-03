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


from cloudcafe.compute.extensions.used_limits.model.used_limits \
    import UsedLimits


class UsedLimitForAdminDomainTest(object):

    def test_rate(self):
        self.assertEqual(self.used_limit.rate.regex, ".*")
        self.assertEqual(self.used_limit.rate.uri, "*")
        self.assertEqual(self.used_limit.rate.limit[0].next_available,
                         '2012-11-27T17:24:53Z')
        self.assertEqual(self.used_limit.rate.limit[0].unit,
                         'MINUTE')
        self.assertEqual(self.used_limit.rate.limit[0].verb,
                         'POST')
        self.assertEqual(str(self.used_limit.rate.limit[0].remaining),
                         '10')
        self.assertEqual(str(self.used_limit.rate.limit[0].value),
                         '10')

    def test_absolute(self):
        self.assertEqual(str(self.used_limit.absolute.maxImageMeta),
                         '128')
        self.assertEqual(str(self.used_limit.absolute.maxTotalRAMSize),
                         '51200')
        self.assertEqual(str(self.used_limit.absolute.maxTotalInstances),
                         '10')
        self.assertEqual(str(self.used_limit.absolute.maxPersonality),
                         '5')
        self.assertEqual(str(self.used_limit.absolute.maxPersonalitySize),
                         '10240')
        self.assertEqual(str(self.used_limit.absolute.maxSecurityGroupRules),
                         '20')
        self.assertEqual(str(self.used_limit.absolute.maxSecurityGroups),
                         '10')
        self.assertEqual(str(self.used_limit.absolute.maxServerMeta),
                         '128')
        self.assertEqual(str(self.used_limit.absolute.maxTotalCores),
                         '20')
        self.assertEqual(str(self.used_limit.absolute.maxTotalFloatingIps),
                         '10')
        self.assertEqual(str(self.used_limit.absolute.maxTotalKeyPairs),
                         '100')
        self.assertEqual(str(self.used_limit.absolute.totalCoresUsed),
                         '0')
        self.assertEqual(str(self.used_limit.absolute.totalFloatingIPsUsed),
                         '0')
        self.assertEqual(str(self.used_limit.absolute.totalInstancesUsed),
                         '0')
        self.assertEqual(str(self.used_limit.absolute.totalRAMUsed),
                         '0')
        self.assertEqual(str(self.used_limit.absolute.totalSecurityGroupsUsed),
                         '0')


class UsedLimitForAdminDomainJSONTest(unittest.TestCase,
                                      UsedLimitForAdminDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.used_limit_for_admin_json = '{"limits":' \
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
        cls.used_limit = UsedLimits.\
            deserialize(cls.used_limit_for_admin_json,
                        "json")


class UsedLimitForAdminDomainXMLTest(unittest.TestCase,
                                     UsedLimitForAdminDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.used_limit_xml = '<?xml version="1.0" encoding="UTF-8"?>' \
                             '<limits>' \
                             '<rates><rate regex=".*" uri="*">' \
                             '<limit ' \
                             'next-available="2012-11-27T17:24:53Z" ' \
                             'unit="MINUTE" ' \
                             'verb="POST" ' \
                             'remaining="10" ' \
                             'value="10"/>' \
                             '<limit ' \
                             'next-available="2012-11-27T17:24:53Z" ' \
                             'unit="MINUTE" ' \
                             'verb="PUT" ' \
                             'remaining="10" ' \
                             'value="10"/>' \
                             '</rate></rates>' \
                             '<absolute>' \
                             '<limit ' \
                             'name="maxServerMeta" value="128"/>' \
                             '<limit ' \
                             'name="maxPersonality" value="5"/>' \
                             '<limit ' \
                             'name="maxImageMeta" value="128"/>' \
                             '<limit ' \
                             'name="maxPersonalitySize" value="10240"/>' \
                             '<limit ' \
                             'name="maxSecurityGroupRules" value="20"/>' \
                             '<limit ' \
                             'name="maxTotalKeypairs" value="100"/>' \
                             '<limit ' \
                             'name="totalRAMUsed" value="0"/>' \
                             '<limit ' \
                             'name="totalInstancesUsed" value="0"/>' \
                             '<limit ' \
                             'name="maxSecurityGroups" value="10"/>' \
                             '<limit ' \
                             'name="totalFloatingIpsUsed" value="0"/>' \
                             '<limit ' \
                             'name="maxTotalCores" value="20"/>' \
                             '<limit ' \
                             'name="totalSecurityGroupsUsed" value="0"/>' \
                             '<limit ' \
                             'name="maxTotalFloatingIps" value="10"/>' \
                             '<limit ' \
                             'name="maxTotalInstances" value="10"/>' \
                             '<limit ' \
                             'name="totalCoresUsed" value="0"/>' \
                             '<limit ' \
                             'name="maxTotalRAMSize" value="51200"/>' \
                             '</absolute></limits>'

        cls.used_limit = UsedLimits.\
            deserialize(cls.used_limit_xml,
                        "xml")

if __name__ == '__main__':
    unittest.main()
