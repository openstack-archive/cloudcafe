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

import collections
import os

from prettytable import PrettyTable

from cloudcafe.networking.networks.common.composites import CustomComposite
from cloudcafe.networking.networks.common.exceptions \
    import MissingDataException


class Resources(object):
    """Networking resource management class for list and delete methods.

    Attributes:
        resources (list): networking resources to manage, for ex.
            ['servers', 'keypairs', 'security_groups',
             'ports', 'subnets', 'networks']
        all (str): name pattern to be used by all resources. Except for the
            resources attributes with value.
        servers (str): name pattern used for servers if given.
        keypairs (str): name pattern used for keypairs if given.
        networks (str): name pattern used for networks if given.
        subnets (str): name pattern used for subnets if given.
        ports (str): name pattern used for ports if given.
        security_groups (str): name pattern used for security groups if given.
        failed_servers (list): for tracking delete failures on delete calls.
        failed_keypairs (list): for tracking delete failures on delete calls.
        failed_networks (list): for tracking delete failures on delete calls.
        failed_subnets (list): for tracking delete failures on delete calls.
        failed_ports (list): for tracking delete failures on delete calls.
        failed_security_groups (list): for tracking delete failures on delete.

    The class attributes are set after the set_resources call.
    """
    def __init__(self):
        self.resources = None

    def set_resources(self, resources, initial_val=None):
        """Setting resource values and failed list as class attributes

        Args:
            resources (list): resources list for ex.
                ['servers', 'networks', ...]
        """

        self.resources = resources

        # Initialize the resources as class attributes with None
        # And the resource delete lists as empty lists
        self.set_resources_val(initial_val)
        self.set_failed_deletes()

    def set_resources_val(self, val):
        """Setting attribute values to capture resource info

        Args:
            val(str): values of class attributes listed in self.resources
        """

        for resource in self.resources:
            setattr(self, resource, val)

    def set_failed_deletes(self):
        """Resetting attribute lists to track resource failed deletes"""

        for resource in self.resources:
            delete_list = 'failed_{0}'.format(resource)
            setattr(self, delete_list, list())

    def get_config_file(self, file_path=None):
        """Getting the config file

        Args:
            file_path(Optional[str]): config file path
        """

        if not file_path:
            file_path = os.environ.get('CAFE_CONFIG_FILE_PATH')
            if not file_path:
                msg = ('The file_path must be given or the environment '
                       'variable CAFE_CONFIG_FILE_PATH must be set')
                raise MissingDataException(msg)

        if not file_path.endswith('.config'):
            config_file = ''.join([file_path, '.config'])
        else:
            config_file = file_path
        return config_file

    def list_networking(self, name=None, file_path=None, verbose=True,
                        resource_show=None, resource_filter=None,
                        raise_exception=False):
        """Get method for networking related resources

        Args:
            name (Optional[str]): name pattern to filter by responses.
                If not given all resources will be listed.
            file_path (Optional[str]): config directory path with file name
                (the .config extension may be omitted). If not given the
                CAFE_CONFIG_FILE_PATH environment variable value will be used.
            verbose (Optional[bool]): flag to print delete msgs to console.
            resource_show (Optional[list]): resources to show only.
            resource_filter (Optional[list]): resources to skip showing.
                Ignored if resource_show given.
            raise_exception (Optional [bool]): flag for raising an exception
                if get calls throw an error.

        Returns:
            dict: ONLY if verbose is set to False, otherwise this info
                is printed by the method call. The names and id counts by
                resource are returned as well as a list of them on a table.

                For ex.
                {'subnets': {'table': <prettytable.PrettyTable object>
                             'names': 2, 'ids': 2},
                 'keypairs': {'table': <prettytable.PrettyTable object>,
                              'names': 0, 'ids': 0},
                 'networks': {'table': <prettytable.PrettyTable object>,
                              'names': 2, 'ids': 2},
                 'ports': {'table': <prettytable.PrettyTable object,
                           'names': 0, 'ids': 0},
                 'security_groups': {'table': <prettytable.PrettyTable object>,
                                     'names': 0, 'ids': 0},
                 'servers': {'table': <prettytable.PrettyTable object>,
                             'names': 3, 'ids': 3}}
        """

        config_file = self.get_config_file(file_path=file_path)

        if verbose:
            print 'Using config file {0}'.format(config_file)

        # Setting the custom composite
        com = CustomComposite(config_file_path=config_file)
        com.set_cafe_config_file_path()
        com.set_cafe_composites()

        # Defining resources get calls.
        res_fn = collections.OrderedDict([
            ('servers', {'res_com': com.net.behaviors,
                         'get_fn': 'list_servers'}),
            ('keypairs', {'res_com': com.net.behaviors,
                          'get_fn': 'list_keypairs'}),
            ('security_groups', {'res_com': com.sec.behaviors,
                                 'get_fn': 'list_security_groups'}),
            ('ports', {'res_com': com.ports.behaviors,
                       'get_fn': 'list_ports'}),
            ('subnets', {'res_com': com.subnets.behaviors,
                         'get_fn': 'list_subnets'}),
            ('networks', {'res_com': com.networks.behaviors,
                          'get_fn': 'list_networks'})
            ])

        resources = res_fn.keys()
        resources_count = dict()

        resource_set = set(resources)
        if resource_show:
            resources = list(resource_set.intersection(resource_show))
        elif resource_filter:
            resource_filter = list(resource_set.intersection(resource_filter))
            filter(resources.remove, resource_filter)

        output_list = []
        for resource in resources:
            output = PrettyTable()
            count = dict()
            res_com = res_fn[resource]['res_com']
            get_fn = res_fn[resource]['get_fn']
            params_kwargs = dict(raise_exception=raise_exception)

            resp = getattr(res_com, get_fn)(**params_kwargs)

            # Extracting the nested requests response object in networking
            # resources. This is not needed for the compute resources.
            if resource in ['networks', 'subnets', 'ports', 'security_groups']:
                resp = resp.response.entity

            name_list = res_com.get_name_list_from_entity_list(
                entity_list=resp, name=name)
            resource_name = '{0}_name'.format(resource)
            output.add_column(resource_name, name_list)
            names_count = len(name_list)
            count.update({'names': names_count})

            # For resources without ids like Keypairs
            if resource not in ['keypairs']:
                id_list = res_com.get_id_list_from_entity_list(
                    entity_list=resp, name=name)
                resource_id = '{0}_id'.format(resource)
                output.add_column(resource_id, id_list)
            else:
                id_list = []
            ids_count = len(id_list)
            count.update({'ids': ids_count})

            output.align = 'l'

            output_list.append(output)
            count.update({'table': output})
            resources_count.update({resource: count})

            if verbose:
                print output

        if verbose:
            print 'Resources Summary'
            for k, v in resources_count.items():
                report = '{0}: {1} with name and {2} with id'.format(
                    k, v['names'], v['ids'])
                print report
            note = ('NOTE: Some resources like ports, may have an empty string'
                    ' as name. Others, like keypairs, may not have id')
            print note
        else:
            # This is jut in case the printing is desired to be done elsewhere
            return resources_count

    def delete_networking(self, file_path=None, resource_dict=None,
                          timeout=None, raise_exception=None, verbose=True):
        """Clean up method for networking related resources

        Args:
            file_path (Optional[str]): config directory path with file name
                (the .config extension may be omitted). If not given the
                CAFE_CONFIG_FILE_PATH environment variable value will be used.
            resource_dict (Optional[dict]): Resource names to be used for
                deletion, all possible keys are,
                {'all': 'test*', 'servers': 'test_svr*', 'keypairs': 'test*',
                'security_group_rules': 'test*', 'security_groups': 'test*',
                'ports': 'ports*', 'subnets': 'test*', 'networks': 'test*'}

                The values heere are just name pattern examples and should be
                set to '*' for all or may have a resource start name like
                'test*', that will delete all resources starting with test
                on their name. You can also give a resource exact name, or
                an non matching pattern name to skip resource deletions.

                If the all key is given, all resources will be targeted for
                deletion with its value as the name pattern to be used.
                If other resource keys are given, in combination with the all
                key, these resource values will be used for their name pattern.

                If the all key is not given, only resource given keys will be
                targeted for deletion.

                If the resource dict is not given at all, the default value
                will be {'all': '*'} that will delete ALL resources.

            timeout (Optional[int]): wait time for server deletion. If not
                given default val compute.servers.config.server_build_timeout
            raise_exception (Optional [bool]): flag for raising an exception
                if servers aren't deleted within the timeout.
            verbose (Optional[bool]): flag to print delete msgs to console.
        """

        # Defining initial values
        config_file = self.get_config_file(file_path=file_path)

        if verbose:
            print 'Using config file {0}'.format(config_file)

        if not resource_dict:
            resource_dict = {'all': '*'}

        # Setting the custom composite
        com = CustomComposite(config_file_path=config_file)
        com.set_cafe_config_file_path()
        com.set_cafe_composites()

        # Defining resources delete calls. Delete order is important.
        res_fn = collections.OrderedDict([
            ('servers', {'res_com': com.net.behaviors,
                         'del_fn': 'wait_for_servers_to_be_deleted'}),
            ('keypairs', {'res_com': com.net.behaviors,
                          'del_fn': 'delete_keypairs'}),
            ('security_groups', {'res_com': com.sec.behaviors,
                                 'del_fn': 'delete_security_groups'}),
            ('ports', {'res_com': com.ports.behaviors,
                       'del_fn': 'delete_ports'}),
            ('subnets', {'res_com': com.subnets.behaviors,
                         'del_fn': 'delete_subnets'}),
            ('networks', {'res_com': com.networks.behaviors,
                          'del_fn': 'delete_networks'})
            ])

        resources = res_fn.keys()

        # Getting the name value for all resources if given
        all_resources = resource_dict.get('all')

        # Setting the resources as class attrs with initial name value
        self.set_resources(resources=resources, initial_val=all_resources)

        # Overwriting individual resource name value if given
        for k, v in resource_dict.items():
            setattr(self, k, v)

        for resource in resources:
            # Getting resources name patterns from class attrs
            name_pattern = getattr(self, resource)

            if name_pattern:

                if verbose:
                    msg = 'Deleting {0} with name: {1}'.format(resource,
                                                               name_pattern)
                    if resource == 'servers':
                        if timeout:
                            timeout_val = timeout
                        else:
                            timeout_val = (
                                'compute.servers.config.server_build_timeout')
                        add_msg = 'Within timeout: {0}'.format(timeout_val)
                        msg = '\n'.join([msg, add_msg])
                    print msg

                res_com = res_fn[resource]['res_com']
                del_fn = res_fn[resource]['del_fn']
                params_kwargs = dict(name=name_pattern)

                if resource == 'servers':
                    add_params = dict(timeout=timeout,
                                      raise_exception=raise_exception)
                    params_kwargs.update(add_params)

                failed_deletes = getattr(res_com, del_fn)(**params_kwargs)

                if verbose and failed_deletes:
                    msg = '\nUnable to delete the following {0}'.format(
                        resource)
                    print msg

                    for failure in failed_deletes:
                        print failure

                # Updating resource failure list in res object
                failed_name = 'failed_{0}'.format(resource)
                setattr(self, failed_name, failed_deletes)

        if verbose:
            print '\n'
            print '*'*9
            print 'Delete resource summary'
            print '"*" implies names starts with'
            print 'Resources list are all available resource options'
            print 'Failed lists populated with failures if any\n'
            print self
            print '*'*9

    def __repr__(self):
        """Representing resource attributes: str, int and list"""
        data = self.__dict__
        msg = ['Resources']
        for key, value in data.items():
            val_type = type(value)
            if val_type is str or val_type is int or val_type is list:
                s = '{0}: {1}'.format(key, value)
                msg.append(s)
        if len(msg) < 2:
            msg.append('No resources have been set')
        res = '\n'.join(msg)
        return res
