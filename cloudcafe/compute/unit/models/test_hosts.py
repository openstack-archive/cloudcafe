import unittest2 as unittest

from cloudcafe.compute.hosts_api.models.hosts import Host


class HostDomainTest(object):

    def test_resource_length(self):
        self.assertTrue(len(self.host.resources) > 0)

    def test_host_resource_cpu(self):
        self.assertEqual(self.host.resources[0].cpu, "1")

    def test_host_resource_disk(self):
        self.assertEqual(self.host.resources[0].disk_gb, "1028")

    def test_resource_host_name(self):
        self.assertEqual(self.host.resources[0].host, "nova")

    def test_host_resource_memory(self):
        self.assertEqual(self.host.resources[0].memory_mb, "8192")

    def test_host_resource_project(self):
        self.assertEqual(self.host.resources[0].project, "(total)")


class HostDomainJSONTest(unittest.TestCase, HostDomainTest):

    @classmethod
    def setUp(cls):
        cls.host_json = '{"host":[{"resource":' \
                        '{"cpu": "1",' \
                        '"disk_gb": "1028", ' \
                        ' "host": "nova", ' \
                        '"memory_mb": "8192", ' \
                        '"project": "(total)"}}]}'
        cls.host = Host.deserialize(cls.host_json, "json")


class HostDomainXMLTest(unittest.TestCase, HostDomainTest):

    @classmethod
    def setUp(cls):
        cls.host_xml = '<?xml version="1.0" encoding="UTF-8"?>' \
                       '<host> <resource>' \
                       ' <project>(total)</project>' \
                       ' <memory_mb>8192</memory_mb>' \
                       ' <host>nova</host> <cpu>1</cpu>' \
                       ' <disk_gb>1028</disk_gb>' \
                       ' </resource> </host>'

        cls.host = Host.deserialize(cls.host_xml, "xml")


class HostDomainCollectionTest(object):

    def test_hosts_length(self):
        self.assertEqual(len(self.hosts), 2)

    def test_host_names(self):
        self.assertEqual(self.hosts[0].host_name, "host_name1")
        self.assertEqual(self.hosts[1].host_name, "host_name2")

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
                         '[{"host_name":' \
                         ' "host_name1","service": "compute1",' \
                         '"zone": "nova1"},' \
                         '{"host_name": "host_name2",' \
                         '"service": "compute2","zone": "nova2"}]}'
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
