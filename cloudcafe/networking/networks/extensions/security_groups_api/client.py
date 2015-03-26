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

from cafe.engine.http.client import AutoMarshallingHTTPClient
from cloudcafe.networking.networks.extensions.security_groups_api.models.\
    request import SecurityGroupRequest, SecurityGroupRuleRequest
from cloudcafe.networking.networks.extensions.security_groups_api.models.\
    response import SecurityGroup, SecurityGroups, SecurityGroupRule, \
    SecurityGroupRules


class SecurityGroupsClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None, tenant_id=None):
        """
        @param url: Base URL for the networks service
        @type url: string
        @param auth_token: Auth token to be used for all requests
        @type auth_token: string
        @param serialize_format: Format for serializing requests
        @type serialize_format: string
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: string
        @param tenant_id: optional tenant id to be included in the
            header if given
        @type tenant_id: string
        """
        super(SecurityGroupsClient, self).__init__(serialize_format,
                                                   deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.serialize_format)
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        if tenant_id:
            self.default_headers['X-Auth-Project-Id'] = tenant_id
        self.url = url
        self.security_groups_url = '{url}/security-groups'.format(url=self.url)
        self.security_group_rules_url = '{url}/security-group-rules'.format(
            url=self.url)

    def create_security_group(self, name=None, description=None,
                              tenant_id=None, requestslib_kwargs=None):
        """
        @summary: Creates a security group
        @param name: A symbolic name for the security group. Not required to
            be unique.
        @type name: string
        @param description: (optional) Description of a security group.
        @type description: string
        @param tenant_id: (admin use only) Owner of the security group.
        @type tenant_id: string
        @return: security group create response
        @rtype: Requests.response
        """
        url = self.security_groups_url
        request = SecurityGroupRequest(name=name, description=description,
                                       tenant_id=tenant_id)
        resp = self.request('POST', url,
                            response_entity_type=SecurityGroup,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def update_security_group(self, security_group_id, name=None,
                              description=None, tenant_id=None,
                              requestslib_kwargs=None):
        """
        @summary: Updates a security group
        @param name: A symbolic name for the security group. Not required to
            be unique.
        @type name: string
        @param description: (optional) Description of a security group.
        @type description: string
        @param tenant_id: (admin use only) Owner of the security group.
        @type tenant_id: string
        @return: security group update response
        @rtype: Requests.response
        """
        url = '{base_url}/{security_group_id}'.format(
            base_url=self.security_groups_url,
            security_group_id=security_group_id)
        request = SecurityGroupRequest(name=name, description=description,
                                       tenant_id=tenant_id)
        resp = self.request('PUT', url,
                            response_entity_type=SecurityGroup,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_security_group(self, security_group_id, requestslib_kwargs=None):
        """
        @summary: Shows information for a specified security group
        @param security_group_id: The UUID for the security group
        @type security_group_id: string
        @return: get security group response
        @rtype: Requests.response
        """
        url = '{base_url}/{security_group_id}'.format(
            base_url=self.security_groups_url,
            security_group_id=security_group_id)
        resp = self.request('GET', url,
                            response_entity_type=SecurityGroup,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_security_groups(self, security_group_id=None, name=None,
                             description=None, tenant_id=None,
                             limit=None, marker=None, page_reverse=None,
                             requestslib_kwargs=None):
        """
        @summary: Lists security groups, filtered by params if given
        @param security_group_id: The UUID for the security group to filter by
        @type security_group_id: string
        @param name: name for the security group to filter by
        @type name: string
        @param description: security group description to filter by
        @type description: string
        @param tenant_id: security group tenant ID to filter by
        @type tenant_id: string
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @return: list security groups response
        @rtype: Requests.response
        """
        params = {'id': security_group_id, 'name': name,
                  'description': description, 'tenant_id': tenant_id,
                  'limit': limit, 'marker': marker,
                  'page_reverse': page_reverse}

        url = self.security_groups_url
        resp = self.request('GET', url, params=params,
                            response_entity_type=SecurityGroups,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_security_group(self, security_group_id,
                              requestslib_kwargs=None):
        """
        @summary: Deletes a specified security group and its associated
            security group rules
        @param security_group_id: The UUID for the security group
        @type security_group_id: string
        @return: delete security group response
        @rtype: Requests.response
        """

        url = '{base_url}/{security_group_id}'.format(
            base_url=self.security_groups_url,
            security_group_id=security_group_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_security_group_rule(self, security_group_id, direction,
                                   ethertype, protocol=None,
                                   port_range_min=None, port_range_max=None,
                                   remote_group_id=None, remote_ip_prefix=None,
                                   requestslib_kwargs=None):
        """
        @summary: Creates a security group rule
        @param security_group_id: The security group ID to associate with
        @type security_group_id: string
        @param direction: ingress or egress security group rule direction
        @type direction: string
        @param ethertype: Must be IPv4 or IPv6
        @type ethertype: string
        @param protocol: protocol matched by the security group rule.
            Valid values are null, tcp, udp, and icmp.
        @type protocol: string
        @param port_range_min: The minimum port number in the range
            that is matched by the security group rule. Value must be less
            than or equal to the port_range_max for tcp or udp. If the protocol
            is ICMP, this value must be an ICMP type.
        @type port_range_min: int
        @param port_range_max: The maximum port number in the range
        @type port_range_max: int
        @param remote_group_id: The remote group ID to be associated with
        @type remote_group_id: string
        @param remote_ip_prefix: The remote IP prefix to be associated
            with, remote_group_id or remote_ip_prefix can be specified
        @type remote_ip_prefix: string
        @return: security group rule create response
        @rtype: Requests.response
        """
        url = self.security_group_rules_url
        request = SecurityGroupRuleRequest(
            direction=direction, ethertype=ethertype,
            security_group_id=security_group_id, port_range_min=port_range_min,
            port_range_max=port_range_max, protocol=protocol,
            remote_group_id=remote_group_id, remote_ip_prefix=remote_ip_prefix)
        resp = self.request('POST', url,
                            response_entity_type=SecurityGroupRule,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_security_group_rule(self, security_group_rule_id,
                                requestslib_kwargs=None):
        """
        @summary: Shows information for a specified security group rule
        @param security_group_rule_id: The UUID for the security group rule
        @type security_group_rule_id: string
        @return: get security group rule response
        @rtype: Requests.response
        """
        url = '{base_url}/{security_group_rule_id}'.format(
            base_url=self.security_group_rules_url,
            security_group_rule_id=security_group_rule_id)
        resp = self.request('GET', url,
                            response_entity_type=SecurityGroupRule,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_security_group_rules(self, security_group_rule_id=None,
                                  security_group_id=None, direction=None,
                                  ethertype=None, protocol=None,
                                  port_range_min=None, port_range_max=None,
                                  remote_group_id=None, remote_ip_prefix=None,
                                  tenant_id=None, limit=None, marker=None,
                                  page_reverse=None, requestslib_kwargs=None):
        """
        @summary: Lists security group rules, filtered by params if given
        @param security_group_rule_id: security group rule ID to filter by
        @type security_group_rule_id: string
        @param security_group_id: The security group ID to filter by
        @type security_group_id: string
        @param direction: direction to filter by
        @type direction: string
        @param ethertype: IPv4 or IPv6 ethertype to filter by
        @type ethertype: string
        @param protocol: protocol like tcp, udp, or icmp to filter by
        @type protocol: string
        @param port_range_min: The minimum port number to filter by
        @type port_range_min: int
        @param port_range_max: The maximum port number to filter by
        @type port_range_max: int
        @param remote_group_id: The remote group ID filter by
        @type remote_group_id: string
        @param remote_ip_prefix: The remote IP prefix to filter by
        @type remote_ip_prefix: string
        @param tenant_id: security group rule tenant ID to filter by
        @type tenant_id: string
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @return: list security groups rules response
        @rtype: Requests.response
        """
        params = {'id': security_group_rule_id,
                  'security_group_id': security_group_id,
                  'direction': direction, 'ethertype': ethertype,
                  'protocol': protocol, 'port_range_min': port_range_min,
                  'port_range_max': port_range_max,
                  'remote_group_id': remote_group_id,
                  'remote_ip_prefix': remote_ip_prefix, 'tenant_id': tenant_id,
                  'limit': limit, 'marker': marker,
                  'page_reverse': page_reverse}

        url = self.security_group_rules_url
        resp = self.request('GET', url, params=params,
                            response_entity_type=SecurityGroupRules,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_security_group_rule(self, security_group_rule_id,
                                   requestslib_kwargs=None):
        """
        @summary: Deletes a specified security group rule
        @param security_group_rule_id: The UUID for the security group rule
        @type security_group_rule_id: string
        @return: delete security group rule response
        @rtype: Requests.response
        """

        url = '{base_url}/{security_group_rule_id}'.format(
            base_url=self.security_group_rules_url,
            security_group_rule_id=security_group_rule_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
