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

import os
from cafe.engine.models.data_interfaces import\
    BaseConfigSectionInterface, ConfigEnvironmentVariableError

_TEST_CONFIG_FILE_ENV_VAR = 'OSTNG_CONFIG_FILE'


class ConfigSectionInterface(BaseConfigSectionInterface):
    def __init__(self, config_file_path=None, section_name=None):
        section_name = (section_name or
                        getattr(self, 'SECTION_NAME', None) or
                        getattr(self, 'CONFIG_SECTION_NAME', None))

        config_file_path = config_file_path or self.default_config_file

        super(ConfigSectionInterface, self).__init__(config_file_path,
                                                     section_name)

    @property
    def default_config_file(self):
        test_config_file_path = None
        try:
            test_config_file_path = os.environ[_TEST_CONFIG_FILE_ENV_VAR]
        except KeyError:
            msg = "'{0}' environment variable was not set.".format(
                _TEST_CONFIG_FILE_ENV_VAR)
            raise ConfigEnvironmentVariableError(msg)
        except Exception as exception:
            print ("Unexpected exception when attempting to access '{1}'"
                   " environment variable.".format(_TEST_CONFIG_FILE_ENV_VAR))
            raise exception

        return test_config_file_path
