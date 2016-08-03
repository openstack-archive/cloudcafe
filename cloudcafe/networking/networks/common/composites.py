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


import os

from cloudcafe.compute.composites import _ComputeAuthComposite, \
    ComputeComposite
from cloudcafe.compute.config import ComputeEndpointConfig
from cloudcafe.compute.extensions.ip_associations_api.composites \
    import IPAssociationsComposite
from cloudcafe.networking.networks.composites import _NetworkingAuthComposite,\
    NetworkingComposite
from cloudcafe.networking.networks.config import NetworkingEndpointConfig, \
    UserAuthConfig, UserConfig
from cloudcafe.networking.networks.extensions.ip_addresses_api.composites \
    import IPAddressesComposite
from cloudcafe.networking.networks.extensions.limits_api.composites \
    import LimitsComposite
from cloudcafe.networking.networks.extensions.security_groups_api.composites \
    import SecurityGroupsComposite


class CustomComposite(object):
    """
    @summary: Creates customized composites for networking specifying a
        config file and/or overwriting the config section parameters from
        networking_endpoint, user, and user_auth_config.
    """
    CAFE_CONFIG_FILE_PATH = 'CAFE_CONFIG_FILE_PATH'

    def __init__(self, region=None, networking_endpoint_name=None,
                 networking_endpoint_url=None, compute_endpoint_name=None,
                 compute_endpoint_url=None, auth_endpoint=None,
                 strategy=None, username=None, api_key=None, tenant_id=None,
                 user_id=None, project_id=None, passcode=None, password=None,
                 tenant_name=None, config_file_path=None):
        """
        @param region: environment region, for ex. QE-ORD, DFW, IAD, etc.
            (networking_endpoint and compute_endpoint config file param)
        @type region: str
        @param networking_endpoint_name: service catalog name to get the
        publicURL, for ex. cloudNetworks (networking_endpoint config file
            section param)
        @type networking_endpoint_name: str
        @param networking_endpoint_url: to override publicURL from the catalog
            (networking_endpoint config file section param)
        @type networking_endpoint_url: str

        @param compute_endpoint_name: service catalog name to get the
        publicURL, for ex. cloudServersOpenStack (compute_endpoint config file
            section param)
        @type compute_endpoint_name: str
        @param compute_endpoint_url: to override publicURL from the catalog
            (compute_endpoint config file section param)
        @type compute_endpoint_url: str
        @param auth_endpoint: authentication endpoint for user credentials
        @type auth_endpoint: str
        @param strategy: type of authentication exposed by the auth_endpoint.
           Currently supported values: keystone, rax_auth, rax_auth_mfa, and
           saio_tempauth
        @type strategy: str
        @param username: name of the user
        @type username: str
        @param api_key: user api key
        @type api_key: str
        @param tenant_id: user tenant ID
        @type tenant_id: str
        @param user_id: user ID
        @type user_id: str
        @param project_id: user project ID (usually same as tenant ID)
        @type project_id: str
        @param passcode: auth MFA secondary password (passcode)
        @type passcode: str
        @param password: user password
        @type password: str
        @param tenant_name: user tenant name
        @type tenant_name: str
        @param config_file_path: to override the CAFE_CONFIG_FILE_PATH file
        @type config_file_path: str

        """
        # networking_endpoint section params (region is also used by compute)
        self.region = region
        self.networking_endpoint_name = networking_endpoint_name
        self.networking_endpoint_url = networking_endpoint_url

        # compute_endpoint section params
        self.compute_endpoint_name = compute_endpoint_name
        self.compute_endpoint_url = compute_endpoint_url

        # user_auth_config section params
        self.auth_endpoint = auth_endpoint
        self.strategy = strategy

        # user section params
        self.username = username
        self.api_key = api_key
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.project_id = project_id
        self.passcode = passcode
        self.password = password
        self.tenant_name = tenant_name

        # To track all config file paths used
        self.config_file_path_records = []

        # Overwriting config file path if given
        self.config_file_path = config_file_path
        self.set_cafe_config_file_path()

        # Setting the new config objects
        self.set_cafe_configs()

        # Networking composites and sub-composites
        self.net = None
        self.networks = None
        self.subnets = None
        self.ports = None

        # Extension composites: security groups (sec), IP addresses (ipaddr),
        # limits, and IP associations (ipassoc).
        self.sec = None
        self.ipaddr = None
        self.ipassoc = None

        # Compute composites and sub-composites
        self.compute = None
        self.flavors = None
        self.images = None
        self.servers = None
        self.keypairs = None

        # Initially setting the networking composite only
        self.set_cafe_composites(composites=['networking'])

    def set_cafe_configs(self, configs=None):
        """Setting attributes for new config objects"""
        if not configs:
            configs = ['user', 'user_auth', 'compute_endpoint',
                       'networking_endpoint']

        if 'user' in configs:
            self.set_user_config()
        if 'user_auth' in configs:
            self.set_user_auth_config()
        if 'compute_endpoint' in configs:
            self.set_compute_endpoint_config()
        if 'networking_endpoint' in configs:
            self.set_networking_endpoint_config()

    def set_cafe_config_file_path(self):
        """Updating the cafe config file path value"""
        self.config_file_path_records.append(os.environ.get(
            self.CAFE_CONFIG_FILE_PATH))
        if self.config_file_path:
            os.environ.update({self.CAFE_CONFIG_FILE_PATH:
                               self.config_file_path})

    def reset_cafe_config_file_path(self):
        """Resetting to the previous cafe config file path value"""
        if self.config_file_path_records:
            previous_config_file = self.config_file_path_records.pop()
            os.environ.update({self.CAFE_CONFIG_FILE_PATH:
                               previous_config_file})

    def reset_attr_values(self, attrs=None):
        """
        @summary: Setting to None the class config values
        """
        if not attrs:
            attrs = ['region', 'networking_endpoint_name',
                     'networking_endpoint_url', 'compute_endpoint_name',
                     'compute_endpoint_url', 'auth_endpoint', 'strategy',
                     'username', 'api_key', 'tenant_id', 'user_id',
                     'project_id', 'passcode', 'password', 'tenant_name']

        for val in attrs:
            setattr(self, val, None)

    def set_cafe_composites(self, composites=None):
        """
        @summary: Setting customized composites
        @param composites: composites to set, for ex. ['networking']
        @type composites: list
        """

        # setting all if not given
        if not composites:
            composites = ['networking', 'compute', 'ip_associations',
                          'security_groups', 'ip_addresses', 'limits']

        # Compute needs to go first since used by networking
        if 'compute' in composites:
            self.compute = ComputeComposite(
                auth_composite=self.compute_auth_composite)
            self.flavors = self.compute.flavors
            self.images = self.compute.images
            self.servers = self.compute.servers
            self.keypairs = self.compute.keypairs
        if 'networking' in composites:
            self.net = NetworkingComposite(
                auth_composite=self.networking_auth_composite)
            self.networks = self.net.networks
            self.subnets = self.net.subnets
            self.ports = self.net.ports

            # need to overwrite the compute composite at networking
            self.net.behaviors.compute = self.compute

        if 'ip_associations' in composites:
            self.ipassoc = IPAssociationsComposite(
                auth_composite=self.compute_auth_composite)
        if 'security_groups' in composites:
            self.sec = SecurityGroupsComposite(
                auth_composite=self.networking_auth_composite)
        if 'ip_addresses' in composites:
            self.ipaddr = IPAddressesComposite(
                auth_composite=self.networking_auth_composite)
        if 'limits' in composites:
            self.limits = LimitsComposite(
                auth_composite=self.networking_auth_composite)

    @property
    def networking_auth_composite(self):
        """Getting customized networking auth composite"""

        return _NetworkingAuthComposite(
            networking_endpoint_config=self.networking_endpoint_config,
            user_auth_config=self.user_auth_config,
            user_config=self.user_config)

    @property
    def compute_auth_composite(self):
        """Getting customized compute auth composite"""

        return _ComputeAuthComposite(
            compute_endpoint_config=self.compute_endpoint_config,
            endpoint_config=self.user_auth_config,
            user_config=self.user_config)

    def set_networking_endpoint_config(self):
        """Setting the updated self._new_networking_endpoint_config attr"""
        endpoint_config = NetworkingEndpointConfig()

        new_config_kwargs = dict(
            region=self.region,
            networking_endpoint_name=self.networking_endpoint_name,
            networking_endpoint_url=self.networking_endpoint_url)

        self._new_networking_endpoint_config = \
            Clone(obj_to_clone=endpoint_config, new_kwargs=new_config_kwargs)

    @property
    def networking_endpoint_config(self):
        """Returning the networking_endpoint config"""
        return self._new_networking_endpoint_config

    def set_compute_endpoint_config(self):
        """Setting the updated self._new_compute_endpoint_config attribute"""
        endpoint_config = ComputeEndpointConfig()

        new_config_kwargs = dict(
            region=self.region,
            compute_endpoint_name=self.compute_endpoint_name,
            compute_endpoint_url=self.compute_endpoint_url)

        self._new_compute_endpoint_config = Clone(obj_to_clone=endpoint_config,
                                                  new_kwargs=new_config_kwargs)

    @property
    def compute_endpoint_config(self):
        """Returning the compute_endpoint config"""
        return self._new_compute_endpoint_config

    def set_user_auth_config(self):
        """Setting the updated self._new_user_auth_config attribute"""
        user_auth_config = UserAuthConfig()

        # in the config file auth_endpoint is just endpoint
        new_config_kwargs = dict(auth_endpoint=self.auth_endpoint,
                                 strategy=self.strategy)

        self._new_user_auth_config = Clone(obj_to_clone=user_auth_config,
                                           new_kwargs=new_config_kwargs)

    @property
    def user_auth_config(self):
        """Returning the user_auth_config"""
        return self._new_user_auth_config

    def set_user_config(self):
        """Setting the updated self._new_user_config attribute"""
        user_config = UserConfig()
        new_config_kwargs = dict(
            username=self.username, api_key=self.api_key,
            tenant_id=self.tenant_id, user_id=self.user_id,
            project_id=self.project_id, passcode=self.passcode,
            password=self.password, tenant_name=self.tenant_name)

        self._new_user_config = Clone(obj_to_clone=user_config,
                                      new_kwargs=new_config_kwargs)

    @property
    def user_config(self):
        """Returning the user config"""
        return self._new_user_config

    def __repr__(self):
        """Representing custom config data"""
        data = self.__dict__
        msg = ['Custom config data:']
        for key, value in data.items():
            if type(value) is str:
                s = '{0}: {1}'.format(key, value)
                msg.append(s)
        s = '\n{0} records: {1}'.format(self.CAFE_CONFIG_FILE_PATH,
                                        self.config_file_path_records)
        msg.append(s)
        res = '\n'.join(msg)
        return res


class Clone(object):
    """Class to create custom objects"""
    def __init__(self, obj_to_clone, new_kwargs=None):
        """
        @param obj_to_clone: instance of object to copy for ex. UserConfig()
        @type obj_to_clone: instance
        @param new_kwargs: attributes to set in new copy (clone)
        @type new_kwargs: dict
        """
        original_attrs = dir(obj_to_clone)

        # Copying the object data to the clone
        for attr in original_attrs:
            if not attr.startswith('_'):
                val = getattr(obj_to_clone, attr, None)
                setattr(self, attr, val)

        # Setting new data into the clone
        for key, val in new_kwargs.items():
            if val:
                setattr(self, key, val)
