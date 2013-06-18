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
from cloudcafe.identity.v2_0.base import BaseIdentityListModel


class Users(BaseIdentityListModel):
    def __init__(self, users=None):
        """
        Models a users list returned by keystone
        """
        super(Users, self).__init__()
        self.extend(users or [])

    @classmethod
    def _list_to_obj(cls, user_dict_list):
        users = Users()
        for user_dict in user_dict_list:
            user = User._dict_to_obj(user_dict)
            users.append(user)

        return users


class User(BaseIdentityListModel):
    def __init__(self, id_=None, name=None, tenant_id=None,
                 enabled=None, email=None):
        """
        Models a user object returned by keystone
        """
        super(User, self).__init__()
        self.id_ = id_
        self.name = name
        self.tenant_id = tenant_id
        self.enabled = enabled
        self.email = email

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return User(**json_dict)
