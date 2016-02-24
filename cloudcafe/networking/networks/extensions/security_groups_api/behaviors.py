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

import time

from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors, NetworkingResponse
from cloudcafe.networking.networks.common.exceptions \
    import ResourceBuildException, ResourceDeleteException, \
    ResourceGetException, ResourceListException, ResourceUpdateException
from cloudcafe.networking.networks.extensions.security_groups_api.constants \
    import SecurityGroupsResponseCodes


class SecurityGroupsBehaviors(NetworkingBaseBehaviors):

    def __init__(self, security_groups_client, security_groups_config):
        super(SecurityGroupsBehaviors, self).__init__()
        self.config = security_groups_config
        self.client = security_groups_client

    def create_security_group(self, name=None, description=None,
                              tenant_id=None, resource_build_attempts=None,
                              raise_exception=True, use_exact_name=False,
                              poll_interval=None):
        """
        @summary: Creates a security group
        @param name: A symbolic name for the security group. Not required to
            be unique.
        @type name: string
        @param description: (optional) Description of a security group.
        @type description: string
        @param tenant_id: (admin use only) Owner of the security group.
        @type tenant_id: string
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts: int
        @param raise_exception: flag to raise an exception if the
            Security Group was not created or to return None
        @type raise_exception: bool
        @param use_exact_name: flag if the exact name in config should be used
        @type use_exact_name: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        if name is None and not use_exact_name:
            name = rand_name(self.config.starts_with_name)
        elif not use_exact_name:
            name = rand_name(name)
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_build_attempts = (resource_build_attempts or
                                   self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Security Group Create failure'
        for attempt in range(resource_build_attempts):
            self._log.debug(
                'Attempt {0} of {1} building security group {2}'.format(
                    attempt + 1, resource_build_attempts, name))

            resp = self.client.create_security_group(
                name=name, description=description, tenant_id=tenant_id)

            resp_check = self.check_response(
                resp=resp,
                status_code=SecurityGroupsResponseCodes.CREATE_SECURITY_GROUP,
                label=name,
                message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the create was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to create {0} security group after {1} attempts: '
                '{2}').format(name, resource_build_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            return result

    def update_security_group(self, security_group_id, name=None,
                              description=None, tenant_id=None,
                              resource_update_attempts=None,
                              raise_exception=False, poll_interval=None):
        """
        @summary: Updates a security group
        @param security_group_id: The UUID for the security group
        @type security_group_id: string
        @param name: A symbolic name for the security group. Not required to
            be unique.
        @type name: string
        @param description: (optional) Description of a security group.
        @type description: string
        @param tenant_id: (admin use only) Owner of the security group.
        @type tenant_id: string
        @param resource_update_attempts: number of API retries
        @type resource_update_attempts: int
        @param raise_exception: flag to raise an exception if the
            Security Group was not updated or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_update_attempts = (resource_update_attempts or
                                    self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Security Group Update failure'
        for attempt in range(resource_update_attempts):
            self._log.debug('Attempt {0} of {1} updating security group '
                            '{2}'.format(attempt + 1, resource_update_attempts,
                                         security_group_id))

            resp = self.client.update_security_group(
                security_group_id=security_group_id, name=name,
                description=description, tenant_id=tenant_id)

            resp_check = self.check_response(
                resp=resp,
                status_code=SecurityGroupsResponseCodes.UPDATE_SECURITY_GROUP,
                label=security_group_id, message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the update was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to update {0} security group after {1} attempts: '
                '{2}').format(security_group_id, resource_update_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceUpdateException(err_msg)
            return result

    def get_security_group(self, security_group_id, resource_get_attempts=None,
                           raise_exception=False, poll_interval=None):
        """
        @summary: Shows information for a specified security group
        @param security_group_id: The UUID for the security group
        @type security_group_id: string
        @param resource_get_attempts: number of API retries
        @type resource_get_attempts: int
        @param raise_exception: flag to raise an exception if the get
            Security Group was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_get_attempts = (resource_get_attempts or
                                 self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Security Group Get failure'
        for attempt in range(resource_get_attempts):
            self._log.debug(
                'Attempt {0} of {1} getting security group {2}'.format(
                    attempt + 1,
                    resource_get_attempts,
                    security_group_id))

            resp = self.client.get_security_group(
                security_group_id=security_group_id)

            resp_check = self.check_response(
                resp=resp,
                status_code=SecurityGroupsResponseCodes.GET_SECURITY_GROUP,
                label=security_group_id,
                message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the get was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to GET {0} security group after {1} attempts: '
                '{2}').format(security_group_id, resource_get_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceGetException(err_msg)
            return result

    def list_security_groups(self, security_group_id=None, name=None,
                             description=None, tenant_id=None,
                             limit=None, marker=None, page_reverse=None,
                             resource_list_attempts=None,
                             raise_exception=False, poll_interval=None):
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
        @param resource_list_attempts: number of API retries
        @type resource_list_attempts: int
        @param raise_exception: flag to raise an exception if the list
            Security Groups was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_list_attempts = (resource_list_attempts or
                                  self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Security Group List failure'
        for attempt in range(resource_list_attempts):
            self._log.debug(
                'Attempt {0} of {1} with security groups list'.format(
                    attempt + 1,
                    resource_list_attempts))

            resp = self.client.list_security_groups(
                security_group_id=security_group_id, name=name,
                description=description, tenant_id=tenant_id, limit=limit,
                marker=marker, page_reverse=page_reverse)

            resp_check = self.check_response(
                resp=resp,
                status_code=SecurityGroupsResponseCodes.LIST_SECURITY_GROUPS,
                label='',
                message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the list was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to LIST security groups after {0} attempts: '
                '{1}').format(resource_list_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceListException(err_msg)
            return result

    def delete_security_group(self, security_group_id,
                              resource_delete_attempts=None,
                              raise_exception=False, poll_interval=None):
        """
        @summary: Deletes a specified security group and its associated
            security group rules
        @param security_group_id: The UUID for the security group
        @type security_group_id: string
        @param resource_delete_attempts: number of API retries
        @type resource_delete_attempts: int
        @param raise_exception: flag to raise an exception if the deleted
            Security Group was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_delete_attempts = (resource_delete_attempts or
                                    self.config.api_retries)

        result = NetworkingResponse()
        for attempt in range(resource_delete_attempts):
            self._log.debug(
                'Attempt {0} of {1} deleting security group {2}'.format(
                    attempt + 1, resource_delete_attempts, security_group_id))

            resp = self.client.delete_security_group(
                security_group_id=security_group_id)
            result.response = resp

            # Delete response is without entity so resp_check can not be used
            if (resp.ok and resp.status_code ==
                    SecurityGroupsResponseCodes.DELETE_SECURITY_GROUP):
                return result

            del_status_code = SecurityGroupsResponseCodes.DELETE_SECURITY_GROUP
            err_msg = (
                '{security_group} Security Group Delete failure, '
                'expected status code: {expected_status}. Response: {status} '
                '{reason} {content}'
                ).format(security_group=security_group_id,
                         expected_status=del_status_code,
                         status=resp.status_code,
                         reason=resp.reason,
                         content=resp.content)
            self._log.error(err_msg)
            result.failures.append(err_msg)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to DELETE {0} Security Group after {1} attempts: '
                '{2}').format(security_group_id, resource_delete_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceDeleteException(err_msg)
            return result

    def delete_security_groups(self, security_group_list=None, name=None,
                               tenant_id=None):
        """
        @summary: deletes multiple security groups
        @param security_group_list: list of security groups UUIDs
        @type security_group_list: list(str)
        @param name: name for the security group to filter by (ignored if
            security_group_list given)
        @type name: string
        @param tenant_id: security group tenant ID to filter by
        @type tenant_id: string (ignored if security_group_list given)
        @return: failed deletes list with security group ID and failures
        @rtype: list(dict)
        """
        if security_group_list is None:
            resp = self.list_security_groups(tenant_id=tenant_id)
            if (resp.response.status_code !=
                    SecurityGroupsResponseCodes.LIST_SECURITY_GROUPS):
                get_msg = ('Unable to get security groups list for '
                           'delete_security_groups call')
                self._log.info(get_msg)
                return None
            security_groups = resp.response.entity

            # In case the filtering on the GET call did NOT worked as expected
            if tenant_id:
                security_groups = self.filter_entity_list_by_attr(
                    entity_list=security_groups, attr='tenant_id',
                    value=tenant_id)

            security_group_list = self.get_id_list_from_entity_list(
                entity_list=security_groups, name=name)
        log_msg = 'Deleting security groups: {0}'.format(security_group_list)
        self._log.info(log_msg)
        failed_deletes = []
        for security_group_id in security_group_list:
            result = self.delete_security_group(
                security_group_id=security_group_id)
            if result.failures:
                failed_deletes.append(result.failures)
        return failed_deletes

    def clean_security_group(self, security_group_id, timeout=None,
                             poll_interval=None):
        """
        @summary: deletes a security group within a time out
        @param security_group_id: The UUID for the security group
        @type security_group_id: string
        @param timeout: seconds to wait for the security group to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: None if delete was successful or the undeleted
            security_group_id
        @rtype: None or string
        """
        timeout = timeout or self.config.resource_delete_timeout
        poll_interval = poll_interval or self.config.api_poll_interval
        endtime = time.time() + int(timeout)
        log_msg = 'Deleting {0} security group within a {1}s timeout '.format(
            security_group_id, timeout)
        self._log.info(log_msg)
        resp = None
        while time.time() < endtime:
            try:
                self.client.delete_security_group(
                    security_group_id=security_group_id)
                resp = self.client.get_security_group(
                    security_group_id=security_group_id)
            except Exception as err:
                err_msg = ('Encountered an exception deleting a security group'
                           ' within the clean_security_group method. '
                           'Exception: {0}').format(err)
                self._log.error(err_msg)

            if (resp is not None and
                    resp.status_code == SecurityGroupsResponseCodes.NOT_FOUND):
                return None
            time.sleep(poll_interval)

        err_msg = ('Unable to delete {0} security group within a {1}s '
                   'timeout').format(security_group_id, timeout)
        self._log.error(err_msg)
        return security_group_id

    def clean_security_groups(self, security_group_list, timeout=None,
                              poll_interval=None):
        """
        @summary: deletes each security group from a list calling
            clean_security_group
        @param security_group_list: list of security groups UUIDs
        @type security_group_list: list(str)
        @param timeout: seconds to wait for the security group to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: list of undeleted security groups UUIDs
        @rtype: list(str)
        """
        log_msg = 'Deleting security groups: {0}'.format(security_group_list)
        self._log.info(log_msg)
        undeleted_security_groups = []
        for security_group in security_group_list:
            result = self.clean_security_group(
                security_group_id=security_group, timeout=timeout,
                poll_interval=poll_interval)
            if result:
                undeleted_security_groups.append(result)
        if undeleted_security_groups:
            err_msg = 'Unable to delete security groups: {0}'.format(
                undeleted_security_groups)
            self._log.error(err_msg)
        return undeleted_security_groups

    def create_security_group_rule(self, security_group_id,
                                   direction='ingress', ethertype='IPv4',
                                   protocol=None, port_range_min=None,
                                   port_range_max=None, remote_group_id=None,
                                   remote_ip_prefix=None,
                                   resource_build_attempts=None,
                                   raise_exception=True, poll_interval=None):
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
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts: int
        @param raise_exception: flag to raise an exception if the
            Security Group Rule was not created or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_build_attempts = (resource_build_attempts or
                                   self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Security Group Rule Create failure'
        for attempt in range(resource_build_attempts):
            self._log.debug((
                'Attempt {0} of {1} building security group rule '
                'at security group {2}')
                .format(attempt + 1,
                        resource_build_attempts,
                        security_group_id))

            resp = self.client.create_security_group_rule(
                security_group_id=security_group_id, direction=direction,
                ethertype=ethertype, protocol=protocol,
                port_range_min=port_range_min, port_range_max=port_range_max,
                remote_group_id=remote_group_id,
                remote_ip_prefix=remote_ip_prefix)

            label = 'At Security Group {0}'.format(security_group_id)
            exp_code = SecurityGroupsResponseCodes.CREATE_SECURITY_GROUP_RULE
            resp_check = self.check_response(
                resp=resp, status_code=exp_code, label=label, message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the create was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to create at security group {0} security group '
                'rule after {1} attempts: {2}'
                ).format(security_group_id,
                         resource_build_attempts,
                         result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            return result

    def get_security_group_rule(self, security_group_rule_id,
                                resource_get_attempts=None,
                                raise_exception=False, poll_interval=None):
        """
        @summary: Shows information for a specified security group rule
        @param security_group_rule_id: The UUID for the security group rule
        @type security_group_rule_id: string
        @param resource_get_attempts: number of API retries
        @type resource_get_attempts: int
        @param raise_exception: flag to raise an exception if the get
            Security Group Rule was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_get_attempts = (resource_get_attempts or
                                 self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Security Group Rule Get failure'
        for attempt in range(resource_get_attempts):
            self._log.debug(
                'Attempt {0} of {1} getting security group rule {2}'.format(
                    attempt + 1, resource_get_attempts,
                    security_group_rule_id))

            resp = self.client.get_security_group_rule(
                security_group_rule_id=security_group_rule_id)

            resp_check = self.check_response(
                resp=resp,
                status_code=SecurityGroupsResponseCodes.GET_SECURITY_GROUP_RULE,
                label=security_group_rule_id, message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the get was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to GET {0} security group rule after {1} attempts: '
                '{2}').format(security_group_rule_id, resource_get_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceGetException(err_msg)
            return result

    def list_security_group_rules(self, security_group_rule_id=None,
                                  security_group_id=None, direction=None,
                                  ethertype=None, protocol=None,
                                  port_range_min=None, port_range_max=None,
                                  remote_group_id=None, remote_ip_prefix=None,
                                  tenant_id=None, limit=None, marker=None,
                                  page_reverse=None,
                                  resource_list_attempts=None,
                                  raise_exception=False, poll_interval=None):
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
        @param resource_list_attempts: number of API retries
        @type resource_list_attempts: int
        @param raise_exception: flag to raise an exception if the list
            Security Groups Rules was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_list_attempts = (resource_list_attempts or
                                  self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Security Group Rules List failure'
        for attempt in range(resource_list_attempts):
            self._log.debug(
                'Attempt {0} of {1} with security group rules list'.format(
                    attempt + 1, resource_list_attempts))

            resp = self.client.list_security_group_rules(
                security_group_rule_id=security_group_rule_id,
                security_group_id=security_group_id, direction=direction,
                ethertype=ethertype, protocol=protocol,
                port_range_min=port_range_min, port_range_max=port_range_max,
                remote_group_id=remote_group_id,
                remote_ip_prefix=remote_ip_prefix, tenant_id=tenant_id,
                limit=limit, marker=marker, page_reverse=page_reverse)

            resp_check = self.check_response(
                resp=resp,
                status_code=SecurityGroupsResponseCodes.LIST_SECURITY_GROUP_RULES,
                label='', message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the list was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to LIST security group rules after {0} attempts: '
                '{1}').format(resource_list_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceListException(err_msg)
            return result

    def delete_security_group_rule(self, security_group_rule_id,
                                   resource_delete_attempts=None,
                                   raise_exception=False, poll_interval=None):
        """
        @summary: Deletes a specified security group rule
        @param security_group_rule_id: The UUID for the security group rule
        @type security_group_rule_id: string
        @param resource_delete_attempts: number of API retries
        @type resource_delete_attempts: int
        @param raise_exception: flag to raise an exception if the delete
            Security Group Rule was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_delete_attempts = (resource_delete_attempts or
                                    self.config.api_retries)

        result = NetworkingResponse()
        for attempt in range(resource_delete_attempts):
            self._log.debug(
                'Attempt {0} of {1} deleting security group rule {2}'.format(
                    attempt + 1, resource_delete_attempts,
                    security_group_rule_id))

            resp = self.client.delete_security_group_rule(
                security_group_rule_id=security_group_rule_id)
            result.response = resp

            # Delete response is without entity so resp_check can not be used
            if (resp.ok and resp.status_code ==
                    SecurityGroupsResponseCodes.DELETE_SECURITY_GROUP_RULE):
                return result

            del_status_code = \
                SecurityGroupsResponseCodes.DELETE_SECURITY_GROUP_RULE
            err_msg = (
                '{security_group_rule} Security Group Rule Delete failure, '
                'expected status code: {expected_status}. Response: {status} '
                '{reason} {content}').format(
                    security_group_rule=security_group_rule_id,
                    expected_status=del_status_code,
                    status=resp.status_code, reason=resp.reason,
                    content=resp.content)
            self._log.error(err_msg)
            result.failures.append(err_msg)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to DELETE {0} Security Group Rule after {1} attempts: '
                '{2}').format(security_group_rule_id, resource_delete_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceDeleteException(err_msg)
            return result

    def delete_security_group_rules(self, security_group_rule_list=None,
                                    security_group_id=None, tenant_id=None):
        """
        @summary: deletes multiple security group rules
        @param security_group_rule_list: list of security group rules UUIDs
        @type security_group_rule_list: list(str)
        @param security_group_id: the security group ID to filter by
        @type security_group_id: string (ignored if security_group_list given)
        @param tenant_id: security group tenant ID to filter by
        @type tenant_id: string (ignored if security_group_list given)
        @return: failed deletes list with security group ID and failures
        @rtype: list(dict)
        """
        if security_group_rule_list is None:
            resp = self.list_security_group_rules(
                security_group_id=security_group_id, tenant_id=tenant_id)
            if (resp.response.status_code !=
                    SecurityGroupsResponseCodes.LIST_SECURITY_GROUP_RULES):
                get_msg = (
                    'Unable to get security groups rules list for '
                    'delete_security_group_rules call')
                self._log.info(get_msg)
                return None
            security_group_rules = resp.response.entity

            # In case the filtering on the GET call did NOT worked as expected
            if security_group_id:
                security_group_rules = self.filter_entity_list_by_attr(
                    entity_list=security_group_rules, attr='security_group_id',
                    value=security_group_id)
            if tenant_id:
                security_group_rules = self.filter_entity_list_by_attr(
                    entity_list=security_group_rules, attr='tenant_id',
                    value=tenant_id)

            security_group_rule_list = self.get_id_list_from_entity_list(
                entity_list=security_group_rules)
        log_msg = 'Deleting security group rules: {0}'.format(
            security_group_rule_list)
        self._log.info(log_msg)
        failed_deletes = []
        for security_group_rule_id in security_group_rule_list:
            result = self.delete_security_group_rule(
                security_group_rule_id=security_group_rule_id)
            if result.failures:
                failed_deletes.append(result.failures)
        return failed_deletes

    def clean_security_group_rule(self, security_group_rule_id, timeout=None,
                                  poll_interval=None):
        """
        @summary: deletes a security group rule within a time out
        @param security_group_rule_id: The UUID for the security group rule
        @type security_group_id: string
        @param timeout: seconds to wait for the security group rule delete
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: None if delete was successful or the undeleted
            security_group_rule_id
        @rtype: None or string
        """
        timeout = timeout or self.config.resource_delete_timeout
        poll_interval = poll_interval or self.config.api_poll_interval
        endtime = time.time() + int(timeout)
        log_msg = ('Deleting {0} security group rule within a {1}s '
                   'timeout ').format(security_group_rule_id, timeout)
        self._log.info(log_msg)
        resp = None
        while time.time() < endtime:
            try:
                self.client.delete_security_group_rule(
                    security_group_rule_id=security_group_rule_id)
                resp = self.client.get_security_group_rule(
                    security_group_rule_id=security_group_rule_id)
            except Exception as err:
                err_msg = ('Encountered an exception deleting a security group'
                           ' rule within the clean_security_group method. '
                           'Exception: {0}').format(err)
                self._log.error(err_msg)

            if (resp is not None and
                    resp.status_code == SecurityGroupsResponseCodes.NOT_FOUND):
                return None
            time.sleep(poll_interval)

        err_msg = ('Unable to delete {0} security group rule within a {1}s '
                   'timeout').format(security_group_rule_id, timeout)
        self._log.error(err_msg)
        return security_group_rule_id

    def clean_security_group_rules(self, security_group_rule_list,
                                   timeout=None, poll_interval=None):
        """
        @summary: deletes each security group rule from a list calling
            clean_security_group_rule
        @param security_group_rule_list: list of security group rules UUIDs
        @type security_group_rule_list: list(str)
        @param timeout: seconds to wait for the security group rule delete
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: list of undeleted security group rule UUIDs
        @rtype: list(str)
        """
        log_msg = 'Deleting security group rules: {0}'.format(
            security_group_rule_list)
        self._log.info(log_msg)
        undeleted_security_group_rules = []
        for security_group_rule in security_group_rule_list:
            result = self.clean_security_group_rule(
                security_group_rule_id=security_group_rule, timeout=timeout,
                poll_interval=poll_interval)
            if result:
                undeleted_security_group_rules.append(result)
        if undeleted_security_group_rules:
            err_msg = 'Unable to delete security group rules: {0}'.format(
                undeleted_security_group_rules)
            self._log.error(err_msg)
        return undeleted_security_group_rules
