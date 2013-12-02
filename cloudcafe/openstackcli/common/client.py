import inspect
from cafe.engine.clients.commandline import BaseCommandLineClient


class BaseOpenstackPythonCLI_Client(BaseCommandLineClient):

    _KWMAP = {
        'os_username': 'os-username',
        'os_password': 'os-password',
        'os_tenant_name': 'os-tenant-name',
        'os_auth_url': 'os-auth-url',
        'os_region_name': 'os-region-name',
        'os_service_type': 'os-service-type',
        'os_service_name': 'os-service-name',
        'endpoint_type': 'endpoint-type',
        'os_cacert': 'os-cacert',
        'debug': 'debug',
        'retries': 'retries',
        'version': 'version'}

    _CMD = None

    def __init__(
            self, os_username=None, os_password=None, os_tenant_name=None,
            os_auth_url=None, os_region_name=None, os_service_type=None,
            os_service_name=None, endpoint_type=None, os_cacert=None,
            debug=False, retries=None, version=False):

        self.os_username = os_username
        self.os_password = os_password
        self.os_tenant_name = os_tenant_name
        self.os_auth_url = os_auth_url
        self.os_region_name = os_region_name
        self.os_service_type = os_service_type
        self.os_service_name = os_service_name
        self.os_cacert = os_cacert
        self.debug = debug
        self.retries = retries
        self.version = version

        super(BaseOpenstackPythonCLI_Client, self).__init__()

    def base_cmd(self):
        cmd_string = self._CMD
        for attr, flag in self._KWMAP.iteritems():
            value = self._process_boolean_flag_value(getattr(self, attr, None))
            if value is None:
                continue
            cmd_string += self._generate_cmd(flag, value)
        return cmd_string

    def _generate_cmd(self, flag, *values):
        return " --{0}{1}".format(
            flag, "".join([" {0}".format(v) for v in values]))

    def _dict_to_metadata_cmd_string(self, metadata):
        if isinstance(metadata, dict):
            return " ".join(
                ["{0}={1}".format(k, v) for k, v in metadata.iteritems()])

    def _process_boolean_flag_value(self, value):
        if isinstance(value, bool):
            value = str() if value else None
        return value

    def _process_command(self):
        """Creates a command from the calling function's locals() and executes
        that command."""
        # Get local vars of the function that called _process_command
        # Assumes that the calling function is an opencli client.
        frame = inspect.currentframe().f_back
        func_args, _, _, func_locals = inspect.getargvalues(frame)

        # Remove irrelevant local attrs and extract keyword map, command, and
        # response type object from the function's locals.
        func_args.remove('self')
        func_locals.pop('self', None)
        kwmap = func_locals.pop('_kwmap', dict())
        sub_command = func_locals.pop('_cmd', str())
        response_type = func_locals.pop('_response_type', None)

        # Assume every remaining non-private function local is a pythonified
        # version of a command flag's name.
        pythonified_flag_names = [
            attr for attr in func_locals.keys() if not attr.startswith('_')]

        # Assume that the name of every required function arg is the
        # name of a required (positional) command arg.
        # Extract required values (and their names) from the function locals
        req_arg_names = [name for name in func_args if name not in kwmap]
        req_arg_values = [func_locals[name] for name in req_arg_names]

        # Build a dictionary of optional flag names mapped to the values passed
        # into the function via those flag's pythonified flag names.
        optional_flags_dict = dict(
            (kwmap[name], func_locals[name])
            for name in pythonified_flag_names if name not in req_arg_names)

        # Build a string of all the optional flags and their values
        optional_flags_string = ""
        for flag, value in optional_flags_dict.iteritems():
            value = self._process_boolean_flag_value(value)
            if value is None:
                continue
            optional_flags_string = "{0}{1}".format(
                optional_flags_string, self._generate_cmd(flag, value))

        # Build the final command string
        cmd = "{base_cmd} {sub_cmd} {req_arg_values} {optional_flags}".format(
            base_cmd=self.base_cmd(),
            sub_cmd=sub_command,
            req_arg_values=' '.join([str(value) for value in req_arg_values]),
            optional_flags=optional_flags_string)

        # Execute the command and attach an entity object to the response, if
        # applicable.
        response = self.run_command(cmd)
        response_body_string = '\n'.join(response.standard_out)
        setattr(response, 'entity', None)
        if response_type is None:
            return response

        try:
            response.entity = response_type.deserialize(response_body_string)
        except Exception as exception:
            self._log.warning(
                "_response_entity object defined in {0} does not implement "
                "deserialize() classmethod".format(frame.f_code.co_name))
            self._log.exception(exception)

        return response
