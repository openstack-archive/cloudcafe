"""
Copyright 2015 Rackspace

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

from cloudcafe.compute.extensions.config_drive.models.\
    config_drive_vendor_meta import VendorMeta


class VendorMetaTest(object):

    def test_meta_services(self):
        self.assertEqual(self.vendor_meta.network_info.services[0].type, "dns")
        self.assertEqual(self.vendor_meta.network_info.services[0].address,
                         "173")

    def test_server_networks(self):
        self.assertEqual(self.vendor_meta.network_info.networks[0].network_id,
                         "0")
        self.assertEqual(self.vendor_meta.network_info.networks[0].type,
                         "ipv4")
        self.assertEqual(self.vendor_meta.network_info.networks[0].netmask,
                         "0")
        self.assertEqual(self.vendor_meta.network_info.networks[0].link,
                         "tap")
        self.assertEqual(self.vendor_meta.network_info.networks[0].routes,
                         "1")

    def test_meta_links(self):
        self.assertEqual(
            self.vendor_meta.network_info.links[0].ethernet_mac_address,
            "FE:")
        self.assertEqual(self.vendor_meta.network_info.links[0].mtu,
                         "15")
        self.assertEqual(self.vendor_meta.network_info.links[0].id,
                         "tap")
        self.assertEqual(self.vendor_meta.network_info.links[0].vif_id,
                         "647")

    def test_meta_general_fields(self):
        self.assertEqual(self.vendor_meta.region, "prod")
        self.assertEqual(self.vendor_meta.ip_whitelist, "173/29")
        self.assertEqual(self.vendor_meta.roles, "user:admin")
        self.assertEqual(self.vendor_meta.provider, "Company")


class CreateVendorMetaObject(unittest.TestCase, VendorMetaTest):
    @classmethod
    def setUpClass(cls):

        vendor_meta_json = ('{"network_info": {"services": [{"type": "dns", '
                            '"address": "173"}], '
                            '"networks": [{"network_id": "0", '
                            '"type": "ipv4", "netmask": "0", "link": "tap", '
                            '"routes": "1"}], '
                            '"links": [{"ethernet_mac_address": "FE:", '
                            '"mtu": "15", "id": "tap", "vif_id": "647"}]}, '
                            '"region": "prod", '
                            '"ip_whitelist": "173/29", '
                            '"roles": "user:admin", "provider": "Company"}')
        print vendor_meta_json
        cls.vendor_meta = VendorMeta.deserialize(vendor_meta_json, 'json')
