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

import copy
import json

from cafe.engine.models.base import AutoMarshallingListModel, \
    AutoMarshallingModel


class Job(AutoMarshallingModel):
    """Networking Job model object to track the auto port update transactions
        done by adding and deleting security group rules

    Attributes:
        id (str): job ID.
        tenant_id (str): user tenant ID.
        transaction_id (str): multiple jobs can belong to one transaction.
            subtransactions and parents will have the same transaction_id.
        parent_id (str): parent ID (may not always be used and set to None).
        subtransactions (int): number of child jobs.
        completed_subtransactions (int): number of subtransactions completed.
        transaction_percent (int): job completion percentage (100 for done).
        completed (bool): set to true when the job is done.
        action (str): job description, for ex. create sg rule <sg_rule_id>
            or update port <port_id>.
        created_at (str): creation date, for ex. 2016-10-07 16:16:00.
    """
    JOB = 'job'

    def __init__(self, id_=None, tenant_id=None, transaction_id=None,
                 parent_id=None, subtransactions=None,
                 completed_subtransactions=None, transaction_percent=None,
                 completed=None, action=None, created_at=None, **kwargs):

        # kwargs is to be used for extensions or checking unexpected attrs
        super(Job, self).__init__()
        self.id = id_
        self.tenant_id = tenant_id
        self.transaction_id = transaction_id
        self.parent_id = parent_id
        self.subtransactions = subtransactions
        self.completed_subtransactions = completed_subtransactions
        self.transaction_percent = transaction_percent
        self.completed = completed
        self.action = action
        self.created_at = created_at
        self.kwargs = kwargs

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Return job object from a JSON serialized string"""

        ret = None
        json_response = json.loads(serialized_str)

        # Creating a deep copy just in case later we want the original resp
        json_dict = copy.deepcopy(json_response)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.JOB in json_dict:
            job_dict = json_dict.get(cls.JOB)
            ret = Job(**job_dict)
        return ret


class Jobs(AutoMarshallingListModel):

    JOBS = 'jobs'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Return a list of job objects from a JSON serialized string"""

        ret = cls()
        json_response = json.loads(serialized_str)

        # Creating a deep copy just in case later we want the original resp
        json_dict = copy.deepcopy(json_response)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.JOBS in json_dict:
            jobs = json_dict.get(cls.JOBS)
            for job in jobs:
                ret.append(Job(**job))
        return ret
