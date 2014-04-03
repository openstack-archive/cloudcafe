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

from cloudcafe.bare_metal.drivers.models.responses import Driver, Drivers


class DriversModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.drivers_json_response = \
            """
            {
               "drivers":[
                  {
                     "hosts":[
                        "localhost"
                     ],
                     "name":"fake_ipminative",
                     "links":[
                        {
                           "href":"http://local:6385/v1/drivers/ipminative",
                           "rel":"self"
                        },
                        {
                           "href":"http://local:6385/drivers/ipminative",
                           "rel":"bookmark"
                        }
                     ]
                  },
                  {
                     "hosts":[
                        "localhost"
                     ],
                     "name":"p_ipminative",
                     "links":[
                        {
                           "href":"http://local:6385/v1/drivers/p_ipminative",
                           "rel":"self"
                        },
                        {
                           "href":"http://local:6385/drivers/p_ipminative",
                           "rel":"bookmark"
                        }
                     ]
                  },
                  {
                     "hosts":[
                        "localhost"
                     ],
                     "name":"fake_pxe",
                     "links":[
                        {
                           "href":"http://local:6385/v1/drivers/fake_pxe",
                           "rel":"self"
                        },
                        {
                           "href":"http://local:6385/drivers/fake_pxe",
                           "rel":"bookmark"
                        }
                     ]
                  },
                  {
                     "hosts":[
                        "localhost"
                     ],
                     "name":"fake_ssh",
                     "links":[
                        {
                           "href":"http://local:6385/v1/drivers/fake_ssh",
                           "rel":"self"
                        },
                        {
                           "href":"http://local:6385/drivers/fake_ssh",
                           "rel":"bookmark"
                        }
                     ]
                  },
                  {
                     "hosts":[
                        "localhost"
                     ],
                     "name":"fake_ipmitool",
                     "links":[
                        {
                           "href":"http://local:6385/v1/drivers/fake_ipmitool",
                           "rel":"self"
                        },
                        {
                           "href":"http://local:6385/drivers/fake_ipmitool",
                           "rel":"bookmark"
                        }
                     ]
                  },
                  {
                     "hosts":[
                        "localhost"
                     ],
                     "name":"fake",
                     "links":[
                        {
                           "href":"http://local:6385/v1/drivers/fake",
                           "rel":"self"
                        },
                        {
                           "href":"http://local:6385/drivers/fake",
                           "rel":"bookmark"
                        }
                     ]
                  },
                  {
                     "hosts":[
                        "localhost"
                     ],
                     "name":"pxe_ssh",
                     "links":[
                        {
                           "href":"http://local:6385/v1/drivers/pxe_ssh",
                           "rel":"self"
                        },
                        {
                           "href":"http://local:6385/drivers/pxe_ssh",
                           "rel":"bookmark"
                        }
                     ]
                  },
                  {
                     "hosts":[
                        "localhost"
                     ],
                     "name":"pxe_ipmitool",
                     "links":[
                        {
                           "href":"http://local:6385/v1/drivers/pxe_ipmitool",
                           "rel":"self"
                        },
                        {
                           "href":"http://local:6385/drivers/pxe_ipmitool",
                           "rel":"bookmark"
                        }
                     ]
                  }
               ]
            }
            """
        cls.drivers = Drivers.deserialize(cls.drivers_json_response, 'json')

    def test_list_drivers(self):
        self.assertEqual(len(self.drivers), 8)

    def test_drivers_in_list(self):
        self.assertTrue(
            any([driver for driver in self.drivers
                 if driver.name == 'fake_ipminative']))
        self.assertTrue(
            any([driver for driver in self.drivers
                 if driver.name == 'p_ipminative']))
        self.assertTrue(
            any([driver for driver in self.drivers
                 if driver.name == 'fake_pxe']))
        self.assertTrue(
            any([driver for driver in self.drivers
                 if driver.name == 'fake_ssh']))
        self.assertTrue(
            any([driver for driver in self.drivers
                 if driver.name == 'fake_ipmitool']))
        self.assertTrue(
            any([driver for driver in self.drivers
                 if driver.name == 'fake']))
        self.assertTrue(
            any([driver for driver in self.drivers
                 if driver.name == 'pxe_ssh']))
        self.assertTrue(
            any([driver for driver in self.drivers
                 if driver.name == 'pxe_ipmitool']))


class DriverModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver_json_response = \
            """
            {
               "hosts":[
                  "localhost"
               ],
               "name":"fake",
               "links":[
                  {
                     "href":"http://192.168.159.128:6385/v1/drivers/fake",
                     "rel":"self"
                  },
                  {
                     "href":"http://192.168.159.128:6385/drivers/fake",
                     "rel":"bookmark"
                  }
               ]
            }
            """
        cls.driver = Driver.deserialize(cls.driver_json_response, 'json')

    def test_driver_name(self):
        self.assertEqual(self.driver.name, "fake")

    def test_driver_hosts(self):
        self.assertEqual(len(self.driver.hosts), 1)
        self.assertIn('localhost', self.driver.hosts)

    def test_driver_links(self):
        self.assertEqual(len(self.driver.links), 2)

        for driver in self.driver.links:
            self.assertIn(driver.rel, ['self', 'bookmark'])

            if driver.rel == 'bookmark':
                self.assertEqual(
                    driver.href,
                    'http://192.168.159.128:6385/drivers/fake')
            else:
                self.assertEqual(
                    driver.href,
                    'http://192.168.159.128:6385/v1/drivers/fake')
