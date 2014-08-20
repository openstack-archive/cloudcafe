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

from cafe.engine.behaviors import BaseBehavior

from cloudcafe.common.exceptions import BuildErrorException, TimeoutException
from cloudcafe.networking.lbaas.common.types import LBaaSStatusTypes


class BaseLoadBalancersBehaviors(BaseBehavior):

    def __init__(self, lbaas_client_type, config):
        super(BaseLoadBalancersBehaviors, self).__init__()
        self.config = config

        # This can be a be client of type:  health_monitor, listener,
        # load_balancer, member or pool
        self.lbaas_client_type = lbaas_client_type

    def create_active_lbaas_object(self, lbaas_model_type, **kwargs):
        """
        @summary: Creates a LBaaS object and waits for it to become active
        @param lbaas_model_type: The type of the LBaaS object.
            ex: health_monitor, listener, load_balancer, member, pool
        @type lbaas_model_type: str
        @param kwargs: Key/value pairs to be used in
            create function call
        @type kwargs: dict
        @return: Response object containing response and the LBaaS model
            domain object
        @rtype: requests.Response
        """

        try:
            create_func = getattr(self.lbaas_client_type,
                                  "create_{0}".format(lbaas_model_type))
        except AttributeError as ex:
            error_message = ("Failed to obtain 'create' method for {type_}: "
                             "{message}".format(type_=lbaas_model_type,
                                                message=ex.message))
            self._log.error(error_message)
            raise Exception(error_message)
        else:
            resp = create_func(**kwargs)
        assert resp.status_code == 202
        assert resp.entity is not None

        lbaas_model_obj = resp.entity
        resp = self.wait_for_lbaas_object_status(
            lbaas_object_id=lbaas_model_obj.entity.id,
            lbaas_model_type=lbaas_model_type,
            desired_status=LBaaSStatusTypes.ACTIVE)
        return resp

    def update_lbaas_object_and_wait_for_active(
            self, lbaas_model_type, **kwargs):
        """
        @summary: Updates a LBaaS object and waits for it to become active
        @param lbaas_object_id: The id of the LBaaS type object.
        @type lbaas_object_id: str
        @param lbaas_model_type: The type of the LBaaS object.
            ex: health_monitor, listener, load_balancer, member, pool
        @type lbaas_model_type: str
        @param kwargs: Key/value pairs to be used in
            create function call
        @type kwargs: dict
        @return: Response object containing response and the image
                 domain object
        @rtype: requests.Response
        """

        try:
            update_func = getattr(self.lbaas_client_type,
                                  "update_{0}".format(lbaas_model_type))
        except AttributeError as ex:
            error_message = ("Failed to obtain 'update' method for {type_}: "
                             "{message}".format(type_=lbaas_model_type,
                                                message=ex.message))
            self._log.error(error_message)
            raise Exception(error_message)
        else:
            resp = update_func(**kwargs)
        assert resp.status_code == 202
        assert resp.entity is not None

        lbaas_model_obj = resp.entity
        resp = self.wait_for_lbaas_object_status(
            lbaas_object_id=lbaas_model_obj.entity.id,
            lbaas_model_type=lbaas_model_type,
            desired_status=LBaaSStatusTypes.ACTIVE)
        return resp

    def wait_for_lbaas_object_status(self, lbaas_object_id, lbaas_model_type,
                                     desired_status, interval_time=None,
                                     timeout=None):
        """
        @summary: Waits for a LBaaS type object to reach a desired status.
        @param lbaas_object_id: The id of the LBaaS type object.
        @type lbaas_object_id: str
        @param lbaas_model_type: The type of the LBaaS object.
            ex: health_monitor, listener, load_balancer, member, pool
        @type lbaas_model_type: str
        @param desired_status: Desired final status of the LBaaS type object.
        @type desired_status: str
        @param interval_time: Amount of time in seconds to wait
            between polling.
        @type interval_time: int
        @param interval_time: Amount of time in seconds to wait
            before aborting.
        @type interval_time: int
        @return: Response object containing response and the LBaaS type
            domain object.
        @rtype: requests.Response
        """

        interval_time = interval_time or self.config.lbaas_status_interval
        timeout = timeout or self.config.lbaas_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            try:
                get_func = getattr(self.lbaas_client_type,
                                   "get_{0}".format(lbaas_model_type))
            except AttributeError as ex:
                error_message = ("Failed to obtain 'get' method for {type_}: "
                                 "{message}".format(type_=lbaas_model_type,
                                                    message=ex.message))
                self._log.error(error_message)
                raise Exception(error_message)
            else:
                resp = get_func(lbaas_object_id)

            if not resp.ok:
                raise Exception(
                    "Failed to get {type_} information: "
                    "{code} - {reason}".format(type_=lbaas_model_type,
                                               code=resp.status_code,
                                               reason=resp.reason))
            if resp.entity is None:
                raise Exception(
                    "Response entity was not set. "
                    "Response was: {0}".format(resp.content))

            lbaas_object = resp.entity

            if lbaas_object.status.lower() == LBaaSStatusTypes.ERROR.lower():
                raise BuildErrorException(
                    'Failed during wait of {type_} status with id {id_} '
                    'entered ERROR status.'.format(type_=lbaas_model_type,
                                                   id_=lbaas_object.id))

            if lbaas_object.status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait for {type_} ran for {timeout} seconds and did not "
                "observe {type_} {id_} reach the {status} status.".format(
                    type_=lbaas_model_type, timeout=timeout,
                    id_=lbaas_object_id, status=desired_status))
        return resp
