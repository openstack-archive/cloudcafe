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

import unittest
import mock

from cloudcafe.identity.v3.common.projects.models.responses import Project


class Mock(object):
    @classmethod
    def _dict_to_obj(cls, data):
        return "mocked stuff"

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return "mocked stuff"


class ProjectResponseTests(unittest.TestCase):
    """
    Metatests for v3 Project response model
    """
    RESPONSES = 'cloudcafe.identity.v3.common.projects.models.responses'

    @mock.patch(RESPONSES+'.Domain', Mock)
    def test_dict_to_obj(self):
        """
        test to verify Project.dict_to_obj() can convert a dictionary
        representation of a Project to a Project object
        """
        # ARRANGE
        project_dict = {
            'id': 'test_project_id',
            'name': 'test_project_name',
            'domain': 'test_domain'
        }
        expected_project_obj = Project(id_='test_project_id',
                                       name='test_project_name',
                                       domain='mocked stuff')
        # ACT
        project_resp_obj = Project._dict_to_obj(project_dict)
        # ARRANGE
        self.assertEqual(expected_project_obj, project_resp_obj)


if __name__ == '__main__':
    unittest.main()
