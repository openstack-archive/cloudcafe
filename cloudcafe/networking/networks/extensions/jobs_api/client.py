"""
Copyright 2016 Rackspace

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
from cloudcafe.networking.networks.extensions.jobs_api.models.response \
    import Job, Jobs


class JobsClient(AutoMarshallingHTTPClient):
    """Networking jobs client for GET calls.

    Attributes:
        url (str): Base URL for the networks service.
        auth_token (str): Auth token to be used for all requests.
        serialize_format (str): Format for serializing requests.
        deserialize_format (str): Format for de-serializing responses.
        tenant_id (Optional[str]): tenant id to be included in the header
            if given.
    """

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None, tenant_id=None):

        super(JobsClient, self).__init__(serialize_format, deserialize_format)

        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application', content_subtype=self.serialize_format)
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        if tenant_id:
            self.default_headers['X-Auth-Project-Id'] = tenant_id
        self.jobs_url = '{url}/jobs'.format(url=url)

    def get_job(self, job_id, requestslib_kwargs=None):
        """Get job by ID

        Args:
            job_id (str): job ID

        Returns:
            Requests.resonse object from the GET job with ID API call.
        """

        url = '{base_url}/{job_id}'.format(base_url=self.jobs_url,
                                           job_id=job_id)
        resp = self.request('GET', url, response_entity_type=Job,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_jobs(self, job_id=None, tenant_id=None, transaction_id=None,
                  parent_id=None, subtransactions=None,
                  completed_subtransactions=None, transaction_percent=None,
                  completed=None, action=None, created_at=None, limit=None,
                  marker=None, page_reverse=None, requestslib_kwargs=None):
        """List jobs

        Args:
            job_id (Optional[str]): get job with this ID.
            tenant_id (Optional[str]): get jobs for this tenant ID.
            transaction_id (Optional[str]): get jobs with this transaction ID.
            parent_id (Optional[str]): get jobs with this parent ID.
            subtransactions (Optional[int]): get jobs with this number of
                subtransactions.
            completed_subtransactions (Optional[int]): get jobs with this
                number of completed subtransactions.
            transaction_percent (Optional[int]): get jobs with this completion
                percentage.
            completed (Optional[bool]): get jobs with this true or false flag.
            action (Optional[str]): get jobs with this action,
                for ex. create sg rule <sg_rule_id> or update port <port_id>.
            created_at (Optional[str]): get jobs with this creation date.
            limit (Optional[int]): page size.
            marker (Optional[str]): ID of the last item of the previous page.
            page_reverse (Optional[bool]): direction of the page.

        Returns:
            List of Requests.resonse objects from the GET jobs API call.
            The list may be filtered if optional args are given.
        """

        params = {'id': job_id, 'tenant_id': tenant_id,
                  'transaction_id': transaction_id, 'parent_id': parent_id,
                  'subtransactions': subtransactions,
                  'completed_subtransactions': completed_subtransactions,
                  'transaction_percent': transaction_percent,
                  'completed': completed, 'action': action,
                  'created_at': created_at, 'limit': limit, 'marker': marker,
                  'page_reverse': page_reverse}

        url = self.jobs_url
        resp = self.request('GET', url, params=params,
                            response_entity_type=Jobs,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
