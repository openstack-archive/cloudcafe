from cloudcafe.openstackcli.novacli.client import NovaCLI
from cloudcafe.openstackcli.common.config import OpenstackCLI_CommonConfig
from cloudcafe.openstackcli.novacli.config import NovaCLI_Config


class NovaCLI_Composite(object):

    def __init__(self):
        self.openstack_config = OpenstackCLI_CommonConfig()
        self.config = NovaCLI_Config()
        self._cli_kwargs = {
            'os_username': self.openstack_config.os_username,
            'os_password': self.openstack_config.os_password,
            'os_tenant_name': self.openstack_config.os_tenant_name,
            'os_auth_url': self.openstack_config.os_auth_url,
            'os_region_name': self.openstack_config.os_region_name,
            'debug': self.openstack_config.debug,
            'os_auth_system': self.config.os_auth_system,
            'insecure': self.config.insecure}
        self.client = NovaCLI(**self._cli_kwargs)
        self.client.set_environment_variables(
            self.config.environment_variable_dictionary)
