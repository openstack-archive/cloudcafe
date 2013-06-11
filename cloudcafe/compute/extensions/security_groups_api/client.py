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

from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.compute.extensions.security_groups_api.models.requests \
    import CreateSecurityGroup, CreateSecurityGroupRule
from cloudcafe.compute.extensions.security_groups_api.models.security_group \
    import SecurityGroup, SecurityGroups
from cloudcafe.compute.extensions.security_groups_api.models.\
    security_group_rule import SecurityGroupRule


class SecurityGroupsClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(SecurityGroupsClient, self).__init__(serialize_format,
                                                   deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_security_group(self, name, description=None,
                              requestslib_kwargs=None):
        request = CreateSecurityGroup(name=name, description=description)

        url = '{base_url}/os-security-groups'.format(base_url=self.url)
        resp = self.request('POST', url,
                            response_entity_type=SecurityGroup,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_security_group(self, group_id, requestslib_kwargs=None):

        url = '{base_url}/os-security-groups/{group_id}'.format(
            base_url=self.url, group_id=group_id)
        resp = self.request('GET', url,
                            response_entity_type=SecurityGroup,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_security_groups(self, requestslib_kwargs=None):

        url = '{base_url}/os-security-groups'.format(base_url=self.url)
        resp = self.request('GET', url,
                            response_entity_type=SecurityGroups,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_security_group(self, group_id, requestslib_kwargs=None):
        url = '{base_url}/os-security-groups/{group_id}'.format(
            base_url=self.url, group_id=group_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp


class SecurityGroupRulesClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(SecurityGroupRulesClient, self).__init__(serialize_format,
                                                       deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_rule(self, from_port, ip_protocol, to_port,
                    parent_group_id, cidr, group_id,
                    requestslib_kwargs=None):
        url = '{base_url}/os-security-group-rules'.format(base_url=self.url)
        create_sec_group_request = \
            CreateSecurityGroupRule(from_port, ip_protocol, to_port,
                                    parent_group_id, cidr, group_id)
        resp = self.request('POST', url,
                            response_entity_type=SecurityGroupRule,
                            request_entity=create_sec_group_request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
