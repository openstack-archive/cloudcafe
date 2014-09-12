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

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.common.tools.datagen import rand_name


class DomainBehaviors(BaseBehavior):

    def __init__(self, domain_client):
        super(DomainBehaviors, self).__init__()
        self.domain_client = domain_client

    @staticmethod
    def _prepare_domain_and_email(name=None, email=None, tld="com"):
        """If name is none, generate a random domain name under the given tld.
        If email is none, generate an email using the name. Returns a tuple
        (name, email)."""
        if name is None:
            name = "{0}.{1}.".format(rand_name("testdomain"), tld)
        if email is None:
            email = "email@{0}".format(name).strip('.')
        return name, email

    def create_domain(self, name=None, email=None, ttl=5600):
        name, email = self._prepare_domain_and_email(name, email)
        return self.domain_client.create_domain(
            name=name, email=email, ttl=ttl)


class ServerBehaviors(BaseBehavior):

    def __init__(self, server_client):
        super(ServerBehaviors, self).__init__()
        self.server_client = server_client

    def create_server(self, name=None):
        if name is None:
            name = rand_name("namespace.server") + ".com."
        return self.server_client.create_server(name=name)
