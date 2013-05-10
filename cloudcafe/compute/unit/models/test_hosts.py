import unittest2 as unittest

from cloudcafe.compute.hosts_api.models.hosts import Host


class HostDomainTest(object):

    def test_host_name(self):
        self.assertEqual(self.host.name, "host_name")

    def test_host_service(self):
        self.assertEqual(self.host.service, "compute")

    def test_host_zone(self):
        self.assertEqual(self.host.zone, "nova")


class HostDomainJSONTest(unittest.TestCase, HostDomainTest):

    @classmethod
    def setUp(cls):
        cls.host_json = '{"host":{"host_name":' \
                        ' "host_name","service":' \
                        ' "compute","zone": "nova"}}'
        cls.host = Host.deserialize(cls.host_json, "json")


class HostDomainXMLTest(unittest.TestCase, HostDomainTest):

    @classmethod
    def setUp(cls):
        cls.host_xml = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<host host_name="host_name"' \
                       ' service="compute" zone="nova"/>'
        cls.host = Host.deserialize(cls.host_xml, "xml")


class HostDomainCollectionTest(object):

    def test_hosts_length(self):
        self.assertEqual(len(self.hosts), 2)

    def test_host_names(self):
        self.assertEqual(self.hosts[0].name, "host_name1")
        self.assertEqual(self.hosts[1].name, "host_name2")

    def test_host_services(self):
        self.assertEqual(self.hosts[0].service, "compute1")
        self.assertEqual(self.hosts[1].service, "compute2")

    def test_host_zones(self):
        self.assertEqual(self.hosts[0].zone, "nova1")
        self.assertEqual(self.hosts[1].zone, "nova2")


class HostDomainCollectionJSONTest(unittest.TestCase,
                                   HostDomainCollectionTest):

    @classmethod
    def setUp(cls):
        cls.hosts_json = '{"hosts":' \
                         '[{"host":{"host_name":' \
                         ' "host_name1","service": "compute1",' \
                         '"zone": "nova1"}},' \
                         '{"host":{"host_name": "host_name2",' \
                         '"service": "compute2","zone": "nova2"}}]}'
        cls.hosts = Host.deserialize(cls.hosts_json, "json")


class HostDomainCollectionXMLTest(unittest.TestCase, HostDomainCollectionTest):

    @classmethod
    def setUp(cls):
        cls.hosts_xml = '<?xml version="1.0" encoding="UTF-8"?>' \
                        '<hosts>' \
                        '<host host_name="host_name1" ' \
                        'service="compute1" zone="nova1"/>' \
                        '<host host_name="host_name2"' \
                        ' service="compute2" zone="nova2"/>' \
                        '</hosts>'
        cls.hosts = Host.deserialize(cls.hosts_xml, "xml")


if __name__ == '__main__':
    unittest.main()
