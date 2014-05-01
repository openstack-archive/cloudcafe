"""
Copyright 2014 Rackspace

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

from cloudcafe.bare_metal.nodes.models.responses import (
    Node, Nodes, DriverInterfaces)


class NodesModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nodes_json = \
            """
            {
               "nodes":[
                  {
                     "instance_uuid":null,
                     "provision_state":null,
                     "power_state":"power off",
                     "links":[
                        {
                           "href":"http://192.168.159.128:6385/v1/nodes/1",
                           "rel":"self"
                        },
                        {
                           "href":"http://192.168.159.128:6385/nodes/1",
                           "rel":"bookmark"
                        }
                     ],
                     "uuid":"1"
                  },
                  {
                     "instance_uuid":"3b209332-d933-4db2-9afd-8a0d7824e7c1",
                     "provision_state":"active",
                     "power_state":"power on",
                     "links":[
                        {
                           "href":"http://192.168.159.128:6385/v1/nodes/2",
                           "rel":"self"
                        },
                        {
                           "href":"http://192.168.159.128:6385/nodes/2",
                           "rel":"bookmark"
                        }
                     ],
                     "uuid":"2"
                  },
                  {
                     "instance_uuid":null,
                     "provision_state":null,
                     "power_state":"power off",
                     "links":[
                        {
                           "href":"http://192.168.159.128:6385/v1/nodes/3",
                           "rel":"self"
                        },
                        {
                           "href":"http://192.168.159.128:6385/nodes/3",
                           "rel":"bookmark"
                        }
                     ],
                     "uuid":"3"
                  }
               ]
            }
            """
        cls.nodes = Nodes.deserialize(cls.nodes_json, 'json')

    def test_nodes(self):
        self.assertEqual(len(self.nodes), 3)

    def test_individual_node(self):
        self.assertTrue(
            any([node for node in self.nodes if node.uuid == '1']))
        self.assertTrue(
            any([node for node in self.nodes if node.uuid == '2']))
        self.assertTrue(
            any([node for node in self.nodes if node.uuid == '3']))


class NodeModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.node_json = \
            """
            {
               "instance_uuid":"3b209332-d933-4db2-9afd-8a0d7824e7c1",
               "target_power_state":null,
               "properties":{
                  "memory_mb":"512",
                  "cpu_arch":"x86_64",
                  "local_gb":"10",
                  "cpus":"1"
               },
               "maintenance":false,
               "links":[
                  {
                     "href":"http://192.168.159.128:6385/v1/nodes/1",
                     "rel":"self"
                  },
                  {
                     "href":"http://192.168.159.128:6385/nodes/1",
                     "rel":"bookmark"
                  }
               ],
               "driver_info":{
                  "pxe_image_source":"6e862337-0dac-4af3-9ef0-635e4389c982",
                  "ssh_virt_type":"virsh",
                  "pxe_root_gb":"10",
                  "ssh_port":"22",
                  "ssh_username":"stack",
                  "pxe_deploy_key":"V0ABT9NKVTNBDXEUA9HOIKDV5FV8OQXE",
                  "pxe_deploy_ramdisk":"c1d57373-b909-4dc6-a484-5159315e99f7",
                  "ssh_key_filename":"/opt/stack/data/ironic/ssh_keys/key",
                  "ssh_address":"192.168.159.128",
                  "pxe_deploy_kernel":"5faf2b8c-ceee-4caa-a6d2-a16678668168",
                  "pxe_swap_mb":"0"
               },
               "extra":{
                  "key1":"value1"
               },
               "last_error":null,
               "console_enabled":false,
               "target_provision_state":null,
               "driver":"pxe_ssh",
               "updated_at":"2014-04-01T02:09:25+00:00",
               "ports":[
                  {
                     "href":"http://192.168.159.128:6385/v1/nodes/1/ports",
                     "rel":"self"
                  },
                  {
                     "href":"http://192.168.159.128:6385/nodes/1/ports",
                     "rel":"bookmark"
                  }
               ],
               "provision_updated_at":"2014-04-01T01:58:58+00:00",
               "chassis_uuid":"c14437c0-f498-4fb8-84e2-4d88e10e3d0c",
               "provision_state":"active",
               "reservation":"localhost",
               "power_state":"power on",
               "created_at":"2014-04-01T01:53:48+00:00",
               "uuid":"4353282d-7ae6-4b77-aec7-172555333bfa"
            }
            """
        cls.node = Node.deserialize(cls.node_json, 'json')

    def test_instance_uuid(self):
        self.assertEqual(
            self.node.instance_uuid, "3b209332-d933-4db2-9afd-8a0d7824e7c1")

    def test_target_power_state(self):
        self.assertIsNone(self.node.target_power_state)

    def test_node_links(self):
        self.assertEqual(len(self.node.links), 2)

        for link in self.node.links:
            self.assertIn(link.rel, ['self', 'bookmark'])
            if link.rel == 'bookmark':
                self.assertEqual(
                    link.href,
                    'http://192.168.159.128:6385/nodes/1')
            else:
                self.assertEqual(
                    link.href,
                    'http://192.168.159.128:6385/v1/nodes/1')

    def test_properties(self):
        self.assertEqual(len(self.node.properties), 4)
        self.assertEqual(self.node.properties.get('memory_mb'), "512")
        self.assertEqual(self.node.properties.get('cpu_arch'), "x86_64")
        self.assertEqual(self.node.properties.get('local_gb'), "10")
        self.assertEqual(self.node.properties.get('cpus'), "1")

    def test_maintenance(self):
        self.assertFalse(self.node.maintenance)

    def test_driver_info(self):
        self.assertEqual(len(self.node.driver_info), 11)
        self.assertEqual(
            self.node.driver_info.get('pxe_image_source'),
            '6e862337-0dac-4af3-9ef0-635e4389c982')
        self.assertEqual(self.node.driver_info.get('ssh_virt_type'), 'virsh')
        self.assertEqual(self.node.driver_info.get('pxe_root_gb'), '10')
        self.assertEqual(self.node.driver_info.get('ssh_port'), '22')
        self.assertEqual(self.node.driver_info.get('ssh_username'), 'stack')
        self.assertEqual(
            self.node.driver_info.get('pxe_deploy_key'),
            'V0ABT9NKVTNBDXEUA9HOIKDV5FV8OQXE')
        self.assertEqual(
            self.node.driver_info.get('pxe_deploy_ramdisk'),
            'c1d57373-b909-4dc6-a484-5159315e99f7')
        self.assertEqual(
            self.node.driver_info.get('ssh_key_filename'),
            '/opt/stack/data/ironic/ssh_keys/key')
        self.assertEqual(
            self.node.driver_info.get('ssh_address'),
            '192.168.159.128')
        self.assertEqual(
            self.node.driver_info.get('pxe_deploy_kernel'),
            '5faf2b8c-ceee-4caa-a6d2-a16678668168')
        self.assertEqual(self.node.driver_info.get('pxe_swap_mb'), '0')

    def test_node_extra_info(self):
        self.assertEqual(len(self.node.extra), 1)
        self.assertEqual(self.node.extra.get('key1'), 'value1')

    def test_node_last_error(self):
        self.assertIsNone(self.node.last_error)

    def test_node_console_enabled(self):
        self.assertFalse(self.node.console_enabled)

    def test_node_target_provision_state(self):
        self.assertIsNone(self.node.target_provision_state)

    def test_node_driver(self):
        self.assertEqual(self.node.driver, 'pxe_ssh')

    def test_node_updated_at(self):
        self.assertEqual(self.node.updated_at, '2014-04-01T02:09:25+00:00')

    def test_node_ports(self):
        self.assertEqual(len(self.node.ports), 2)
        for port in self.node.ports:
            self.assertIn(port.rel, ['self', 'bookmark'])

            if port.rel == 'bookmark':
                self.assertEqual(
                    port.href,
                    'http://192.168.159.128:6385/nodes/1/ports')
            else:
                self.assertEqual(
                    port.href,
                    'http://192.168.159.128:6385/v1/nodes/1/ports')

    def test_node_provision_updated_at(self):
        self.assertEqual(
            self.node.provision_updated_at, '2014-04-01T01:58:58+00:00')

    def test_node_chassis_id(self):
        self.assertEqual(
            self.node.chassis_uuid, 'c14437c0-f498-4fb8-84e2-4d88e10e3d0c')

    def test_node_provision_state(self):
        self.assertEqual(self.node.provision_state, 'active')

    def test_node_reservation(self):
        self.assertEqual(self.node.reservation, 'localhost')

    def test_node_power_state(self):
        self.assertEqual(self.node.power_state, 'power on')

    def test_node_created_at(self):
        self.assertEqual(self.node.created_at, '2014-04-01T01:53:48+00:00')

    def test_node_uuid(self):
        self.assertEqual(
            self.node.uuid, '4353282d-7ae6-4b77-aec7-172555333bfa')


class NodesDriverInterfacesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver_interfaces_json = \
            """
            {
                "console": {"reason": "not supported", "result": null},
                "power": {"result": true},
                "deploy": {"result": true}
            }
            """
        cls.driver_interfaces = DriverInterfaces.deserialize(
            cls.driver_interfaces_json, 'json')

    def test_console_result(self):
        self.assertIsNotNone(self.driver_interfaces.console)
        self.assertEqual(
            self.driver_interfaces.console.reason, 'not supported')
        self.assertIsNone(self.driver_interfaces.console.result)

    def test_power_result(self):
        self.assertIsNotNone(self.driver_interfaces.power)
        self.assertTrue(self.driver_interfaces.power.result)

    def test_deploy_result(self):
        self.assertIsNotNone(self.driver_interfaces.deploy)
        self.assertTrue(self.driver_interfaces.deploy.result)
