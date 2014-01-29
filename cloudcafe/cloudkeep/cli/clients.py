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
from cafe.engine.clients.commandline import BaseCommandLineClient


class BarbicanCLIClient(BaseCommandLineClient):

    def __init__(self, url, api_version, auth_endpoint=None,
                 user=None, password=None, tenant_id=None):
        super(BarbicanCLIClient, self).__init__(base_command='barbican')
        self.url = url
        self.username = user
        self.password = password
        self.tenant_id = tenant_id
        self.api_version = api_version
        self.auth_endpoint = auth_endpoint
        self.barbican_endpoint = '{base}/{api_version}/'.format(
            base=self.url, api_version=self.api_version)

    def _construct_option_str_from_dict(self, param_dict):
        options = []
        cleaned = {k: v for k, v in param_dict.iteritems() if v is not None}

        for argument, value in cleaned:
            options.append(str(argument))

            # Assuming we can use the value if it's not empty
            if value != '':
                options.append(str(value))

        return ' '.join(options)

    def _generate_cli_base_options(self):
        """ Constructs a string of CLI options based on set parameters"""
        options = {
            '--os-username': self.username,
            '--os-password': self.password,
            '--os-auth-url': self.auth_endpoint,
            '--os-tenant-id': self.tenant_id
        }

        if not self.username and not self.password:
            self._log.info('No username and password was provided. '
                           'Assuming no-auth mode')
            options['--no-auth'] = ''

        return self._construct_option_str_from_dict(options)

    def _action_command(self, entity_type, action, *params):
        options_str = self._generate_cli_base_options()

        cmd = '{options} {entity} {action}'.format(options=options_str,
                                                   entity=entity_type,
                                                   action=action)
        for param in params:
            cmd += '{base} {added}'.format(base=cmd, added=param)

        resp = self.run_command(cmd=cmd)

        return resp

    def get_help(self):
        return self.run_command(cmd='-h')

    def create_order(self, name=None, algorithm=None, bit_length=None,
                     mode=None, payload_content_type=None, expiration=None):
        """ Creates an order using the Barbican cli client. """
        options = self._construct_option_str_from_dict({
            '--name': name,
            '--algorithm': algorithm,
            '--bit-length': bit_length,
            '--mode': mode,
            '--payload-content-type': payload_content_type,
            '--expiration': expiration
        })

        return self._action_command(
            BarbicanEntityType.ORDER, 'create', options)

    def store_secret(self, name=None, payload=None, payload_content_type=None,
                     payload_content_encoding=None, algorithm=None,
                     bit_length=None, mode=None, expiration=None):
        options = self._construct_option_str_from_dict({
            '--name': name,
            '--payload': payload,
            '--payload-content-type': payload_content_type,
            '--payload-content-encoding': payload_content_encoding,
            '--algorithm': algorithm,
            '--bit-length': bit_length,
            '--mode': mode,
            '--expiration': expiration
        })
        return self._action_command(
            BarbicanEntityType.SECRET, 'store', options)

    def get(self, entity_type, hateos_ref):
        return self._action_command(entity_type, 'get', hateos_ref)

    def list(self, entity_type):
        return self._action_command(entity_type, 'list')

    def verify(self):
        return self._action_command(BarbicanEntityType.VERIFICATION, 'verify')

    def delete(self, entity_type):
        return self._action_command(entity_type, 'delete')


class BarbicanEntityType(object):
    SECRET = 'secret'
    ORDER = 'order'
    VERIFICATION = 'verification'
