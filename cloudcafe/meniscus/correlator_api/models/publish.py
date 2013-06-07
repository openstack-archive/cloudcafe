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
from json import dumps as json_to_str, loads as str_to_json
from cafe.engine.models.base import AutoMarshallingModel


class PublishMessage(AutoMarshallingModel):

    def __init__(self, host=None, pname=None, time=None, native=None):
        super(PublishMessage, self).__init__()
        self.host = host
        self.pname = pname
        self.time = time
        self.native = native

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        body = {
            'host': self.host,
            'pname': self.pname,
            'time': self.time,
            'native': self.native
        }

        return {'log_message': self._remove_empty_values(body)}


class JobInformation(AutoMarshallingModel):

    def __init__(self, job_id, job_status_uri):
        super(JobInformation, self).__init__()
        self.job_id = job_id
        self.job_status_uri = job_status_uri

    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return JobInformation(**json_dict)
