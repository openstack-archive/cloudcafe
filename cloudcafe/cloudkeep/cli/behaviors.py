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


class BarbicanCLIBehaviors(object):

    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.created_entities = []

    def _delete_all_created_entities(self):
        for hateos_ref in self.created_entities:
            self.client.delete(hateos_ref)

    def _process_response(self, resp, clean=True):
        hateos_ref = None
        if resp.return_code == 0:
            hateos_ref = resp.standard_out
            if clean:
                self.created_entities.append(hateos_ref)

        return hateos_ref, resp


class SecretsCLIBehaviors(BarbicanCLIBehaviors):

    def store_secret(self, name=None, payload=None, payload_content_type=None,
                     payload_content_encoding=None, algorithm=None,
                     bit_length=None, mode=None, expiration=None, clean=True):
        resp = self.client.store(
            name=name, payload=payload,
            payload_content_type=payload_content_type,
            payload_content_encoding=payload_content_encoding,
            algorithm=algorithm, bit_length=bit_length, mode=mode,
            expiration=expiration)

        return self._process_response(resp, clean)


class OrdersCLIBehaviors(BarbicanCLIBehaviors):

    def create(self, name=None, algorithm=None, bit_length=None,
               mode=None, payload_content_type=None, expiration=None,
               clean=True):
        resp = self.client.create(
            name=name, algorithm=algorithm, bit_length=bit_length, mode=mode,
            payload_content_type=payload_content_type, expiration=expiration)

        return self._process_response(resp, clean)
