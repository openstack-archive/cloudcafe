import unittest
from cloudcafe.openstackcli.novacli.client import NovaCLI


class NovaCLI_InitializeClientWithAllArguments(unittest.TestCase):
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


class NovaCLI_CommandSerializationTests_CreateServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        class FakeResponse(object):
            def __init__(self, cmd):
                self.command = cmd
                self.standard_out = "fake standard out"

        cls.novacli = NovaCLI()
        cls.novacli.run_command = lambda x: FakeResponse(x)
        cls.command = cls.novacli.create_server(
            name='fake name',
            no_service_net=True,
            no_public=True,
            disk_config='auto',
            flavor='fake flavor',
            image='fake image',
            boot_volume='fake boot volume',
            snapshot='fake snapshot',
            num_instances='55',
            key_name='SomeKeyName',
            user_data='SomeUserData',
            availability_zone='SomeAvailabilityZone',
            security_groups='SomeSecurityGroups',
            swap=100,  # Just so that there's an int in this test.
            config_drive='/dev/sda',
            image_with={'fake_image_with_key': 'fake_image_with_value'},
            meta={
                'fake_meta_key1': 'fake_meta_value1',
                'fake_meta_key2': 'fake_meta_value2'},
            file_={'dst-path': 'src-path'},
            block_device_mapping={'dev-name': 'mapping'},
            block_device={'bdkey': 'bdvalue'},
            ephemeral={'size': 'SomeSize', 'format': 'SomeFormat'},
            hint={'HintKey': 'HintValue'},
            nic={
                'net-id': 'Some-net-uuid',
                'port-id': 'Some-port-uuid',
                'v4-fixed-ip': 'Some-ip-addr'}).command

    def test_no_arguments(self):
        r = self.novacli.create_server("")
        self.assertEqual(r.command.strip(), "nova boot")

    def test_name(self):
        self.assertIn("fake name", self.command)

    def test_no_service_net(self):
        self.assertIn("--no-service-net", self.command)

    def test_no_public(self):
        self.assertIn("--no-public", self.command)

    def test_disk_config(self):
        self.assertIn("--disk-config auto", self.command)

    def test_flavor(self):
        self.assertIn("--flavor fake flavor", self.command)

    def test_image(self):
        self.assertIn("--image fake image", self.command)

    def test_boot_volume(self):
        self.assertIn("--boot-volume fake boot volume", self.command)

    def test_snapshot(self):
        self.assertIn("--snapshot fake snapshot", self.command)

    def test_num_instances(self):
        self.assertIn("--num-instances 55", self.command)

    def test_key_name(self):
        self.assertIn("--key-name SomeKeyName", self.command)

    def test_user_data(self):
        self.assertIn("--user-data SomeUserData", self.command)

    def test_availability_zone(self):
        self.assertIn("--availability-zone SomeAvailabilityZone", self.command)

    def test_security_groups(self):
        self.assertIn("--security-groups SomeSecurityGroups", self.command)

    def test_swap(self):
        self.assertIn("--swap 100", self.command)

    def test_config_drive(self):
        self.assertIn("--config-drive /dev/sda", self.command)

    def test_image_with(self):
        self.assertIn(
            "--image-with 'fake_image_with_key'='fake_image_with_value'",
            self.command)

    def test_meta(self):
        self.assertIn(
            "--meta 'fake_meta_key1'='fake_meta_value1'", self.command)
        self.assertIn(
            "--meta 'fake_meta_key2'='fake_meta_value2'", self.command)

    def test_file(self):
        self.assertIn("--file 'dst-path'='src-path'", self.command)

    def test_block_device_mapping(self):
        self.assertIn(
            "--block-device-mapping 'dev-name'='mapping'",
            self.command)

    def test_block_device(self):
        self.assertIn("--block-device 'bdkey'='bdvalue'", self.command)

    def test_ephemeral(self):
        self.assertIn(
            "--ephemeral 'format'='SomeFormat' 'size'='SomeSize' ",
            self.command)

    def test_hint(self):
        self.assertIn("--hint 'HintKey'='HintValue'", self.command)

    def test_nic(self):
        self.assertIn(
            "--nic 'port-id'='Some-port-uuid' 'net-id'='Some-net-uuid' "
            "'v4-fixed-ip'='Some-ip-addr'", self.command)
