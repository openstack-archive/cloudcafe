"""
Copyright 2015 Rackspace

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
from cloudcafe.networking.networks.common.constants \
    import NeutronErrorTypes, NeutronResponseCodes


class SecurityGroupsResponseCodes(NeutronResponseCodes):
    """HTTP Security Groups API Response codes"""

    LIST_SECURITY_GROUPS = 200
    GET_SECURITY_GROUP = 200
    CREATE_SECURITY_GROUP = 201
    UPDATE_SECURITY_GROUP = 200
    DELETE_SECURITY_GROUP = 204
    LIST_SECURITY_GROUP_RULES = 200
    GET_SECURITY_GROUP_RULE = 200
    CREATE_SECURITY_GROUP_RULE = 201
    DELETE_SECURITY_GROUP_RULE = 204


class SecurityGroupsErrorTypes(NeutronErrorTypes):
    """Security Groups Error Types"""
    EGRESS_SECURITY_GROUP_RULES_NOT_ENABLED = (
        'EgressSecurityGroupRulesNotEnabled')
    INVALID_INPUT = 'InvalidInput'
    SECURITY_GROUP_INVALID_ICMP_VALUE = 'SecurityGroupInvalidIcmpValue'
    SECURITY_GROUP_INVALID_PORT_VALUE = 'SecurityGroupInvalidPortValue'
    SECURITY_GROUP_MISSING_ICMP_TYPE = 'SecurityGroupMissingIcmpType'
    SECURITY_GROUP_NOT_FOUND = 'SecurityGroupNotFound'
    SECURITY_GROUP_PROTOCOL_REQUIRED_WITH_PORTS = (
        'SecurityGroupProtocolRequiredWithPorts')
    SECURITY_GROUP_RULE_INVALID_ETHERTYPE = (
        'SecurityGroupRuleInvalidEtherType')
    SECURITY_GROUP_RULE_INVALID_PROTOCOL = 'SecurityGroupRuleInvalidProtocol'
    SECURITY_GROUP_RULE_NOT_FOUND = 'SecurityGroupRuleNotFound'
