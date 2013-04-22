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

from cloudcafe.common.models.configuration import ConfigSectionInterface


class DBaaSConfig(ConfigSectionInterface):
    SECTION_NAME = 'database'

    @property
    def host(self):
        """Endpoint for database server"""
        return self.get('host')

    @property
    def tenant_id(self):
        """User/Tenant ID"""
        return self.get('tenant_id')

    @property
    def atom_hopper_url(self):
        """N/A"""
        return self.get('atom_hopper_url')

    @property
    def atom_hopper_feed_limit(self):
        """N/A"""
        return self.get('atom_hopper_feed_limit')

    @property
    def atom_hopper_pagination_limit(self):
        """N/A"""
        return self.get('atom_hopper_pagination_limit')

    @property
    def stability_mode(self):
        """N/A"""
        return self.get('stability_mode')

    @property
    def version_url(self):
        """Used to get version information from DBaaS"""
        return self.get('version_url')

    @property
    def rp_admin_user(self):
        """RBAC admin user"""
        return self.get('rp_admin_user')

    @property
    def rp_admin_pw(self):
        """RBAC admin pw"""
        return self.get('rp_admin_pw')

    @property
    def creator_user(self):
        """RBAC creator user"""
        return self.get('creator_user')

    @property
    def creator_pw(self):
        """RBAC creator pw"""
        return self.get('creator_pw')

    @property
    def observer_user(self):
        """RBAC observer user"""
        return self.get('observer_user')

    @property
    def observer_pw(self):
        """RBAC observer pw"""
        return self.get('observer_pw')

    @property
    def perf_server(self):
        """N/A"""
        return self.get('perf_serv')

    @property
    def perf_server_user(self):
        """N/A"""
        return self.get('perf_serv_user')

    @property
    def perf_server_password(self):
        """N/A"""
        return self.get('perf_serv_pass')

    @property
    def graphite_endpoint(self):
        """N/A"""
        return self.get('graphiteEndpoint')

    @property
    def mgmt_host(self):
        """N/A"""
        return self.get('mgmt_host')

    @property
    def mgmt_base_url(self):
        """N/A"""
        return self.get('mgmt_base_url')

    @property
    def mgmt_username(self):
        """N/A"""
        return self.get('mgmt_username')

    @property
    def mgmt_api_key(self):
        """N/A"""
        return self.get('mgmt_api_key')

    @property
    def mgmt_tenant_id(self):
        """N/A"""
        return self.get('mgmt_tenant_id')
