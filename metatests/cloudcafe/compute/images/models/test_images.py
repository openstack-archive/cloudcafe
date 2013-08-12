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

from cloudcafe.compute.images_api.models.image import Image
import unittest2 as unittest


class ImageDomainTest(object):

    def test_image_disk_config(self):
        self.assertEqual(self.image.diskConfig, "AUTO")

    def test_image_id(self):
        self.assertEqual(self.image.id, "a10eacf7-ac15-4225-b533-5744f1fe47c1")

    def test_image_name(self):
        self.assertEqual(self.image.name, "Debian 6 (Squeeze)")

    def test_image_status(self):
        self.assertEqual(self.image.status, "ACTIVE")

    def test_image_updated_time(self):
        self.assertEqual(self.image.updated, "2012-06-29T17:38:26Z")

    def test_image_created_time(self):
        self.assertEqual(self.image.created, "2012-06-29T17:38:07Z")

    def test_image_min_disk(self):
        self.assertEqual(self.image.minDisk, 10)

    def test_image_min_ram(self):
        self.assertEqual(self.image.minRam, 256)

    def test_image_progress(self):
        self.assertEqual(self.image.progress, 100)

    def test_image_links(self):
        base_url = 'https://preprod.ord.servers.api.rackspacecloud.com'
        resource_path = '5825921/images/a10eacf7-ac15-4225-b533-5744f1fe47c1'

        self.assertEqual(
            self.image.links.self, "{base_url}/v2/{resource_path}".format(
                base_url=base_url, resource_path=resource_path))
        self.assertEqual(self.image.links.bookmark,
                         "{base_url}/{resource_path}".format(
                             base_url=base_url, resource_path=resource_path))


class ImageXMLDomainTest(unittest.TestCase, ImageDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.image_xml = \
            ('<image xmlns:OS-DCF="http://docs.openstack.org/compute/'
             'ext/disk_config/api/v1.1" xmlns:atom="http://www.w3.org/'
             '2005/Atom" xmlns="http://docs.openstack.org/compute/api/v1.1"'
             'status="ACTIVE" updated="2012-06-29T17:38:26Z" '
             'name="Debian 6 (Squeeze)" created="2012-06-29T17:38:07Z" '
             'minDisk="10" progress="100" minRam="256" '
             'id="a10eacf7-ac15-4225-b533-5744f1fe47c1" '
             'OS-DCF:diskConfig="AUTO"><metadata>'
             '<meta key="os_distro">debian</meta>'
             '<meta key="com.rackspace__1__visible_core">1</meta>'
             '<meta key="com.rackspace__1__build_rackconnect">1</meta>'
             '<meta key="image_type">base</meta>'
             '<meta key="org.openstack__1__os_version">6.0</meta>'
             '<meta key="org.openstack__1__os_distro">org.debian</meta>'
             '<meta key="rax_managed">false</meta>'
             '<meta key="os_version">6</meta>'
             '<meta key="com.rackspace__1__visible_rackconnect">1</meta>'
             '<meta key="rax_options">0</meta>'
             '<meta key="auto_disk_config">True</meta>'
             '<meta key="com.rackspace__1__options">0</meta>'
             '<meta key="os_type">linux</meta>'
             '<meta key="com.rackspace__1__build_core">1</meta>'
             '<meta key="arch">x86-64</meta>'
             '<meta key="com.rackspace__1__visible_managed">0</meta>'
             '<meta key="org.openstack__1__architecture">x64</meta>'
             '<meta key="com.rackspace__1__build_managed">0</meta>'
             '</metadata><atom:link href="https://preprod.ord.servers.api.'
             'rackspacecloud.com/v2/5825921/images/a10eacf7-ac15-4225-b533'
             '-5744f1fe47c1" rel="self"/><atom:link href="https://preprod.'
             'ord.servers.api.rackspacecloud.com/5825921/images/a10eacf7-'
             'ac15-4225-b533-5744f1fe47c1" rel="bookmark"/><atom:link '
             'href="https://preprod.ord.servers.api.rackspacecloud.com/'
             '5825921/images/a10eacf7-ac15-4225-b533-5744f1fe47c1" '
             'type="application/vnd.openstack.image" rel="alternate"/>'
             '</image>')
        cls.image = Image.deserialize(cls.image_xml, 'xml')


class ImageJSONDomainTest(unittest.TestCase, ImageDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.image_json = \
            ('{"image": {"status": "ACTIVE", "updated":'
             ' "2012-06-29T17:38:26Z", "links": [{"href":'
             '"https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921'
             '/images/a10eacf7-ac15-4225-b533-5744f1fe47c1", "rel": "self"}, '
             '{"href": "https://preprod.ord.servers.api.rackspacecloud.com/'
             '5825921/images/a10eacf7-ac15-4225-b533-5744f1fe47c1", "rel":'
             ' "bookmark"}, {"href": "https://preprod.ord.servers.api.'
             'rackspacecloud.com/5825921/images/a10eacf7-ac15-4225-b533-'
             '5744f1fe47c1", "type": "application/vnd.openstack.image",'
             '"rel": "alternate"}], "minDisk": 10,'
             ' "id": "a10eacf7-ac15-4225-b533-5744f1fe47c1",'
             ' "name": "Debian 6 (Squeeze)", "created":'
             ' "2012-06-29T17:38:07Z", "OS-DCF:diskConfig": "AUTO",'
             ' "progress": 100, "minRam": 256, "metadata": '
             '{"os_distro": "debian", "com.rackspace__1__visible_core": "1",'
             ' "com.rackspace__1__build_rackconnect": "1", '
             '"image_type": "base", "org.openstack__1__os_version": "6.0",'
             ' "org.openstack__1__os_distro": "org.debian", '
             '"rax_managed": "false", "os_version": "6", '
             '"com.rackspace__1__visible_rackconnect": "1", '
             '"rax_options": "0", "auto_disk_config": "True", '
             '"com.rackspace__1__options": "0", "os_type": "linux", '
             '"com.rackspace__1__build_core": "1", "arch": "x86-64", '
             '"com.rackspace__1__visible_managed": "0", '
             '"org.openstack__1__architecture": "x64", '
             '"com.rackspace__1__build_managed": "0"}}}')
        cls.image = Image.deserialize(cls.image_json, 'json')
