from collections import OrderedDict
import pexpect


class SshUnableToConnect(Exception):
    MSG = 'Unable to connect to: {ip} (Type: {t_type})'

    def __init__(self, target_ip=None, target_type=None):
        target_type = target_type or 'Not Specified'
        args = {'ip': target_ip, 't_type': target_type}
        self.message = self.MSG.format(**args)

    def __str__(self):
        return self.message


class MissingCredentials(SshUnableToConnect):
    MSG = 'Missing credentials to connect to: {ip} (Type: {t_type})'


class SshResponse(object):
    str_concat = '{0!s}\n{1!s}'

    def __init__(self):
        """
        Supports pexpect connection info:
            + Contains open connection (if open)
            + Tracks various aspects of open connection: STDOUT, STDIN, STDERR
            + Tracks I/O per command (if commands issued over SSH connection)
            + errors = Any caught exceptions

            + stdin = all stdin
            + stdout = all stdout
            + output = interlaced stdin/stdout

        """
        self.stdout = ''
        self.stdin = ''
        self.stderr = ''
        self.output = ''
        self.cmd_output = OrderedDict()
        self.errors = ''
        self.connection = None

    def _add(self, attribute, value):
        prop = getattr(self, attribute, self.stdout)
        setattr(self, attribute, self.str_concat.format(prop, value))
        self.output = self.str_concat.format(self.output, value)

    def add_to_stdin(self, value):
        self._add('stdin', value)

    def add_to_stdout(self, value):
        self._add('stdout', value)

    def add_to_stderr(self, value):
        self._add('stderr', value)

    def add_to_cmd_out(self, cmd, value):
        self._add('stdout', value)
        self.cmd_output[cmd] = value

    @property
    def result(self):
        return self.errors == ''


class SshMixin(object):

    PSWD_PROMPT_REGEX = r'ssword\:\s*'
    LINUX_PROMPT_REGEX = r'[$#>]\s*$'
    SSH_KEY_REGEX = r'connecting\s+\(yes\/no\)\?\s*'

    DEFAULT_CMD = 'ls -alF'

    def connect_to_proxy(
            self, user=None, ip_address=None, password=None):
        """
        Connect to proxy or local host

        Note: Parameters are only for the remote connections

        @param user: Use different user other than registered proxy user
        @param password: Use different password other than registered pswd
        @param ip_address: Use specific IP address other than proxy address

        @return: Active SSH connection to target

        """

        user = user or self.proxy_server_user
        ip_address = ip_address or self.proxy_server_address
        password = password or self.proxy_server_password

        # Establish connection to proxy and return open connection
        if self.use_proxy:
            response_obj = self._ssh_from_here(
                user=user, password=password, target_ip=ip_address)
            conn = response_obj.connection

            self.last_response = response_obj

        # Return nothing, since it is a local connection.... for now, user can
        # open pipe/process for local connection.
        else:
            conn = self._connect_to_local_proxy()

        return conn

    def can_ssh(self, target_ip, user, password, cmd=DEFAULT_CMD):
        """
        Verifies SSH connectivity to specific target. The routine will connect
        to the target IP and issue a single command. If the command returns
        anything, including an error, SSH login was successful.

        @param target_ip: SSH to IP
        @param user: Log in as user 'x'
        @param password: Log in using password
        @param cmd: Command to execute if login worked

        @return: (Boolean) : Did SSH work? True=YES, False=No

        """
        output = self.ssh_to_target(
            target_ip=target_ip, user=user, password=password, cmds=[cmd])
        self.last_response = output
        return cmd in output.output

    def ssh_to_target(
            self, target_ip=None, user=None, password=None, cmds=None,
            proxy_user=None, proxy_pswd=None, proxy_ip=None,
            close_when_done=True, response_obj=None):
        """
        SSH to the target host from the specified host. If target_ip is not
        specified, the response_obj with an open connection must be provided.
        The open connection will be used to use the commands. If neither the
        (target_ip, user, and password) or the response_obj is specified,
        an UnableToConnect exception will be raised.

        NOTE: Currently as implemented, only Linux hosts are supported by this
        routine.

        NOTE: These parameters are only optional if the response_obj is not
        provided.

        :param target_ip: IP Address to connect to
        :param user: username for SSH connection
        :param password: password for SSH connection

        :param proxy_user: Specify different user than what was configured in
            the proxy_mgr.
        :param proxy_pswd: Specify different password than what was
            configured in the proxy_mgr.
        :param proxy_ip: Specific different target IP than what was
            configured in the proxy mgr.
        :param close_when_done: Close the connection when complete.
        :param cmds: OrderDict  of cmds to execute to verify connection
            (DEFAULT = 'ls -alF'). The Key is the command, the value is the
            regexp needed to validate the cmd response. If no commands are
            executed, the open connection is returned within the response
            object.
        :param response_obj: Provided SshResponse Object a for open
            connection to pass cmds to...

        :return: SSH Response object
        """
        if response_obj is not None:
            self.display_conn_info(response_obj)

        if response_obj is None:

            # Make sure there is an IP to connect to...
            if target_ip is None:
                raise SshUnableToConnect(
                    target_ip=target_ip, target_type='target server')

            password = password or self.proxy_server_password
            if None in [user, password]:
                raise MissingCredentials(
                    target_ip=target_ip, target_type='target server')

            # Ok, we have enough info to log in...
            msg = 'No connection was provided. Establishing connection.'
            self.logger.info(msg)
            ssh_args = {'target_ip': target_ip, 'user': user,
                        'password': password}

            # If we need a proxy
            if self.use_proxy:

                # Get the proxy connection info...
                proxy_user = proxy_user or self.proxy_server_user
                proxy_pswd = proxy_pswd or self.proxy_server_password
                proxy_ip = proxy_ip or self.proxy_server_address

                if None in [proxy_user, proxy_pswd, proxy_ip]:
                    raise MissingCredentials(
                        target_ip=proxy_ip, target_type='proxy server')

                # Establish and save the connection to proxy server
                proxy_connection = self._ssh_from_here(
                    target_ip=proxy_ip, user=proxy_user, password=proxy_pswd)
                ssh_args['response_obj'] = proxy_connection

                self.logger.debug('Connection Hop Path: {0}'.format(
                    self._conn_path))

                # Make sure we connected...
                if proxy_connection.connection is None:
                    self.logger.error(
                        'Unable to connect to proxy: {ip}'.format(ip=proxy_ip))
                    self.logger.error(proxy_connection.errors)
                    raise SshUnableToConnect(
                        target_ip=proxy_ip, target_type='proxy')

            # Make SSH connection and verify connection was successful.
            response_obj = self._ssh_from_here(**ssh_args)
            if response_obj.connection is None:
                self.logger.error(
                    'Unable to connect to host: {ip}'.format(ip=proxy_ip))
                self.logger.error(response_obj.errors)
                self.logger.debug('Connection Hop Path: {0}'.format(
                    self._conn_path))

                raise SshUnableToConnect(
                    target_ip=target_ip, target_type='target server')

        # If there are commands to execute
        if cmds is not None:
            response_obj = self._cmds_via_open_connection(response_obj, cmds)

        self.last_response = response_obj

        # Close the connection if necessary.
        if close_when_done:
            self.close_connections(response_obj)

        return response_obj

    def _ssh_from_here(self, target_ip, user, password, response_obj=None):
        """
        Connect via ssh using a pexpect process from the local host or an
        open pexpect connection to remote host.

        @param target_ip: The IP address of the target host
        @param user: Username on target host to connect to host as...
        @param password: Password on target host to connect to host as...
        @param cmd: Command to execute on the host to validate connection
        @param timeout: Connection Timeout (if exceeded, stop trying connection
            and make connection as FAILED).

        @return: String of connection output.

        """
        response_obj = response_obj or SshResponse()
        self.session_password = password

        ssh_options = ('-oStrictHostKeyChecking=no '
                       '-oUserKnownHostsFile=/dev/null')

        # Build SSH command
        ssh_cmd = 'ssh {options} {user}@{ip}'.format(
            user=user, ip=target_ip, options=ssh_options)
        self.logger.debug('SSH INVOCATION CMD: {cmd}'.format(cmd=ssh_cmd))
        response_obj.add_to_stdin(ssh_cmd)

        # Build list of potential and expected output
        # NOTE: LINUX_REGEX_PROMPT must be the last entry in the ordered dict
        expectations = OrderedDict([
            (pexpect.TIMEOUT, None),
            (self.PSWD_PROMPT_REGEX, password),
            (self.SSH_KEY_REGEX, 'yes'),
            (self.LINUX_PROMPT_REGEX, None)])

        # Set ssh process from the open connection
        ssh_process = response_obj.connection

        # If the open connection was empty, establish it from the local host
        if ssh_process is None:
            ssh_process = pexpect.spawn(ssh_cmd)

            if ssh_process is None:
                self.logger.error(
                    'Unable to connect to host: {ip}'.format(ip=target_ip))
                raise SshUnableToConnect(target_ip=target_ip)

            # Record the IP to track hops
            if target_ip not in self._conn_path:
                self._conn_path.append(target_ip)
            ssh_process.delaybeforesend = self._pexpect_cmd_delay
            response_obj.connection = ssh_process

        # Use the open connection to establish an SSH connection to the target
        else:
            ssh_process.sendline(ssh_cmd)
            if target_ip not in self._conn_path:
                self._conn_path.append(target_ip)

        while True:

            # Watch the connection for expected output.
            try:
                response = ssh_process.expect(expectations.keys())

            # TIMEOUT, break out of loop and indicate FAILURE
            except pexpect.TIMEOUT:
                err = "SSH'ing to target timed out. {0} --> {1}"
                err_msg = err.format(
                    ssh_process.before, ssh_process.after)
                self.logger.error(err_msg)

                # Record IO and remove IP from the tracking list
                response_obj.add_to_stdout(
                    str(ssh_process.before) + str(ssh_process.after))
                self._conn_path.pop()

                if not self._conn_path:
                    response_obj.connection = None
                break

            # CONNECTION CLOSED, save output and break out of loop.
            except pexpect.EOF:
                self.logger.debug('Reached END OF FILE')
                response_obj.add_to_stdout(
                    str(ssh_process.before) + str(ssh_process.after))
                self._conn_path.pop()
                if not self._conn_path:
                    response_obj.connection = None
                break

            # If TIMEOUT returned by response, break out of loop and indicate
            # FAILURE...
            if response == 0:
                err = "SSH'ing target timed out. {0} --> {1}"
                self.logger.error(err.format(
                    ssh_process.before, ssh_process.after))
                response_obj.add_to_stdout(
                    str(ssh_process.before) + str(ssh_process.after))
                self._conn_path.pop()
                if not self._conn_path:
                    response_obj.connection = None
                break

            # Connection established, the expected prompt was found
            # (last element in the expectation ordered dict)
            if response == len(expectations.keys()) - 1:
                response_obj.add_to_stdout(
                    str(ssh_process.before) + str(ssh_process.match.group()))
                break

            # Received expected output, transmit corresponding input
            next_transmit = expectations[expectations.keys()[response]]
            if next_transmit is None:
                self.logger.warn("Didn't drop out of loop, but nothing "
                                 "additional to transmit.")
                self.logger.debug('Option pexpect returned: {0} of {1}'.format(
                    response, len(expectations.keys()) - 1))
                self.logger.debug('Transaction thus far:\n{0}'.format(
                    str(ssh_process.before) + str(ssh_process.match.group()) +
                    str(ssh_process.after)))
                break

            # Transmit the next command in the process based on matched
            # expectation
            self.logger.debug("TX'ing: '{0}'".format(next_transmit))
            response_obj.add_to_stdout(str(ssh_process.before) +
                                       ssh_process.match.group())
            response_obj.add_to_stdin(next_transmit)
            ssh_process.sendline(next_transmit)

        # Broke from loop, return all received output...
        self.last_response = response_obj
        return response_obj

    def _cmds_via_open_connection(self, response_obj, cmds):
        """
        SSH from the local host using pexpect.

        @param response_obj: Populated SshResponse Obj
        @param cmds: Ordered Dict of commands to execute on the host to
                validate connection

        @return: SshResponse Obj

        """
        # Build list of potential and expected output
        expectations = OrderedDict([
            (pexpect.TIMEOUT, None),
            (self.PSWD_PROMPT_REGEX, self.session_password),
            (self.LINUX_PROMPT_REGEX, None)])

        # Get the SSH connection to the target host
        ssh_process = response_obj.connection

        for cmd in cmds:
            self.logger.debug("TX'ing CMD: '{0}'".format(cmd))
            ssh_process.sendline(cmd)
            response_obj.add_to_stdin(cmd)

            while True:

                # Watch connection for potential and expected output.
                try:
                    response = ssh_process.expect(expectations.keys())

                # TIMEOUT, break out of loop and indicate FAILURE
                except pexpect.TIMEOUT:
                    err = "CMD '{cmd}' timed out. {before} --> {after}"
                    self.logger.error(err.format(
                        before=ssh_process.before, after=ssh_process.after,
                        cmd=cmd))
                    self.logger.debug('Connection Hop Path: {0}'.format(
                        self._conn_path))

                    response_obj.add_to_stdout(str(ssh_process.before))
                    if not self._conn_path:
                        response_obj.connection = None
                    break

                # CONNECTION CLOSED, save output and break out of loop.
                except pexpect.EOF:
                    self.logger.debug('Reached END OF FILE')
                    response_obj.add_to_stdout(str(ssh_process.before))
                    if cmd == 'exit':
                        output = (str(ssh_process.before) +
                                  str(ssh_process.after))
                        response_obj.add_to_cmd_out(cmd, output)

                    self._conn_path.pop()
                    if not self._conn_path:
                        response_obj.connection = None
                    break

                # If TIMEOUT returned by response, break out of loop and
                # indicate FAILURE...
                if response == 0:
                    err = "CMD '{cmd}' timed out. {before} --> {after}"
                    self.logger.error(err.format(
                        before=ssh_process.before, after=ssh_process.after,
                        cmd=cmd))

                    response_obj.add_to_stdout(
                        str(ssh_process.before) + str(ssh_process.after))
                    self.logger.debug('Connection Hop Path: {0}'.format(
                        self._conn_path))
                    break

                if response == (len(expectations.keys()) - 1):
                    self.logger.debug('CMD {cmd} issued.'.format(cmd=cmd))
                    output = (str(ssh_process.before) +
                              ssh_process.match.group() +
                              str(ssh_process.after))
                    response_obj.add_to_cmd_out(cmd, output)
                    self.last_response = response_obj
                    break

                # Transmit the next command/input based on matched expectation
                next_transmit = expectations[expectations.keys()[response]]
                self.logger.debug("TX'ing: '{0}'".format(next_transmit))
                response_obj.add_to_stdout(
                    str(ssh_process.before) + ssh_process.match.group())
                response_obj.add_to_stdin(next_transmit)
                self.last_response = response_obj

        # Broke from loop, return all received output...
        self.last_response = response_obj
        return response_obj

    def close_connections(self, response_obj):
        """
        Close all open connections, based on IP/hop tracking

        @param response_obj: Populated SshResponse Object

        @return: None

        """
        self.logger.debug('Closing all open connections: {0}'.format(
            self._conn_path))

        # If there are connections open...
        if getattr(response_obj, 'connection', None) is not None:

            # Iterate through the hop list (if the connection is still open)
            while (list(set(self._conn_path)) and
                    response_obj.connection is not None):

                response_obj = self._cmds_via_open_connection(
                    response_obj, ['exit'])
                self.last_response = response_obj
