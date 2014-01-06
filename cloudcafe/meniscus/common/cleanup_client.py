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
from cafe.engine.mongo.client import BaseMongoClient


class MeniscusDbClient(BaseMongoClient):
    """
    This is client is only designed to clean up workers and tenants that are
    created as a result of testing due to the lack of API's to remove them.
    """
    def __init__(self, host, db_name, username, password):
        super(MeniscusDbClient, self).__init__(hostname=host,
                                               db_name=db_name,
                                               username=username,
                                               password=password)

    def remove_tenant(self, tenant_id):
        self.delete('tenant', {'tenant_id': tenant_id})

    def remove_worker(self, worker_id):
        self.delete('worker', {'worker_id': worker_id})

    def get_worker(self, worker_id):
        return self.find_one('worker', {'worker_id': worker_id})

    def get_worker_token(self, worker_id):
        worker = self.get_worker(worker_id)
        return worker.get('worker_token')
