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

from cafe.engine.models.base import AutoMarshallingModel


class SecurityGroupRequest(AutoMarshallingModel):
    """
    @summary: Security Group model request object for the OpenStack Networking
        v2.0 API extension.
    @param name: A symbolic name for the security group. Not required to be
        unique.
    @type name: string
    @param description: (optional) Description of a security group.
    @type description: string
    @param tenant_id: (admin use only) Owner of the security group.
    @type tenant_id: string
    """

    def __init__(self, name=None, description=None, tenant_id=None, **kwargs):
        super(SecurityGroupRequest, self).__init__()
        self.name = name
        self.description = description
        self.tenant_id = tenant_id

    def _obj_to_json(self):

        body = {
            'name': self.name,
            'description': self.description,
            'tenant_id': self.tenant_id
        }

        # Removing optional params not given
        body = self._remove_empty_values(body)
        main_body = {'security_group': body}
        return json.dumps(main_body)


class SecurityGroupRuleRequest(AutoMarshallingModel):
    """
    @summary: Security Group Rules model request object for the OpenStack
        Networking v2.0 API extension.
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
    """

    def __init__(self, direction=None, ethertype=None, security_group_id=None,
                 port_range_min=None, port_range_max=None, protocol=None,
                 remote_group_id=None, remote_ip_prefix=None, **kwargs):
        super(SecurityGroupRuleRequest, self).__init__()
        self.direction = direction
        self.ethertype = ethertype
        self.security_group_id = security_group_id
        self.port_range_min = port_range_min
        self.port_range_max = port_range_max
        self.protocol = protocol
        self.remote_group_id = remote_group_id
        self.remote_ip_prefix = remote_ip_prefix

    def _obj_to_json(self):

        body = {
            'direction': self.direction,
            'ethertype': self.ethertype,
            'security_group_id': self.security_group_id,
            'port_range_min': self.port_range_min,
            'port_range_max': self.port_range_max,
            'protocol': self.protocol,
            'remote_group_id': self.remote_group_id,
            'remote_ip_prefix': self.remote_ip_prefix
        }

        # Removing optional params not given
        body = self._remove_empty_values(body)
        main_body = {'security_group_rule': body}
        return json.dumps(main_body)
