"""
Copyright 2014 Rackspace
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

from cloudcafe.identity.common.models.base import (
    BaseIdentityModel, EmptyModel)
from cloudcafe.identity.v3.common.domains.models.requests import Domain
from cloudcafe.identity.v3.common.projects.models.requests import Project


class Auth(BaseIdentityModel):
    """
    Request model for v3 Auth block
    """
    ROOT_TAG = 'auth'

    def __init__(self, identity, scope=None):
        super(Auth, self).__init__(locals())

        self.identity = identity or EmptyModel()
        self.scope = scope

    def _obj_to_dict(self):
        """
        @summary: Converting Auth object to a Dictionary representation
        @return: Dictionary representation of an Auth object
        """
        ret = dict()
        ret[Identity.ROOT_TAG] = self.identity._obj_to_dict()

        if self.scope is not None:
            ret['scope'] = self.scope._obj_to_dict()
        return {self.ROOT_TAG: self._remove_empty_values(ret)}


class Identity(BaseIdentityModel):
    """
    Request model for v3 Identity block
    """

    ROOT_TAG = 'identity'

    def __init__(self, token=None, methods=None, username=None, password=None,
                 token_id=None, user_id=None, user_domain_name=None,
                 user_domain_id=None):
        super(Identity, self).__init__(locals())
        self.methods = methods
        self.token = Token(token_id=token_id)._obj_to_dict()
        self.password = Password(
            username=username, user_id=user_id, password=password,
            user_domain_name=user_domain_name,
            user_domain_id=user_domain_id)._obj_to_dict()
        self.none_attr = [token, user_id, user_domain_name, user_domain_id]

    def _obj_to_dict(self):
        """
        @summary: Converting Identity object to a Dictionary representation
        @return: Dictionary representation of an Identity object
        """
        ret = dict()
        if self.methods is not None:
            ret["methods"] = self.methods
        if self.token is not None:
            ret["token"] = self.token
        if all(x is None for x in self.none_attr):
            ret['RAX-AUTH:password'] = self.password
        elif self.password is not None:
            ret['password'] = self.password
        return self._remove_empty_values(ret)


class Token(BaseIdentityModel):
    """
    Request object for Token
    """
    ROOT_TAG = 'token'

    def __init__(self, token_id=None):
        super(Token, self).__init__(locals())
        self.token_id = token_id

    def _obj_to_dict(self):
        """
        @summary: Converting Token object to Dictionary representation
        @return: Dictionary representation of Token object
        """
        ret = dict()
        if self.token_id is not None:
            ret['id'] = self.token_id
        if ret:
            return self._remove_empty_values(ret)
        return None


class Scope(BaseIdentityModel):
    """
    Request model for v3 Scope block
    """
    ROOT_TAG = 'scope'

    def __init__(self, domain_name=None, domain_id=None,
                 project_domain_id=None, project_domain_name=None,
                 project_id=None, project_name=None):
        super(Scope, self).__init__(locals())

        self.domain_name = domain_name
        self.domain_id = domain_id
        self.project_id = project_id
        self.project_name = project_name
        self.domain = Domain(name=domain_name, id_=domain_id)._obj_to_dict()
        self.project = Project(
            name=project_name, id_=project_id,
            project_domain_id=project_domain_id,
            project_domain_name=project_domain_name)._obj_to_dict()

    def _obj_to_dict(self):
        """
        @summary: Converting Scope object to a Dictionary representation
        @return: Dictionary representation of a Scope object
        """
        ret = dict()
        if self.domain_name is not None:
            ret['domain'] = self.domain
        if self.domain_id is not None:
            ret['domain'] = self.domain
        if self.project_name is not None:
            ret['project'] = dict(self.project)
        if self.project_id is not None:
            ret['project'] = dict(self.project)
        return self._remove_empty_values(ret)


class Password(BaseIdentityModel):
    """
    Request object for Password
    """
    ROOT_TAG = 'user'

    def __init__(self, username=None, user_id=None, password=None,
                 user_domain_name=None, user_domain_id=None):
        super(Password, self).__init__(locals())
        self.username = username
        self.user_id = user_id
        self.password = password
        self.domain_name = user_domain_name
        self.domain_id = user_domain_id
        self.domain = Domain(name=user_domain_name,
                             id_=user_domain_id)._obj_to_dict()

    def _obj_to_dict(self):
        """
        @summary: Converting Password object to Dictionary representation
        @return: Dictionary representation of Password object
        """
        ret = dict()
        if self.username is not None:
            ret['name'] = self.username
        if self.user_id is not None:
            ret['id'] = self.user_id
        if self.password is not None:
            ret['password'] = self.password
        if self.domain_name is not None:
            ret['domain'] = dict(self.domain)
        if self.domain_id is not None:
            ret['domain'] = dict(self.domain)

        # If the dictionary is not empty
        if ret:
            dic = {self.ROOT_TAG: ret}
            return self._remove_empty_values(dic)
        return None
