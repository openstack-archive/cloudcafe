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

from cloudcafe.identity.v3.common.projects.models.requests import Project


class ProjectRequestsTests(unittest.TestCase):
    """
    Metatests for v3 Project request model
    """
    def test_obj_to_dict(self):
        """
        test to verify Project.obj_to_dict() can convert a Project object to
        a dictionary
        """
        # ARRANGE
        test_project_obj = Project(
            id_='test_id',
            name='test_name',
            project_domain_id='test_project_domain_id',
            project_domain_name='test_project_domain_name'
        )
        expected_project_dict = {
            'id': 'test_id',
            'name': 'test_name',
            'domain': {
                'id': 'test_project_domain_id',
                'name': 'test_project_domain_name'
            }
        }
        # ACT
        test_project_dict = test_project_obj._obj_to_dict()
        # ASSERT
        self.assertEqual(expected_project_dict, test_project_dict)


if __name__ == '__main__':
    unittest.main()
