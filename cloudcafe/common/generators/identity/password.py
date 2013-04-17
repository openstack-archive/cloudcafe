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

from datetime import datetime

from cafe.common.generators.base import BaseDataGenerator

class PasswordGenerator(BaseDataGenerator):
    def __init__(self):
        self.test_records = []
        stamp = datetime.now().microsecond
        cluster_name = "auth_functional_%s" %stamp
        self.test_records.append({"false_password":'00000000',
                                  "false_username":'@1234567'})
        self.test_records.append({"false_password":'',
                                  "false_username":''})
        self.test_records.append({"false_password":'Pass1',
                                  "false_username":'@'})
        self.test_records.append({"false_password":'!@#$%^&*()',
                                  "false_username":' 1Afarsf'})
        self.test_records.append({"false_password":'102102101031013010311031',
                                  "false_username":'Ricardo0000000000000!'})
