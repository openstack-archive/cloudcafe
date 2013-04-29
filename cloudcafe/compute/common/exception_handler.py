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

import xml.etree.ElementTree as ET
import json

from cafe.engine.models.base import AutoMarshallingModel
import cloudcafe.compute.common.exceptions as exceptions


ns = "http://docs.openstack.org/compute/api/v1.1"


class ExceptionHandler:

    error_codes_list = [400, 401, 403, 404, 405, 409, 413, 415, 500, 501, 503]

    def check_for_errors(self, resp):

        if resp.status_code not in self.error_codes_list:
            return

        resp_body_dict = None
        if resp.text != "":
            resp_body_dict, type = self._parse_resp_body(resp.text)

        if resp.status_code == 400 and type == 'html':
            raise exceptions.BadRequest(
                resp_body_dict['400 Bad Request']['message'])

        if resp.status_code == 400:
            raise exceptions.BadRequest(
                resp_body_dict['badRequest']['message'])

        if resp.status_code == 401:
            raise exceptions.Unauthorized()

        if resp.status_code == 413:
            if 'overLimit' in resp_body_dict:
                message = resp_body_dict['overLimit']['message']
            else:
                message = 'Rate or absolute limit exceeded'
            raise exceptions.OverLimit(message)

        if resp.status_code == 500 and type == 'html':
            raise exceptions.InternalServerError()

        if resp.status_code == 500 and resp_body_dict is None:
            raise exceptions.ComputeFault(resp.reason)

        if resp.status_code in (500, 501):
            message = ''
            if 'computeFault' in resp_body_dict:
                message = resp_body_dict['computeFault']['message']
            if 'cloudServersFault' in resp_body_dict:
                message = resp_body_dict['cloudServersFault']['message']
            if 'x-compute-request-id' in resp_body_dict:
                message += ' x-compute-request-id ' + resp_body_dict['x-compute-request-id']
            raise exceptions.ComputeFault(message)

        if resp.status_code == 404:
            raise exceptions.ItemNotFound()

        if resp.status_code == 409:
            message = ''
            if 'conflictingRequest' in resp_body_dict:
                message = resp_body_dict['conflictingRequest']['message']
            if 'inProgress' in resp_body_dict:
                message = resp_body_dict['inProgress']['message']
            raise exceptions.ActionInProgress(message)

        if resp.status_code == 405:
            raise exceptions.BadMethod()

        if resp.status_code == 403:
            raise exceptions.Forbidden()

        if resp.status_code == 503:
            raise exceptions.ServiceUnavailable()

        if resp.status_code == 415:
            raise exceptions.BadMediaType()

    def _parse_resp_body(self, resp_body):

        # Try parsing as JSON
        try:
            body = json.loads(resp_body)
            type = 'json'
            return body, type
        except:
            pass

        # Try parsing as XML
        try:
            element = ET.fromstring(resp_body)
            # Handle the case where the API returns the exception in HTML
            AutoMarshallingModel._remove_namespace(element, ns)
            type = 'xml'
            return {element.tag: {'message': element.find('message').text}}, type
        except:
            pass

        # Parse as HTML
        finally:
            split_resp = resp_body.split("\n\n")
            type = 'html'
            return {split_resp[0]: {'message': split_resp[1]}}, type
