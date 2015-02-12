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

import json

from cafe.engine.models.base import AutoMarshallingListModel, \
    AutoMarshallingModel


class SecurityGroup(AutoMarshallingModel):
    """
    @summary: Security Group model response object for the OpenStack
        Networking v2.0 API extension.
    @param id_: UUID for the security group
    @type id_: string
    @param name: name for the security group
    @type name: string
    @param description: Description of the security group
    @type description: string
    @param security_group_rules: rules of the security group
    @type security_group_rules: list
    @param tenant_id: Owner of the security group
    @type tenant_id: string
    """
    SECURITY_GROUP = 'security_group'

    def __init__(self, id_=None, name=None, description=None,
                 security_group_rules=None, tenant_id=None, **kwargs):

        # kwargs is to be used for extensions or checking unexpected attrs
        super(SecurityGroup, self).__init__()
        self.id = id_
        self.name = name
        self.description = description
        self.security_group_rules = security_group_rules
        self.tenant_id = tenant_id
        self.kwargs = kwargs

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Return security group object from a JSON serialized string"""

        ret = None
        json_dict = json.loads(serialized_str)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_ or if they have a
        # special character within the name replacing it for an underscore too
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.SECURITY_GROUP in json_dict:
            security_group_dict = json_dict.get(cls.SECURITY_GROUP)
            ret = SecurityGroup(**security_group_dict)
            if ret.security_group_rules:
                security_group_rules = []
                for rule in ret.security_group_rules:
                    # In case we have a list of uuids (strings)
                    if type(rule) != dict:
                        security_group_rules.append(rule)
                    else:
                        security_group_rules.append(SecurityGroupRule(**rule))
                ret.security_group_rules = security_group_rules
        return ret


class SecurityGroups(AutoMarshallingListModel):

    SECURITY_GROUPS = 'security_groups'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Return a list of security group objects from a JSON
        serialized string
        """
        ret = cls()
        json_dict = json.loads(serialized_str)
        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_ or if they have a
        # special character within the name replacing it for an underscore too
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)
        if cls.SECURITY_GROUPS in json_dict:
            security_groups = json_dict.get(cls.SECURITY_GROUPS)
            for security_group in security_groups:
                result = SecurityGroup(**security_group)
                if result.security_group_rules:
                    security_group_rules = []
                    for rule in result.security_group_rules:
                        # In case we have a list of uuids (strings)
                        if type(rule) != dict:
                            security_group_rules.append(rule)
                        else:
                            security_group_rules.append(
                                SecurityGroupRule(**rule))
                    result.security_group_rules = security_group_rules
                ret.append(result)
        return ret


class SecurityGroupRule(AutoMarshallingModel):
    """
    @summary: Security Group Rules model response object for the OpenStack
        Networking v2.0 API extension.
    @param id_: UUID for the security group rule
    @type id_: string
    @param direction: Ingress or egress: The direction in which the security
        group rule is applied.
    @type direction: string
    @param ethertype: Must be IPv4 or IPv6, and addresses represented in CIDR
        must match the ingress or egress rules.
    @type ethertype: string
    @param security_group_id: The security group ID to associate with this
        security group rule.
    @type security_group_id: string
    @param port_range_min: (optional) The minimum port number in the range
        that is matched by the security group rule. If the protocol is TCP or
        UDP, this value must be less than or equal to the value of the
        port_range_max attribute. If the protocol is ICMP, this value must be
        an ICMP type.
    @type port_range_min: int
    @param port_range_max: (optional) The maximum port number in the range
        that is matched by the security group rule. The port_range_min
        attribute constrains the port_range_max attribute. If the protocol is
        ICMP, this value must be an ICMP type.
    @type port_range_max: int
    @param protocol: (optional) The protocol that is matched by the security
        group rule. Valid values are null, tcp, udp, and icmp.
    @type protocol: string
    @param remote_group_id: (optional) The remote group ID to be associated
        with this security group rule.You can specify either remote_group_id
        or remote_ip_prefix in the request body.
    @type remote_group_id: string
    @param remote_ip_prefix: (optional) The remote IP prefix to be associated
        with this security group rule. You can specify either remote_group_id
        or remote_ip_prefix in the request body. This attribute matches the
        specified IP prefix as the source IP address of the IP packet.
    @type remote_ip_prefix: string
    @param tenant_id: owner of the security group rule
    @type tenant_id: string
    """
    SECURITY_GROUP_RULE = 'security_group_rule'

    def __init__(self, id_=None, direction=None, ethertype=None,
                 security_group_id=None, port_range_min=None,
                 port_range_max=None, protocol=None, remote_group_id=None,
                 remote_ip_prefix=None, tenant_id=None, **kwargs):

        # kwargs is to be used for extensions or checking unexpected attrs
        super(SecurityGroupRule, self).__init__()
        self.id = id_
        self.direction = direction
        self.ethertype = ethertype
        self.security_group_id = security_group_id
        self.port_range_min = port_range_min
        self.port_range_max = port_range_max
        self.protocol = protocol
        self.remote_group_id = remote_group_id
        self.remote_ip_prefix = remote_ip_prefix
        self.tenant_id = tenant_id
        self.kwargs = kwargs

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Return security group rule object from a JSON serialized string"""

        ret = None
        json_dict = json.loads(serialized_str)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_ or if they have a
        # special character within the name replacing it for an underscore too
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.SECURITY_GROUP_RULE in json_dict:
            security_group_rule_dict = json_dict.get(cls.SECURITY_GROUP_RULE)
            ret = SecurityGroupRule(**security_group_rule_dict)
        return ret


class SecurityGroupRules(AutoMarshallingListModel):

    SECURITY_GROUP_RULES = 'security_group_rules'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Return a list of security group rule objects from a JSON
        serialized string
        """

        ret = cls()
        json_dict = json.loads(serialized_str)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_ or if they have a
        # special character within the name replacing it for an underscore too
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.SECURITY_GROUP_RULES in json_dict:
            security_group_rules = json_dict.get(cls.SECURITY_GROUP_RULES)
            for security_group_rule in security_group_rules:
                ret.append(SecurityGroupRule(**security_group_rule))
        return ret
