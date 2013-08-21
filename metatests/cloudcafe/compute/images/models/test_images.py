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

from cloudcafe.compute.images_api.models.image import Image


class ImageDomainTest(object):

    def test_image_disk_config(self):
        self.assertEqual(self.image.disk_config, "AUTO")

    def test_image_id(self):
        self.assertEqual(self.image.id, "1")

    def test_image_name(self):
        self.assertEqual(self.image.name, "Debian 6 (Squeeze)")

    def test_image_status(self):
        self.assertEqual(self.image.status, "ACTIVE")

    def test_image_updated_time(self):
        self.assertEqual(self.image.updated, "2012-06-29T17:38:26Z")

    def test_image_created_time(self):
        self.assertEqual(self.image.created, "2012-06-29T17:38:07Z")

    def test_image_min_disk(self):
        self.assertEqual(self.image.min_disk, 10)

    def test_image_min_ram(self):
        self.assertEqual(self.image.min_ram, 256)

    def test_image_progress(self):
        self.assertEqual(self.image.progress, 100)

    def test_image_metadata(self):
        self.assertEqual(self.image.metadata.meta1, "value1")
        self.assertEqual(self.image.metadata.meta2, "value2")

    def test_image_links(self):
        base_url = 'https://127.0.0.1'
        resource_path = '600/images/1'

        self.assertEqual(
            self.image.links.self, "{base_url}/v2/{resource_path}".format(
                base_url=base_url, resource_path=resource_path))
        self.assertEqual(self.image.links.bookmark,
                         "{base_url}/{resource_path}".format(
                             base_url=base_url, resource_path=resource_path))


class ImageXMLDomainTest(unittest.TestCase, ImageDomainTest):

    @classmethod
    def setUpClass(cls):
        url = 'http://docs.openstack.org'
        cls.image_xml = \
            """
            <image
            xmlns:OS-DCF="{url}/compute/ext/disk_config/api/v1.1"
            xmlns:atom="http://www.w3.org/2005/Atom"
            xmlns="http://docs.openstack.org/compute/api/v1.1"
            status="ACTIVE" updated="2012-06-29T17:38:26Z"
            name="Debian 6 (Squeeze)"
            created="2012-06-29T17:38:07Z" minDisk="10" progress="100"
            minRam="256" id="1" OS-DCF:diskConfig="AUTO">
            <metadata>
                <meta key="meta1">value1</meta>
                <meta key="meta2">value2</meta>
            </metadata>
            <atom:link href="https://127.0.0.1/v2/600/images/1" rel="self"/>
            <atom:link href="https://127.0.0.1/600/images/1" rel="bookmark"/>
            <atom:link href="https://127.0.0.1/600/images/1"
            type="application/vnd.openstack.image" rel="alternate"/>
            </image>
            """.format(url=url)
        cls.image = Image.deserialize(cls.image_xml, 'xml')


class ImageJSONDomainTest(unittest.TestCase, ImageDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.image_json = \
            """
            {"image":
                {
                    "status": "ACTIVE",
                    "updated": "2012-06-29T17:38:26Z",
                    "links":
                        [{"href": "https://127.0.0.1/v2/600/images/1",
                          "rel": "self"},
                         {"href": "https://127.0.0.1/600/images/1",
                          "rel": "bookmark"},
                         {"href": "https://127.0.0.1/600/images/1",
                          "type": "application/vnd.openstack.image",
                          "rel": "alternate"}],
                    "minDisk": 10,
                    "id": "1",
                    "name": "Debian 6 (Squeeze)",
                    "created": "2012-06-29T17:38:07Z",
                    "OS-DCF:diskConfig": "AUTO",
                    "progress": 100,
                    "minRam": 256,
                    "metadata": {
                        "meta1": "value1",
                        "meta2": "value2"
                    }
                }
            }
            """
        cls.image = Image.deserialize(cls.image_json, 'json')
