import unittest
from cloudcafe.openstackcli.novacli.client import NovaCLI


class NovaCLI_InitializationClientWithAllArguments(unittest.TestCase):

    """
            'os_cache': 'os-cache',
            'timings': 'timings',
            'timeout': 'timeout',
            'os_auth_system': 'os-auth-system',
            'service_type': 'service-type',
            'service_name': 'service-name',
            'volume_service_name': 'volume-service-name',
            'os_compute_api_version': 'os-compute-api-version',
            'bypass_url': 'bypass-url',
            'insecure': 'insecure'}
    """
    @classmethod
    def setUpClass(cls):
        cls.novacli = NovaCLI(
            os_cache=True, timings=True, timeout=30,
            os_username='fake_username', os_password='fake_password',
            os_tenant_name='FakeTenantName', os_tenant_id='1234567',
            os_auth_url='os-auth-url', os_region_name='region_name',
            os_auth_system='auth_system', service_type='service-type',
            volume_service_name='vol serv name', endpoint_type='endpoint_type',
            os_compute_api_version='v111', os_cacert='cert_here',
            insecure=True, bypass_url='bypass_url')
        cls.base_cmd = cls.novacli.base_cmd()

    def test_os_cache(self):
        self.assertIn('--os-cache', self.base_cmd)

    def test_timings(self):
        self.assertIn('--timings', self.base_cmd)

    def test_timeout(self):
        self.assertIn('--timeout 30', self.base_cmd)

    def test_os_username(self):
        self.assertIn('--os-username fake_username', self.base_cmd)

    def test_os_password(self):
        self.assertIn('--os-password fake_password', self.base_cmd)

    def test_os_tenant_name(self):
        self.assertIn('--os-tenant-name FakeTenantName', self.base_cmd)

    def test_os_tenant_id(self):
        self.assertIn('--os-tenant-id 1234567', self.base_cmd)

    def test_os_auth_url(self):
        self.assertIn('--os-auth-url os-auth-url', self.base_cmd)

    def test_os_region_name(self):
        self.assertIn('--os-region-name region_name', self.base_cmd)

    def test_os_auth_system(self):
        self.assertIn('--os-auth-system auth_system', self.base_cmd)

    def test_service_type(self):
        self.assertIn('--service-type service-type', self.base_cmd)

    def test_volume_service_name(self):
        self.assertIn('--volume-service-name vol serv name', self.base_cmd)

    def test_endpoint_type(self):
        self.assertIn('--endpoint-type endpoint_type', self.base_cmd)

    def test_os_compute_api_version(self):
        self.assertIn('--os-compute-api-version v111', self.base_cmd)

    def test_os_cacert(self):
        self.assertIn('--os-cacert cert_here', self.base_cmd)

    def test_insecure(self):
        self.assertIn('--insecure', self.base_cmd)

    def test_bypass_url(self):
        self.assertIn('--bypass-url bypass_url', self.base_cmd)

    def test_no_arguments_positive(self):
        novacli = NovaCLI()
        self.assertEquals(novacli.base_cmd().strip(), 'nova')


class NovaCLI_CreateServer_ArgumentSerializationTests(unittest.TestCase):

    def setUp(self):
        self.novacli = NovaCLI(insecure=False)

    def test_no_arguments_positive(self):
        r = self.novacli.create_server("")
        self.assertEqual(r.command.strip(), "nova boot")
