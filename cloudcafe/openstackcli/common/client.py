import inspect
from cafe.engine.clients.commandline import BaseCommandLineClient


class BaseOpenstackPythonCLI_Client(BaseCommandLineClient):

    _KWMAP = {
        'version': 'version',
        'debug': 'debug',
        'retries': 'retries',
        'os_username': 'os-username',
        'os_password': 'os-password',
        'os_tenant_name': 'os-tenant-name',
        'os_tenant_id': 'os-tenant-id',
        'os_auth_url': 'os-auth-url',
        'os_auth_sytem': 'os-auth-system',
        'os_region_name': 'os-region-name',
        'service_type': 'service-type',
        'service_name': 'service-name',
        'endpoint_type': 'endpoint-type',
        'os_cacert': 'os-cacert'}

    _CMD = 'openstack'

    def __init__(
            self, os_username=None, os_password=None, os_tenant_name=None,
            os_tenant_id=None, os_auth_url=None, os_auth_system=None,
            os_region_name=None, service_name=None, service_type=None,
            endpoint_type=None, os_cacert=None, retries=None, debug=False,
            version=False):

        self.os_username = os_username
        self.os_password = os_password
        self.os_tenant_name = os_tenant_name
        self.os_tenant_id = os_tenant_id
        self.os_auth_url = os_auth_url
        self.os_auth_system = os_auth_system
        self.os_region_name = os_region_name
        self.service_type = service_type
        self.service_name = service_name
        self.endpoint_type = endpoint_type
        self.os_cacert = os_cacert
        self.debug = debug
        self.retries = retries
        self.version = version

        super(BaseOpenstackPythonCLI_Client, self).__init__()

    def _generate_cmd(self, flag, *values):
        return " --{0}{1}".format(
            flag, "".join([" {0}".format(v) for v in values]))

    def _dict_to_metadata_cmd_string(self, metadata):
        if isinstance(metadata, dict):
            return " ".join(
                ["{0}={1}".format(k, v) for k, v in metadata.iteritems()])

    def base_cmd(self):
        cmd_string = self._CMD
        for attr, flag in self._KWMAP.iteritems():
            value = getattr(self, attr, None)
            if value is None:
                continue
            if isinstance(value, bool):
                if value is False:
                    continue
                value = ""
            cmd_string += self._generate_cmd(flag, value)
        return cmd_string

    def send(self, response_type=None):
        #Get function locals
        frame = inspect.getouterframes(inspect.currentframe(), 2)[1][0]
        func_args, _, _, func_locals = inspect.getargvalues(frame)

        #Use keyword map to map passed-in values to command strings
        func_args.remove('self')
        func_locals.pop('self', None)
        kwmap = func_locals.pop('_kwmap', dict())
        sub_command = func_locals.pop('_cmd', None)
        positional_flags = [attr for attr in func_args if attr not in kwmap]
        positional_values = [func_locals[attr] for attr in positional_flags]
        all_keys = func_locals.keys()
        command_value_dict = dict(
            (kwmap[attr], func_locals[attr])
            for attr in all_keys if attr not in positional_flags)

        optional_flag_string = ""
        for flag, value in command_value_dict.iteritems():
            if value is None:
                continue
            if isinstance(value, bool):
                if value is False:
                    continue
                value = ""
            optional_flag_string = "{0}{1}".format(
                optional_flag_string, self._generate_cmd(flag, value))

        cmd = (
            "{base_cmd} {sub_cmd} {positional_values} {optional_flags}".format(
                base_cmd=self.base_cmd(),
                sub_cmd=sub_command,
                positional_values=' '.join(
                    [str(value) for value in positional_values]),
                optional_flags=optional_flag_string))

        response = self.run_command(cmd)
        response_body_string = '\n'.join(
            line for line in response.standard_out)
        setattr(
            response, 'entity',
            response_type.deserialize(response_body_string))

        return response
