from cloudcafe.openstackcli.cindercli.client import CinderCLI
from cloudcafe.openstackcli.common.config import OpenstackCLI_CommonConfig
from cloudcafe.openstackcli.cindercli.config import CinderCLI_Config


class CinderCLI_Composite(object):

    def __init__(self):
        self.openstack_config = OpenstackCLI_CommonConfig()
        self.config = CinderCLI_Config()
        self._cli_kwargs = {
            'volume_service_name': self.config.volume_service_name,
            'os_volume_api_version': self.config.os_volume_api_version,
            'os_username': self.openstack_config.os_username,
            'os_password': self.openstack_config.os_password,
            'os_tenant_name': self.openstack_config.os_tenant_name,
            'os_auth_url': self.openstack_config.os_auth_url,
            'os_region_name': self.config.os_region_name or
            self.openstack_config.os_region_name,
            'os_cacert': self.openstack_config.os_cacert,
            'os_auth_system': self.config.os_auth_system,
            'retries': self.openstack_config.retries,
            'debug': self.openstack_config.debug}
        self.client = CinderCLI(**self._cli_kwargs)
        self.client.set_environment_variables(
            self.config.environment_variable_dictionary)
