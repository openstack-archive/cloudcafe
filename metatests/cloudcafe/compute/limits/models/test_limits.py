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

import unittest

from cloudcafe.compute.limits_api.models.limit import TenantLimits


class LimitsModelTest(object):

    def test_rate_limits(self):

        # Validate rate limit
        self.assertEqual(len(self.limits.rate_limits), 1)
        rate_limit = self.limits.rate_limits[0]
        self.assertEqual(rate_limit.regex, '/v[^/]/(\\d+)/?.*')
        self.assertEqual(rate_limit.uri, '*')
        self.assertEqual(len(rate_limit.limits), 2)

        # Validate first limit
        first_limit = rate_limit.limits[0]
        self.assertEqual(first_limit.next_available,
                         '2013-08-20T17:10:28.995Z')
        self.assertEqual(first_limit.unit, 'MINUTE')
        self.assertEqual(first_limit.remaining, 1999)
        self.assertEqual(first_limit.value, 2000)
        self.assertEqual(first_limit.verb, 'GET')

        # Validate second limit
        second_limit = rate_limit.limits[1]
        self.assertEqual(second_limit.next_available,
                         '2013-08-20T17:10:03.071Z')
        self.assertEqual(second_limit.unit, 'MINUTE')
        self.assertEqual(second_limit.remaining, 200)
        self.assertEqual(second_limit.value, 200)
        self.assertEqual(second_limit.verb, 'POST')

    def test_max_server_metadata(self):
        self.assertEqual(self.limits.absolute_limits.max_server_meta, 40)

    def test_max_personality(self):
        self.assertEqual(self.limits.absolute_limits.max_personality, 5)

    def test_total_private_networks_used(self):
        self.assertEqual(
            self.limits.absolute_limits.total_private_networks_used, 0)

    def test_max_image_metadata(self):
        self.assertEqual(self.limits.absolute_limits.max_image_meta, 40)

    def test_max_personality_size(self):
        self.assertEqual(
            self.limits.absolute_limits.max_personality_size, 1000)

    def test_max_security_group_rules(self):
        self.assertEqual(self.limits.absolute_limits.max_sec_group_rules, 20)

    def test_max_total_keypairs(self):
        self.assertEqual(self.limits.absolute_limits.max_total_keypairs, 100)

    def test_total_cores_used(self):
        self.assertEqual(self.limits.absolute_limits.total_cores_used, 9)

    def test_total_ram_used(self):
        self.assertEqual(self.limits.absolute_limits.total_ram_used, 31232)

    def test_total_instances_used(self):
        self.assertEqual(self.limits.absolute_limits.total_instances_used, 2)

    def test_total_floating_ips_used(self):
        self.assertEqual(
            self.limits.absolute_limits.total_floating_ips_used, 0)

    def test_max_total_cores(self):
        self.assertEqual(self.limits.absolute_limits.max_total_cores, -1)

    def test_total_security_groups_used(self):
        self.assertEqual(self.limits.absolute_limits.total_sec_groups_used, 0)

    def test_max_total_private_networks(self):
        self.assertEqual(
            self.limits.absolute_limits.max_total_private_networks, 6)

    def test_max_total_floating_ips(self):
        self.assertEqual(
            self.limits.absolute_limits.max_total_floating_ips, 5)

    def test_max_total_instances(self):
        self.assertEqual(self.limits.absolute_limits.max_total_instances, 100)

    def test_max_total_ram_size(self):
        self.assertEqual(
            self.limits.absolute_limits.max_total_ram_size, 650000)

    def test_max_security_groups(self):
        self.assertEqual(self.limits.absolute_limits.max_sec_groups, 10)


class LimitsJSONModelTest(unittest.TestCase, LimitsModelTest):

    @classmethod
    def setUpClass(cls):
        cls.limits_json = \
            """
            {
              "limits" : {
                "rate" : [
                  {
                    "regex" : "/v[^/]/(\\d+)/?.*",
                    "uri" : "*",
                    "limit" : [
                      {
                        "next-available" : "2013-08-20T17:10:28.995Z",
                        "unit" : "MINUTE",
                        "remaining" : 1999,
                        "value" : 2000,
                        "verb" : "GET"
                      },
                      {
                        "next-available" : "2013-08-20T17:10:03.071Z",
                        "unit" : "MINUTE",
                        "remaining" : 200,
                        "value" : 200,
                        "verb" : "POST"
                      }
                    ]
                  }
                ],
                "absolute" : {
                  "maxServerMeta" : 40,
                  "maxPersonality" : 5,
                  "totalPrivateNetworksUsed" : 0,
                  "maxImageMeta" : 40,
                  "maxPersonalitySize" : 1000,
                  "maxSecurityGroupRules" : 20,
                  "maxTotalKeypairs" : 100,
                  "totalCoresUsed" : 9,
                  "totalRAMUsed" : 31232,
                  "totalInstancesUsed" : 2,
                  "maxSecurityGroups" : 10,
                  "totalFloatingIpsUsed" : 0,
                  "maxTotalCores" : -1,
                  "totalSecurityGroupsUsed" : 0,
                  "maxTotalPrivateNetworks" : 6,
                  "maxTotalFloatingIps" : 5,
                  "maxTotalInstances" : 100,
                  "maxTotalRAMSize" : 650000
                }
              }
            }
            """
        cls.limits = TenantLimits.deserialize(cls.limits_json, 'json')


class LimitsXMLModelTest(unittest.TestCase, LimitsModelTest):

    @classmethod
    def setUpClass(cls):
        docs_url = 'http://docs.openstack.org'
        cls.limits_xml = \
            """
            <limits xmlns:lim="{docs_url}/common/api/v1.0"
            xmlns="{docs_url}/common/api/v1.0">
            <rates>
            <rate regex="/v[^/]/(\d+)/?.*" uri="*">
            <limit next-available="2013-08-20T17:10:28.995Z" unit="MINUTE"
            remaining="1999" value="2000" verb="GET"/>
            <limit next-available="2013-08-20T17:10:03.071Z" unit="MINUTE"
            remaining="200" value="200" verb="POST"/>
            </rate>
            </rates>
            <absolute
            xmlns:os-used-limits="{docs_url}/compute/ext/used_limits/api/v1.1"
            xmlns:atom="http://www.w3.org/2005/Atom">
            <limit name="maxServerMeta" value="40"/>
            <limit name="maxPersonality" value="5"/>
            <limit name="totalPrivateNetworksUsed" value="0"/>
            <limit name="maxImageMeta" value="40"/>
            <limit name="maxPersonalitySize" value="1000"/>
            <limit name="maxSecurityGroupRules" value="20"/>
            <limit name="maxTotalKeypairs" value="100"/>
            <limit name="totalCoresUsed" value="9"/>
            <limit name="totalRAMUsed" value="31232"/>
            <limit name="totalInstancesUsed" value="2"/>
            <limit name="maxSecurityGroups" value="10"/>
            <limit name="totalFloatingIpsUsed" value="0"/>
            <limit name="maxTotalCores" value="-1"/>
            <limit name="totalSecurityGroupsUsed" value="0"/>
            <limit name="maxTotalPrivateNetworks" value="6"/>
            <limit name="maxTotalFloatingIps" value="5"/>
            <limit name="maxTotalInstances" value="100"/>
            <limit name="maxTotalRAMSize" value="650000"/>
            </absolute>
            </limits>
            """.format(docs_url=docs_url)
        cls.limits = TenantLimits.deserialize(cls.limits_xml, 'xml')
