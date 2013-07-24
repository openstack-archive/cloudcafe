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


class TenantsBehaviors(object):
    def __init__(self, client):
        self.tenant_client = client

    def disable_user(self, user_name):
        user = self.get_user_by_name(user_name)
        self.tenant_client.update_user(user_id=user.id_, enabled=False)

    def disable_tenant(self, tenant_name):
        tenant = self.get_tenant_by_name(tenant_name)
        self.tenant_client.update_tenant(tenant_id=tenant.id_, enabled=False)

    def get_user_by_name(self, name):
        response = self.tenant_client.list_users()
        users = response.entity
        user = [user for user in users if user.name == name]
        if len(user) == 1:
            return user[0]
        if len(user) > 1:
            raise Exception("There is more than one user with the given name")

    def get_tenant_by_name(self, name):
        response = self.tenant_client.list_tenants()
        tenants = response.entity
        tenant = [tenant for tenant in tenants if tenant.name == name]
        if len(tenant) == 1:
            return tenant[0]
        if len(tenant) > 1:
            raise Exception("There is more than one tenant with the given "
                            "name")

    def get_role_by_name(self, name, user_id, tenant_id):
        response = self.tenant_client.get_users_roles_on_tenant(
            tenant_id=tenant_id,
            user_id=user_id)
        roles = response.entity
        role = [role for role in roles if role.name == name]
        if len(role) == 1:
            return role[0]
        if len(role) > 1:
            raise Exception("There is more than one role with the given name")

    def get_all_tenant_ids(self):
        """ Get a list of all tenants
        @return list of Tenant IDs
        """
        response = self.tenant_client.list_tenants()
        tenants = response.entity

        return [x.id_ for x in tenants]
