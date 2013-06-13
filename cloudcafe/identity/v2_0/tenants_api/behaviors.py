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

import json
from cloudcafe.identity.v2_0.tenants_api.models.responses.tenant import Tenants
from cloudcafe.identity.v2_0.tenants_api.models.responses.user import Users
from cloudcafe.identity.v2_0.tokens_api.models.requests.role import Roles


class TenantClientBehavior(object):
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
        users_list_dict = json.loads(response.content).get('users')
        users = Users._list_to_obj(users_list_dict)
        user = [user for user in users if user.name == name]
        if len(user) > 0:
            return user[0]

    def get_tenant_by_name(self, name):
        response = self.tenant_client.list_tenants()
        tenants_list_dict = json.loads(response.content).get('tenants')
        tenants = Tenants._list_to_obj(tenants_list_dict)
        tenant = [tenant for tenant in tenants if tenant.name == name]
        if len(tenant) > 0:
            return tenant[0]

    def get_role_by_name(self, name, user_id, tenant_id):
        response = self.tenant_client.get_users_roles_on_tenant(
            tenant_id=tenant_id,
            user_id=user_id)
        roles_list_dict = json.loads(response.content).get('roles')
        roles = Roles._list_to_obj(roles_list_dict)
        role = [role for role in roles if role.name == name]
        if len(role) > 0:
            return role[0]
