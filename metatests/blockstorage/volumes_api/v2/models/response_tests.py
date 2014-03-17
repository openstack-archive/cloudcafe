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
import json
from cloudcafe.blockstorage.volumes_api.v2.models import responses


class BaseTest(object):

    @classmethod
    def setUpClass(cls):
        cls.model = cls.model_type.deserialize(
            cls.serialized_input, cls.deserialize_type)


class VolumeTypeResponseModelBaseTest(BaseTest):
    model_type = responses.VolumeTypeResponse

    class defaults:
        id_ = "32948732984798324"
        name = "fake name"
        extra_specs_key = "ExtraSpecsKey"
        extra_specs_value = "ExtraSpecsValue"

    def test_id(self):
        self.assertEquals(self.model.id_, self.defaults.id_)

    def test_name(self):
        self.assertEquals(self.model.name, self.defaults.name)

    def test_extra_specs(self):
        self.assertEquals(
            self.model.extra_specs,
            {self.defaults.extra_specs_key: self.defaults.extra_specs_value})


class VolumeTypeResponseModelTest_JSON(
        VolumeTypeResponseModelBaseTest, unittest.TestCase):
    defaults = VolumeTypeResponseModelBaseTest.defaults
    deserialize_type = 'json'
    data = {
        "volume_type": {
            "id": defaults.id_,
            "name": defaults.name,
            "extra_specs": {
                defaults.extra_specs_key: defaults.extra_specs_value}}}
    serialized_input = json.dumps(data)


class VolumeTypeResponseModelTest_XML(
        VolumeTypeResponseModelBaseTest, unittest.TestCase):
    defaults = VolumeTypeResponseModelBaseTest.defaults
    xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""
    deserialize_type = 'xml'
    input_template = \
        """{xml_header}<volume_type
                xmlns="http://docs.openstack.org/fakeVolRespModelxmlns"
                id="{id_}" name="{name}">
                <extra_specs>
                    <extra_spec key="{spec_key}">{spec_value}</extra_spec>
                </extra_specs>
            </volume_type>"""

    serialized_input = input_template.format(
        xml_header=xml_header,
        id_=defaults.id_, name=defaults.name,
        spec_key=defaults.extra_specs_key,
        spec_value=defaults.extra_specs_value)


class VolumeTypeListResponseModelBaseTest(BaseTest):
    model_type = responses.VolumeTypeListResponse

    class defaults:
        id_ = "32948732984798324"
        name1 = "fake name 1"
        name2 = "fake name 2"
        extra_specs_key = "ExtraSpecsKey"
        extra_specs_value = "ExtraSpecsValue"

    def test_list_contains_two_items(self):
        self.assertEquals(len(self.model), 2)

    def test_first_item_id(self):
        self.assertEquals(self.model[0].id_, self.defaults.id_)

    def test_second_item_id(self):
        self.assertEquals(self.model[1].id_, self.defaults.id_)

    def test_first_item_name(self):
        self.assertEquals(self.model[0].name, self.defaults.name1)

    def test_second_item_name(self):
        self.assertEquals(self.model[1].name, self.defaults.name2)

    def test_first_item_extra_specs(self):
        self.assertEquals(self.model[0].extra_specs, {
            self.defaults.extra_specs_key:
            self.defaults.extra_specs_value})

    def test_second_item_extra_specs(self):
        self.assertEquals(self.model[1].extra_specs, {
            self.defaults.extra_specs_key:
            self.defaults.extra_specs_value})


class VolumeTypeListResponseModelTest_XML(
        VolumeTypeListResponseModelBaseTest, unittest.TestCase):
    defaults = VolumeTypeListResponseModelBaseTest.defaults
    xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""
    deserialize_type = 'xml'
    input_template = \
        """{xml_header}<volume_types>
            <volume_type
                id="{id_}"
                name="{name1}">
                <extra_specs>
                    <extra_spec key="{spec_key}">{spec_value}</extra_spec>
                </extra_specs>
            </volume_type>
            <volume_type
                id="{id_}"
                name="{name2}">
                <extra_specs>
                    <extra_spec key="{spec_key}">{spec_value}</extra_spec>
                </extra_specs>
            </volume_type>
        </volume_types>
        """
    serialized_input = input_template.format(
        xml_header=xml_header,
        id_=defaults.id_,
        name1=defaults.name1,
        name2=defaults.name2,
        spec_key=defaults.extra_specs_key,
        spec_value=defaults.extra_specs_value)


class VolumeSnapshotResponseModelBaseTest(BaseTest):
    model_type = responses.VolumeSnapshotResponse

    class defaults:
        status = 'creating'
        description = 'fake snapshot description'
        created_at = "2013-02-25T03:56:53.081642"
        metadata_key = "MetaKey"
        metadata_value = "MetaValue"
        volume_id = "3242343242342342f32f324f3f"
        size = 1
        id_ = "2305iu32f9j3298f4jh32498fj"
        name = "FakeSnapshotName"
        os_extended_snapshot_attributes_project_id = '1111111'
        os_extended_snapshot_attributes_progress = '100%'

    def test_id(self):
        self.assertEquals(self.model.id_, self.defaults.id_)

    def test_volume_id(self):
        self.assertEquals(self.model.volume_id, self.defaults.volume_id)

    def test_name(self):
        self.assertEquals(self.model.name, self.defaults.name)

    def test_description(self):
        self.assertEquals(self.model.description, self.defaults.description)

    def test_status(self):
        self.assertEquals(self.model.status, self.defaults.status)

    def test_size_int_equivalent(self):
        self.assertEquals(int(self.model.size), self.defaults.size)

    def test_size_str_compare(self):
        self.assertEquals(str(self.model.size), str(self.defaults.size))

    def test_size_int_compare(self):
        self.assertEquals(int(self.model.size), int(self.defaults.size))

    def test_created_at(self):
        self.assertEquals(self.model.created_at, self.defaults.created_at)

    def test_metadata(self):
        self.assertEquals(
            self.model.metadata,
            {self.defaults.metadata_key: self.defaults.metadata_value})

    def test_os_extended_snapshot_attributes_project_id(self):
        self.assertEquals(
            self.model.os_extended_snapshot_attributes_project_id,
            self.defaults.os_extended_snapshot_attributes_project_id)

    def test_os_extended_snapshot_attributes_progress(self):
        self.assertEquals(
            self.model.os_extended_snapshot_attributes_progress,
            self.defaults.os_extended_snapshot_attributes_progress)


class VolumeSnapshotResponseModelTests_JSON(
        VolumeSnapshotResponseModelBaseTest, unittest.TestCase):

    defaults = VolumeSnapshotResponseModelBaseTest.defaults
    deserialize_type = 'json'
    data = {
        "snapshot": {
            "status": defaults.status,
            "description": defaults.description,
            "created_at": defaults.created_at,
            "metadata": {defaults.metadata_key: defaults.metadata_value},
            "volume_id": defaults.volume_id,
            "size": defaults.size,
            "id": defaults.id_,
            "name": defaults.name,
            "os-extended-snapshot-attributes:project_id": defaults.
            os_extended_snapshot_attributes_project_id,
            "os-extended-snapshot-attributes:progress": defaults.
            os_extended_snapshot_attributes_progress}}
    serialized_input = json.dumps(data)


class VolumeSnapshotResponseModelTests_XML(
        VolumeSnapshotResponseModelBaseTest, unittest.TestCase):

    defaults = VolumeSnapshotResponseModelBaseTest.defaults
    deserialize_type = 'xml'
    xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""
    input_template = \
        """{xml_header}<snapshot
               xmlns:os-extended-snapshot-attributes="FAKE"
               os-extended-snapshot-attributes:project_id="{project_id}"
               os-extended-snapshot-attributes:progress="{progress}"
               status="{status}"
               description="{description}"
               created_at="{created_at}"
               volume_id="{volume_id}"
               size="{size}"
               id="{id_}"
               name="{name}">
               <metadata>
                   <meta key="{metadata_key}">{metadata_value}</meta>
               </metadata>
           </snapshot>"""
    serialized_input = input_template.format(
        project_id=defaults.os_extended_snapshot_attributes_project_id,
        progress=defaults.os_extended_snapshot_attributes_progress,
        xml_header=xml_header,
        status=defaults.status,
        description=defaults.description,
        created_at=defaults.created_at,
        volume_id=defaults.volume_id,
        size=defaults.size,
        id_=defaults.id_,
        name=defaults.name,
        metadata_key=defaults.metadata_key,
        metadata_value=defaults.metadata_value)


class VolumeResponseModelBaseTests(BaseTest):
    model_type = responses.VolumeResponse

    class defaults:
        status = 'available'
        attachment_device = '/dev/xvdg'
        attachment_server_id = u'e335bfc4-5ba0-49b0-9f2b-7bc202583047'
        attachment_id = u'7d4fdc77-8db7-4ba8-9786-c2a265c8b157'
        attachment_volume_id = u'7d4fdc77-8db7-4ba8-9786-c2a265c8b157'
        link_href = "http://localhost:8776/v2/0c2ebfde/volumes/5aa119a8-d35"
        link_rel = 'self'
        availability_zone = "nova"
        source_volid = "1234234234324234"
        snapshot_id = "34545645645646456"
        id_ = "5aa119a8-d25b-45a7-8d1b-88e127885635"
        description = "Super volume."
        bootable = "true"
        name = "vol-002"
        created_at = "2013-02-25T02:40:21.000000"
        volume_type = "None"
        os_vol_tenant_attr_tenant_id = "0c2eba2c5af04d3f9e9d0d410b371fde"
        os_vol_host_attr_host = "ip-10-168-107-25"
        size = 1
        metadata_key = "MetaKey"
        metadata_value = "MetaValue"
        os_vol_mig_status_attr_migstat = '100%'
        os_vol_mig_status_attr_name_id = '1111111'

    def test_id(self):
        self.assertEquals(self.model.id_, self.defaults.id_)

    def test_size_int_equivalent(self):
        self.assertEquals(int(self.model.size), self.defaults.size)

    def test_size_str_compare(self):
        self.assertEquals(str(self.model.size), str(self.defaults.size))

    def test_size_int_compare(self):
        self.assertEquals(int(self.model.size), int(self.defaults.size))

    def test_name(self):
        self.assertEquals(self.model.name, self.defaults.name)

    def test_volume_type(self):
        self.assertEquals(
            self.model.volume_type, self.defaults.volume_type)

    def test_description(self):
        self.assertEquals(
            self.model.description, self.defaults.description)

    def test_availability_zone(self):
        self.assertEquals(
            self.model.availability_zone,
            self.defaults.availability_zone)

    def test_metadata(self):
        self.assertEquals(
            self.model.metadata,
            {self.defaults.metadata_key: self.defaults.metadata_value})

    def test_snapshot_id(self):
        self.assertEquals(
            self.model.snapshot_id, self.defaults.snapshot_id)

    def test_bootable(self):
        self.assertEquals(
            self.model.bootable, self.defaults.bootable)

    def test_attachments_device(self):
        self.assertEquals(
            self.model.attachments[0].device,
            self.defaults.attachment_device)

    def test_attachments_server_id(self):
        self.assertEquals(
            self.model.attachments[0].server_id,
            self.defaults.attachment_server_id)

    def test_attachments_id(self):
        self.assertEquals(
            self.model.attachments[0].id_,
            self.defaults.attachment_id)

    def test_attachments_volume_id(self):
        self.assertEquals(
            self.model.attachments[0].volume_id,
            self.defaults.attachment_volume_id)

    def test_created_at(self):
        self.assertEquals(
            self.model.created_at,
            self.defaults.created_at)

    def test_status(self):
        self.assertEquals(
            self.model.status,
            self.defaults.status)

    def test_links_href(self):
        self.assertEquals(
            self.model.links[0].href,
            self.defaults.link_href)

    def test_links_rel(self):
        self.assertEquals(
            self.model.links[0].rel,
            self.defaults.link_rel)

    def test_source_volid(self):
        self.assertEquals(
            self.model.source_volid,
            self.defaults.source_volid)

    def test_os_vol_host_attr_host(self):
        self.assertEquals(
            self.model.os_vol_host_attr_host,
            self.defaults.os_vol_host_attr_host)

    def test_os_vol_tenant_attr_tenant_id(self):
        self.assertEquals(
            self.model.os_vol_tenant_attr_tenant_id,
            self.defaults.os_vol_tenant_attr_tenant_id)

    def test_os_vol_mig_status_attr_migstat(self):
        self.assertEquals(
            self.model.os_vol_mig_status_attr_migstat,
            self.defaults.os_vol_mig_status_attr_migstat)

    def test_os_vol_mig_status_attr_name_id(self):
        self.assertEquals(
            self.model.os_vol_mig_status_attr_name_id,
            self.defaults.os_vol_mig_status_attr_name_id)


class VolumeResponseModelTests_JSON(
        VolumeResponseModelBaseTests, unittest.TestCase):

    defaults = VolumeResponseModelBaseTests.defaults
    deserialize_type = 'json'
    data = {
        "volume": {
            "status": defaults.status,
            "attachments": [
                {u'device': defaults.attachment_device,
                 u'server_id': defaults.attachment_server_id,
                 u'id': defaults.attachment_id,
                 u'volume_id': defaults.attachment_volume_id}],
            "links": [{
                "href": defaults.link_href,
                "rel": defaults.link_rel}],
            "availability_zone": defaults.availability_zone,
            "os-vol-host-attr:host": defaults.os_vol_host_attr_host,
            "source_volid": defaults.source_volid,
            "snapshot_id": defaults.snapshot_id,
            "id": defaults.id_,
            "description": defaults.description,
            "bootable": defaults.bootable,
            "name": defaults.name,
            "created_at": defaults.created_at,
            "volume_type": defaults.volume_type,
            "os-vol-tenant-attr:tenant_id":
            defaults.os_vol_tenant_attr_tenant_id,
            "size": defaults.size,
            "os-vol-mig-status-attr:migstat":
            defaults.os_vol_mig_status_attr_migstat,
            "os-vol-mig-status-attr:name_id":
            defaults.os_vol_mig_status_attr_name_id,
            "metadata": {defaults.metadata_key: defaults.metadata_value}}}
    serialized_input = json.dumps(data)

    def get_modified_volume_model(self, sub_attr_name, new_object):
        modified_data = dict()
        modified_data['volume'] = self.data['volume']
        modified_data['volume'][sub_attr_name] = new_object
        serialized_input = json.dumps(modified_data)
        model = self.model_type.deserialize(
            serialized_input, self.deserialize_type)
        return model

    def test_empty_attachments_response(self):
        model = self.get_modified_volume_model('attachments', list())
        self.assertEquals(model.attachments, list())
        self.assertIsInstance(
            model.attachments, responses._VolumeAttachmentsList)

    def test_empty_links_response(self):
        model = self.get_modified_volume_model('links', list())
        self.assertEquals(model.links, list())
        self.assertIsInstance(
            model.attachments, responses._VolumeAttachmentsList)

    def test_empty_metadata_response(self):
        model = self.get_modified_volume_model('metadata', dict())
        self.assertEquals(model.metadata, dict())


class VolumeDetailResponseModelTests_XML(
        VolumeResponseModelBaseTests, unittest.TestCase):

    defaults = VolumeResponseModelBaseTests.defaults
    deserialize_type = 'xml'
    xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""
    input_template = \
        """{xml_header}<volume
                xmlns:os-vol-image-meta="http://fake/api/v1"
                xmlns:os-vol-tenant-attr="FAKE"
                xmlns:os-vol-host-attr="FAKE"
                xmlns:os-vol-mig-status-attr="FAKE"
                xmlns:atom="http://www.w3.org/2005/Atom"
                xmlns="http://docs.openstack.org/volume/api/v1"
                status="{status}"
                name="{name}"
                bootable="{bootable}"
                availability_zone="{availability_zone}"
                created_at="{created_at}"
                description="{description}"
                volume_type="{volume_type}"
                snapshot_id="{snapshot_id}"
                source_volid="{source_volid}"
                id="{id_}"
                os-vol-tenant-attr:tenant_id="{os_vol_tenant_attr_tenant_id}"
                os-vol-host-attr:host="{os_vol_host_attr_host}"
                os-vol-mig-status-attr:migstat="{migstat}"
                os-vol-mig-status-attr:name_id="{name_id}"
                size="{size}">
            <attachments>
                <attachment device="{attachment_device}"
                            server_id="{attachment_server_id}"
                            id="{attachment_id}"
                            volume_id="{attachment_volume_id}"
                />
            </attachments>
            <metadata>
                <meta key="{metadata_key}">{metadata_value}</meta>
            </metadata>
        </volume>"""

    serialized_input = input_template.format(
        xml_header=xml_header,
        status=defaults.status,
        name=defaults.name,
        bootable=defaults.bootable,
        availability_zone=defaults.availability_zone,
        created_at=defaults.created_at,
        description=defaults.description,
        volume_type=defaults.volume_type,
        snapshot_id=defaults.snapshot_id,
        source_volid=defaults.source_volid,
        id_=defaults.id_,
        size=defaults.size,
        os_vol_tenant_attr_tenant_id=defaults.os_vol_tenant_attr_tenant_id,
        os_vol_host_attr_host=defaults.os_vol_host_attr_host,
        migstat=defaults.os_vol_mig_status_attr_migstat,
        name_id=defaults.os_vol_mig_status_attr_name_id,
        attachment_device=defaults.attachment_device,
        attachment_server_id=defaults.attachment_server_id,
        attachment_id=defaults.attachment_id,
        attachment_volume_id=defaults.attachment_volume_id,
        metadata_key=defaults.metadata_key,
        metadata_value=defaults.metadata_value)

    @unittest.skip("There are no XML examples of links in XML responses")
    def test_links_href(self):
        super(VolumeDetailResponseModelTests_XML, self).test_links_href()

    @unittest.skip("There are no XML examples of links in XML responses")
    def test_links_rel(self):
        super(VolumeDetailResponseModelTests_XML, self).test_links_href()
