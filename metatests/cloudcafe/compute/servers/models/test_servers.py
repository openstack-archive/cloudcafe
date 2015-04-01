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

from cloudcafe.compute.common.types import ComputeTaskStates
from cloudcafe.compute.servers_api.models.servers import Server


class ServerDomainTest(object):

    def test_server_disk_config(self):
        self.assertEqual(self.server.disk_config, "AUTO")

    def test_server_power_state(self):
        self.assertEqual(self.server.power_state, 1)

    def test_server_progress(self):
        self.assertEqual(self.server.progress, 100)

    def test_server_task_state(self):
        self.assertEqual(self.server.task_state, ComputeTaskStates.NONE)

    def test_server_vm_state(self):
        self.assertEqual(self.server.vm_state, "active")

    def test_server_id(self):
        self.assertEqual(self.server.id, "5")

    def test_server_name(self):
        self.assertEqual(self.server.name, "testserver47476")

    def test_tenant_id(self):
        self.assertEqual(self.server.tenant_id, "660")

    def test_server_status(self):
        self.assertEqual(self.server.status, "ACTIVE")

    def test_server_updated_time(self):
        self.assertEqual(self.server.updated, "2012-12-03T19:04:06Z")

    def test_host_id(self):
        self.assertEqual(
            self.server.host_id, "123")

    def test_user_id(self):
        self.assertEqual(self.server.user_id, "199835")

    def test_server_created_time(self):
        self.assertEqual(self.server.created, "2012-12-03T18:59:16Z")

    def test_server_access_ips(self):
        self.assertEqual(self.server.accessIPv4, "192.168.1.10")
        self.assertEqual(self.server.accessIPv6,
                         "2001:11:7811:69:cf10:c02d:ff10:fa")

    def test_server_addresses(self):
        self.assertEqual(self.server.addresses.public.ipv4, "198.61.236.10")
        self.assertEqual(self.server.addresses.public.addresses[0].version, 4)
        self.assertEqual(self.server.addresses.public.ipv6,
                         "2001:11:7811:69:cf10:c02d:ff10:fa")
        self.assertEqual(self.server.addresses.public.addresses[1].version, 6)
        self.assertEqual(self.server.addresses.private.ipv4, "10.176.99.109")
        self.assertEqual(
            self.server.addresses.private.addresses[0].version, 4)

    def test_server_flavor(self):
        self.assertEqual(self.server.flavor.id, "2")
        self.assertEqual(
            self.server.flavor.links.bookmark,
            "https://127.0.0.1/660/flavors/2")

    def test_server_image(self):
        self.assertEqual(self.server.image.id, "1")
        self.assertEqual(
            self.server.image.links.bookmark,
            "https://127.0.0.1/660/images/1")

    def test_server_links(self):
        self.assertEqual(
            self.server.links.self, "https://127.0.0.1/v2/660/servers/5")
        self.assertEqual(
            self.server.links.bookmark, "https://127.0.0.1/660/servers/5")

    def test_server_metadata(self):
        self.assertEqual(self.server.metadata.get('meta1'), "value1")

    def test_server_keypair(self):
        self.assertEqual(self.server.key_name, "ssh_key")

    def test_server_instance_name(self):
        self.assertEqual(self.server.instance_name, 'instance-test')

    def test_hypervisor_hostname(self):
        self.assertEqual(self.server.hypervisor_name, 'hyper-host')

    def test_server_host(self):
        self.assertEqual(self.server.host, 'host123')


class ServerFromVolumeDomainTest(object):

    def test_server_image(self):
        self.assertIsNone(self.server.image)


class ServerXMLDomainTest(unittest.TestCase, ServerDomainTest):

    @classmethod
    def setUpClass(cls):
        docs_url = 'http://docs.openstack.org'
        ext = 'compute/ext/extended_status'
        cls.server_xml = \
            """
            <server
            xmlns:OS-DCF="{docs_url}/compute/ext/disk_config/api/v1.1"
            xmlns:OS-EXT-STS="{docs_url}/{ext}/api/v1.1"
            xmlns:OS-EXT-SRV-ATTR="{docs_url}/{ext}/api/v1.1"
            xmlns:atom="http://www.w3.org/2005/Atom"
            xmlns="{docs_url}/compute/api/v1.1"
            status="ACTIVE" updated="2012-12-03T19:04:06Z"
            hostId="123"
            tenant_id="660"
            name="testserver47476" created="2012-12-03T18:59:16Z"
            userId="199835" tenantId="660" accessIPv4="192.168.1.10"
            accessIPv6="2001:11:7811:69:cf10:c02d:ff10:fa"
            progress="100" id="5" OS-EXT-STS:vm_state="active"
            key_name="ssh_key"
            OS-EXT-STS:task_state="None" OS-EXT-STS:power_state="1"
            OS-DCF:diskConfig="AUTO"
            OS-EXT-SRV-ATTR:instance_name="instance-test"
            OS-EXT-SRV-ATTR:host="host123"
            OS-EXT-SRV-ATTR:hypervisor_hostname="hyper-host">
            <image id="1">
                <atom:link href="https://127.0.0.1/660/images/1"
                rel="bookmark"/>
            </image>
            <flavor id="2">
                <atom:link href="https://127.0.0.1/660/flavors/2"
                rel="bookmark"/>
            </flavor>
            <metadata>
                <meta key="meta1">value1</meta>
            </metadata>
            <addresses>
                <network id="public">
                    <ip version="4" addr="198.61.236.10"/>
                    <ip version="6" addr="2001:11:7811:69:cf10:c02d:ff10:fa"/>
                </network>
                <network id="private">
                    <ip version="4" addr="10.176.99.109"/>
                </network>
            </addresses>
            <atom:link href="https://127.0.0.1/v2/660/servers/5" rel="self"/>
            <atom:link href="https://127.0.0.1/660/servers/5" rel="bookmark"/>
            </server>
            """.format(docs_url=docs_url, ext=ext)
        cls.server = Server.deserialize(cls.server_xml, 'xml')


class ServerJSONDomainTest(unittest.TestCase, ServerDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.server_json = \
            """
            {
              "server" : {
                "status" : "ACTIVE",
                "key_name" : "ssh_key",
                "updated" : "2012-12-03T19:04:06Z",
                "hostId" : "123",
                "OS-EXT-SRV-ATTR:host" : "host123",
                "addresses" : {
                  "public" : [
                    {
                      "version" : 4,
                      "addr" : "198.61.236.10"
                    },
                    {
                      "version" : 6,
                      "addr" : "2001:11:7811:69:cf10:c02d:ff10:fa"
                    }
                  ],
                  "private" : [
                    {
                      "version" : 4,
                      "addr" : "10.176.99.109"
                    }
                  ]
                },
                "links" : [
                  {
                    "href" : "https://127.0.0.1/v2/660/servers/5",
                    "rel" : "self"
                  },
                  {
                    "href" : "https://127.0.0.1/660/servers/5",
                    "rel" : "bookmark"
                  }
                ],
                "image" : {
                  "id" : "1",
                  "links" : [
                    {
                      "href" : "https://127.0.0.1/660/images/1",
                      "rel" : "bookmark"
                    }
                  ]
                },
                "OS-EXT-STS:task_state" : null,
                "OS-EXT-STS:vm_state" : "active",
                "OS-EXT-SRV-ATTR:instance_name" : "instance-test",
                "OS-EXT-SRV-ATTR:hypervisor_hostname" : "hyper-host",
                "flavor" : {
                  "id" : "2",
                  "links" : [
                    {
                      "href" : "https://127.0.0.1/660/flavors/2",
                      "rel" : "bookmark"
                    }
                  ]
                },
                "id" : "5",
                "user_id" : "199835",
                "name" : "testserver47476",
                "created" : "2012-12-03T18:59:16Z",
                "tenant_id" : "660",
                "OS-DCF:diskConfig" : "AUTO",
                "accessIPv4" : "192.168.1.10",
                "accessIPv6" : "2001:11:7811:69:cf10:c02d:ff10:fa",
                "progress" : 100,
                "OS-EXT-STS:power_state" : 1,
                "metadata" : {
                    "meta1": "value1"
                }
              }
            }
            """
        cls.server = Server.deserialize(cls.server_json, 'json')


class ServerFromVolumeXMLDomainTest(unittest.TestCase,
                                    ServerFromVolumeDomainTest):

    @classmethod
    def setUpClass(cls):
        docs_url = 'http://docs.openstack.org'
        ext = 'compute/ext/extended_status'
        cls.server_xml = \
            """
            <server
            xmlns:OS-DCF="{docs_url}/compute/ext/disk_config/api/v1.1"
            xmlns:OS-EXT-STS="{docs_url}/{ext}/api/v1.1"
            xmlns:OS-EXT-SRV-ATTR="{docs_url}/{ext}/api/v1.1"
            xmlns:atom="http://www.w3.org/2005/Atom"
            xmlns="{docs_url}/compute/api/v1.1"
            status="ACTIVE" updated="2012-12-03T19:04:06Z"
            hostId="123"
            tenant_id="660"
            name="testserver47476" created="2012-12-03T18:59:16Z"
            userId="199835" tenantId="660" accessIPv4="192.168.1.10"
            accessIPv6="2001:11:7811:69:cf10:c02d:ff10:fa"
            progress="100" id="5" OS-EXT-STS:vm_state="active"
            key_name="ssh_key"
            OS-EXT-STS:task_state="None" OS-EXT-STS:power_state="1"
            OS-DCF:diskConfig="AUTO"
            OS-EXT-SRV-ATTR:instance_name="instance-test"
            OS-EXT-SRV-ATTR:host="host123"
            OS-EXT-SRV-ATTR:hypervisor_hostname="hyper-host">
            <image/>
            <flavor id="2">
                <atom:link href="https://127.0.0.1/660/flavors/2"
                rel="bookmark"/>
            </flavor>
            <metadata>
                <meta key="meta1">value1</meta>
            </metadata>
            <addresses>
                <network id="public">
                    <ip version="4" addr="198.61.236.10"/>
                    <ip version="6" addr="2001:11:7811:69:cf10:c02d:ff10:fa"/>
                </network>
                <network id="private">
                    <ip version="4" addr="10.176.99.109"/>
                </network>
            </addresses>
            <atom:link href="https://127.0.0.1/v2/660/servers/5" rel="self"/>
            <atom:link href="https://127.0.0.1/660/servers/5" rel="bookmark"/>
            </server>
            """.format(docs_url=docs_url, ext=ext)
        cls.server = Server.deserialize(cls.server_xml, 'xml')


class ServerFromVolumeJSONDomainTest(unittest.TestCase,
                                     ServerFromVolumeDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.server_json = \
            """
            {
              "server" : {
                "status" : "ACTIVE",
                "key_name" : "ssh_key",
                "updated" : "2012-12-03T19:04:06Z",
                "hostId" : "123",
                "OS-EXT-SRV-ATTR:host" : "host123",
                "addresses" : {
                  "public" : [
                    {
                      "version" : 4,
                      "addr" : "198.61.236.10"
                    },
                    {
                      "version" : 6,
                      "addr" : "2001:11:7811:69:cf10:c02d:ff10:fa"
                    }
                  ],
                  "private" : [
                    {
                      "version" : 4,
                      "addr" : "10.176.99.109"
                    }
                  ]
                },
                "links" : [
                  {
                    "href" : "https://127.0.0.1/v2/660/servers/5",
                    "rel" : "self"
                  },
                  {
                    "href" : "https://127.0.0.1/660/servers/5",
                    "rel" : "bookmark"
                  }
                ],
                "image" : "",
                "OS-EXT-STS:task_state" : null,
                "OS-EXT-STS:vm_state" : "active",
                "OS-EXT-SRV-ATTR:instance_name" : "instance-test",
                "OS-EXT-SRV-ATTR:hypervisor_hostname" : "hyper-host",
                "flavor" : {
                  "id" : "2",
                  "links" : [
                    {
                      "href" : "https://127.0.0.1/660/flavors/2",
                      "rel" : "bookmark"
                    }
                  ]
                },
                "id" : "5",
                "user_id" : "199835",
                "name" : "testserver47476",
                "created" : "2012-12-03T18:59:16Z",
                "tenant_id" : "660",
                "OS-DCF:diskConfig" : "AUTO",
                "accessIPv4" : "192.168.1.10",
                "accessIPv6" : "2001:11:7811:69:cf10:c02d:ff10:fa",
                "progress" : 100,
                "OS-EXT-STS:power_state" : 1,
                "metadata" : {
                    "meta1": "value1"
                }
              }
            }
            """
        cls.server = Server.deserialize(cls.server_json, 'json')
