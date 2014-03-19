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
from random import randint
from cafe.engine.behaviors import behavior
from cloudcafe.identity.v2_0.extensions.osksadm.client import OSKSADM_Client
from cloudcafe.identity.v2_0.common.behaviors import (
    BaseIdentityExtensionBehavior)


class OSKSADM_Behaviors(BaseIdentityExtensionBehavior):
    @behavior(OSKSADM_Client)
    def create_user(
            self, name=None, password="password", email="test@example.com",
            enabled=True, tenant_id=None):
        name = name or "delme{0}".format(randint(1000000, 9000000))
        r = self.client.create_user(
            name=name, enabled=enabled, email=email, password="password",
            tenant_id=tenant_id)
        if not r.ok:
            raise Exception("Failed to create user, Status:{0}". format(
                r.status_code))
        return r.entity

    @behavior(OSKSADM_Client)
    def delete_user(self, user_id):
        r = self.client.delete_user(user_id)
        if not r.ok:
            raise Exception("Failed to delete user, Status:{0}". format(
                r.status_code))

    def add_global_role_to_user(self, user_id, role_id):
        r = self.client.add_global_role_to_user(user_id, role_id)
        if not r.ok:
            raise Exception("Failed to add role to user, Status:{0}". format(
                r.status_code))

    def delete_global_role_from_user(self, user_id, role_id):
        r = self.client.delete_global_role_from_user(user_id, role_id)
        if not r.ok:
            raise Exception(
                "Failed to delete role from user, Status:{0}". format(
                    r.status_code))

    @behavior(OSKSADM_Client)
    def create_tenant(
            self, name=None, description="test description", enabled=True):
        name = name or "delme{0}".format(randint(1000000, 9000000))
        r = self.client.create_tenant(
            name=name, enabled=enabled, description=description)
        if not r.ok:
            raise Exception("Failed to create tenant, Status:{0}". format(
                r.status_code))
        return r.entity

    @behavior(OSKSADM_Client)
    def delete_tenant(self, tenant_id):
        r = self.client.delete_tenant(tenant_id)
        if not r.ok:
            raise Exception("Failed to delete tenant, Status:{0}". format(
                r.status_code))

    @behavior(OSKSADM_Client)
    def add_role_to_user_for_tenant(self, tenant_id, user_id, role_id):
        r = self.client.add_role_to_user_for_tenant(
            tenant_id, user_id, role_id)
        if not r.ok:
            raise Exception("Failed to add role to user, Status:{0}". format(
                r.status_code))

    @behavior(OSKSADM_Client)
    def delete_role_from_user_for_tenant(self, tenant_id, user_id, role_id):
        r = self.client.delete_role_from_user_for_tenant(user_id, role_id)
        if not r.ok:
            raise Exception(
                "Failed to delete role from user, Status:{0}". format(
                    r.status_code))

    @behavior(OSKSADM_Client)
    def create_role(
            self, role_id=None, name=None, description="test description"):
        name = name or "delme{0}".format(randint(1000000, 9000000))
        r = self.client.create_role(
            role_id=role_id, name=name, description=description)
        if not r.ok:
            raise Exception("Failed to create role, Status:{0}". format(
                r.status_code))
        return r.entity

    @behavior(OSKSADM_Client)
    def delete_role(self, role_id):
        r = self.client.delete_role(role_id)
        if not r.ok:
            raise Exception("Failed to delete role, Status:{0}". format(
                r.status_code))

    def create_service(
        self, service_id="1234", name=None, type_="test",
            description="test"):
        name = name or "delme{0}".format(randint(1000000, 9000000))
        r = self.client.create_service(
            service_id=service_id, name=name, description=description,
            type_=type_)
        if not r.ok:
            raise Exception("Failed to create service, Status:{0}". format(
                r.status_code))
        return r.entity

    def delete_service(self, service_id):
        r = self.client.delete_service(service_id)
        if not r.ok:
            raise Exception("Failed to delete service")
