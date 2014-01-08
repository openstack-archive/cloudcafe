#from json import loads
import unittest
import json
import logging
from cloudcafe.blockstorage.volumes_api.v1.models import responses

logging.getLogger('').addHandler(logging.StreamHandler())


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
                xmlns="http://docs.openstack.org/fake"
                id="{id_}" name="{name}">
                <extra_specs>
                    <extra_spec key="{spec_key}">{spec_value}</extra_spec>
                </extra_specs>
            </volume_type>"""

    serialized_input = input_template.format(
        xml_header=xml_header, id_=defaults.id_, name=defaults.name,
        spec_key=defaults.extra_specs_key,
        spec_value=defaults.extra_specs_value)


class VolumeSnapshotResponseModelBaseTest(BaseTest):
    model_type = responses.VolumeSnapshotResponse

    class defaults:
        status = 'creating'
        display_description = 'fake snapshot description'
        created_at = "2013-02-25T03:56:53.081642"
        metadata_key = "MetaKey"
        metadata_value = "MetaValue"
        volume_id = "3242343242342342f32f324f3f"
        size = 1
        id_ = "2305iu32f9j3298f4jh32498fj"
        display_name = "FakeSnapshotName"

    def test_id(self):
        self.assertEquals(self.model.id_, self.defaults.id_)

    def test_volume_id(self):
        self.assertEquals(self.model.volume_id, self.defaults.volume_id)

    def test_display_name(self):
        self.assertEquals(self.model.display_name, self.defaults.display_name)

    def test_display_description(self):
        self.assertEquals(
            self.model.display_description, self.defaults.display_description)

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


class VolumeSnapshotResponseModelTests_JSON(
        VolumeSnapshotResponseModelBaseTest, unittest.TestCase):

    defaults = VolumeSnapshotResponseModelBaseTest.defaults
    deserialize_type = 'json'
    data = {
        "snapshot": {
            "status": defaults.status,
            "display_description": defaults.display_description,
            "created_at": defaults.created_at,
            "metadata": {defaults.metadata_key: defaults.metadata_value},
            "volume_id": defaults.volume_id,
            "size": defaults.size,
            "id": defaults.id_,
            "display_name": defaults.display_name}}
    serialized_input = json.dumps(data)


class VolumeSnapshotResponseModelTests_XML(
        VolumeSnapshotResponseModelBaseTest, unittest.TestCase):

    defaults = VolumeSnapshotResponseModelBaseTest.defaults
    deserialize_type = 'xml'
    xml_header = """<?xml version="1.0" encoding="UTF-8"?>"""
    input_template = \
        """{xml_header}<snapshot
               status="{status}"
               display_description="{display_description}"
               created_at="{created_at}"
               volume_id="{volume_id}"
               size="{size}"
               id="{id_}"
               display_name="{display_name}">
               <metadata>
                   <meta key="{metadata_key}">{metadata_value}</meta>
               </metadata>
           </snapshot>"""
    serialized_input = input_template.format(
        xml_header=xml_header, status=defaults.status,
        display_description=defaults.display_description,
        created_at=defaults.created_at, volume_id=defaults.volume_id,
        size=defaults.size, id_=defaults.id_,
        display_name=defaults.display_name, metadata_key=defaults.metadata_key,
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
        display_description = "Super volume."
        bootable = "true"
        display_name = "vol-002"
        created_at = "2013-02-25T02:40:21.000000"
        volume_type = "None"
        os_vol_tenant_attr_tenant_id = "0c2eba2c5af04d3f9e9d0d410b371fde"
        os_vol_host_attr_host = "ip-10-168-107-25"
        size = 1
        metadata_key = "MetaKey"
        metadata_value = "MetaValue"

    def test_id(self):
        self.assertEquals(self.model.id_, self.defaults.id_)

    def test_size_int_equivalent(self):
        self.assertEquals(int(self.model.size), self.defaults.size)

    def test_size_str_compare(self):
        self.assertEquals(str(self.model.size), str(self.defaults.size))

    def test_size_int_compare(self):
        self.assertEquals(int(self.model.size), int(self.defaults.size))

    def test_display_name(self):
        self.assertEquals(self.model.display_name, self.defaults.display_name)

    def test_volume_type(self):
        self.assertEquals(
            self.model.volume_type, self.defaults.volume_type)

    def test_display_description(self):
        self.assertEquals(
            self.model.display_description, self.defaults.display_description)

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
            "snapshot_id": defaults.snapshot_id,
            "id": defaults.id_,
            "display_description": defaults.display_description,
            "display_name": defaults.display_name,
            "created_at": defaults.created_at,
            "volume_type": defaults.volume_type,
            "size": defaults.size,
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
                xmlns:atom="http://www.w3.org/2005/Atom"
                xmlns="http://docs.openstack.org/volume/api/v1"
                status="{status}"
                display_name="{display_name}"
                availability_zone="{availability_zone}"
                created_at="{created_at}"
                display_description="{display_description}"
                volume_type="{volume_type}"
                snapshot_id="{snapshot_id}"
                id="{id_}"
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
        xml_header=xml_header, status=defaults.status,
        display_name=defaults.display_name,
        availability_zone=defaults.availability_zone,
        created_at=defaults.created_at,
        display_description=defaults.display_description,
        volume_type=defaults.volume_type, snapshot_id=defaults.snapshot_id,
        id_=defaults.id_, size=defaults.size,
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

    @unittest.skip("There are no XML examples of links in XML responses")
    def test_empty_links_response(self):
        pass

    def test_empty_attachments_response(self):
        serialized_input = """{xml_header}<volume
                xmlns:atom="http://www.w3.org/2005/Atom"
                xmlns="http://docs.openstack.org/volume/api/v1"
                status="{status}"
                display_name="{display_name}"
                availability_zone="{availability_zone}"
                created_at="{created_at}"
                display_description="{display_description}"
                volume_type="{volume_type}"
                snapshot_id="{snapshot_id}"
                id="{id_}"
                size="{size}">
            <metadata>
                <meta key="{metadata_key}">{metadata_value}</meta>
            </metadata>
        </volume>""".format(
            xml_header=self.xml_header,
            status=self.defaults.status,
            display_name=self.defaults.display_name,
            availability_zone=self.defaults.availability_zone,
            created_at=self.defaults.created_at,
            display_description=self.defaults.display_description,
            volume_type=self.defaults.volume_type,
            snapshot_id=self.defaults.snapshot_id,
            id_=self.defaults.id_,
            size=self.defaults.size,
            metadata_key=self.defaults.metadata_key,
            metadata_value=self.defaults.metadata_value)

        self.model = self.model_type.deserialize(
            serialized_input, self.deserialize_type)
        self.assertEquals(self.model.attachments, [])
        self.assertIsInstance(
            self.model.attachments, responses._VolumeAttachmentsList)

    def test_empty_metadata_response(self):
        serialized_input = """{xml_header}<volume
                xmlns:atom="http://www.w3.org/2005/Atom"
                xmlns="http://docs.openstack.org/volume/api/v1"
                status="{status}"
                display_name="{display_name}"
                availability_zone="{availability_zone}"
                created_at="{created_at}"
                display_description="{display_description}"
                volume_type="{volume_type}"
                snapshot_id="{snapshot_id}"
                id="{id_}"
                size="{size}">
        </volume>""".format(
            xml_header=self.xml_header,
            status=self.defaults.status,
            display_name=self.defaults.display_name,
            availability_zone=self.defaults.availability_zone,
            created_at=self.defaults.created_at,
            display_description=self.defaults.display_description,
            volume_type=self.defaults.volume_type,
            snapshot_id=self.defaults.snapshot_id,
            id_=self.defaults.id_,
            size=self.defaults.size)

        self.model = self.model_type.deserialize(
            serialized_input, self.deserialize_type)
        self.assertEquals(self.model.metadata, {})
