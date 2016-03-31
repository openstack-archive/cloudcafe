#!/usr/bin/env python

from cafe.common.reporting import cclogging

from cloudcafe.networking.networks.common.proxy_mgr.ping_util \
    import PingMixin
from cloudcafe.networking.networks.common.proxy_mgr.ssh_util \
    import SshMixin

# For available utility routines, please refer to the inherited mixins


class NoPasswordProvided(Exception):
    def __init__(self):
        self.message = ("Server Model Obj does not have the 'admin_pass' "
                        "attribute set")

    def __str__(self):
        return self.message


class NetworkProxyMgr(PingMixin, SshMixin):

    LINUX = 'linux'
    WINDOWS = 'windows'
    OS = [LINUX, WINDOWS]

    DEFAULT_USER = 'root'
    PROMPT_PATTERN = r'[$#>]\s*$'

    STANDARD_CMD_DELAY = 0.5

    def __init__(self, use_proxy=True, proxy_os=LINUX, ip_version=4,
                 logger=None, debug=False):
        """
        Proxy Server Constructor
        @param use_proxy: (Boolean) - Is there a proxy/bastion that should
            execute commands or be used as a hop to another address?
            True - Yes
            False - No, execute cmds from the localhost.
        @param proxy_os: (ENUM) - Support for multiple OSs. A hook for
            future functionality. Only supports Linux currently.
        @param ip_version: Version to use by default, if utilities differ
            across IP versions.
        @param logger: Logging functionality.
        @param debug: (Boolean) Used for debugging system and mixin utiliies

        @return: None
        """

        self.use_proxy = use_proxy

        self._proxy_svr = None
        self._proxy_ip = None
        self._proxy_os = proxy_os
        self._ip_version = ip_version
        self.logger = logger or cclogging.getLogger(
            cclogging.get_object_namespace(self.__class__))
        self.connection = None
        self.debug = debug
        self.session_password = None
        self.prompt_pattern = self.PROMPT_PATTERN
        self.last_response = None

        # Track IPs (hops) currently connected to...
        self._conn_path = []

        # Delay between commands if iterating a list of commands
        self._pexpect_cmd_delay = self.STANDARD_CMD_DELAY

    def set_proxy_server(
            self, server_obj, username=DEFAULT_USER, password=None):
        """
        Saves server model representing the proxy server (compute model)
        If obj does not contain the password, please provide it, it's difficult
        to connect otherwise...

        @param server_obj: compute model representation of server
        @param username: User to log into proxy
        @param password: password for compute VM

        @return: None

        """

        # Determine if the password is set
        if password is not None:
            server_obj.admin_pass = password

        if (not hasattr(server_obj, 'admin_pass') or
                getattr(server_obj, 'admin_pass', None) is None):
            raise NoPasswordProvided()

        server_obj.username = username

        self._proxy_svr = server_obj
        self._proxy_ip = getattr(self._proxy_svr.addresses.public,
                                 'ipv{ver}'.format(ver=self._ip_version))

    @property
    def proxy_server_address(self):
        return self._proxy_ip

    @property
    def proxy_server_password(self):
        return self._proxy_svr.admin_pass

    @proxy_server_password.setter
    def proxy_server_password(self, password):
        self._proxy_svr.admin_pass = password

    @property
    def proxy_server_name(self):
        return self._proxy_svr.name

    @property
    def proxy_server_user(self):
        return self._proxy_svr.username

    @property
    def proxy_server_obj(self):
        return self._proxy_svr

    @proxy_server_obj.setter
    def proxy_server_obj(self, obj):
        self.set_proxy_server(server_obj=obj)

    def display_conn_info(self, conn_info):
        """
        Display connection info and all input/output at time of invocation,
        plus input/output per command

        @param conn_info: Populated SshResponse Object (proxy_mgr.ssh_util)
        @return: None

        """
        output = ("Connection:\n{conn}\nSTDOUT:\n{stdout}\nSTDIN:\n"
                  "{stdin}\nALL:\n{all}").format(
            conn=conn_info, stdin=conn_info.stdin, stdout=conn_info.stdout,
            all=conn_info.output)

        per_command = "\n\nPER COMMAND:\n"
        for cmd, out in conn_info.cmd_output.iteritems():
            command_str = "CMD: '{0}'\n{1}\n\n".format(cmd, out)
            per_command = '{0}\n{1}'.format(per_command, command_str)

        self.logger.debug("{0}\n{1}".format(output, per_command))

    @staticmethod
    def _connect_to_local_proxy():
        """
        Placeholder in case there is a different mechanism used to connect
        to the local host (e.g. - subprocess() or popen())

        @return: None

        """
        return None

# Basic test to verify functionality
if __name__ == '__main__':

    def display_conn_info(conn_info):
        print "Connection:", conn_info
        print '\nSTDOUT\n', conn_info.stdout
        print '\nSTDIN\n', conn_info.stdin
        print '\n\nALL\n', conn_info.output

        print "\n\nPER COMMAND:\n"
        for cmd, out in conn_info.cmd_output.iteritems():
            print "CMD: '{0}'\n{1}\n\n".format(cmd, out)

    class Proxy(object):
        def __init__(self, password=None, username=None, id_=None):
            self.admin_pass = password
            self.username = username
            self.id = id_

    # Flags to test specific scenarios (local/proxy, ping/ssh/both)
    use_proxy = True
    ssh = True
    ping = True

    # Test connect via localhost
    # THESE VALUES NEED TO BE UPDATED TO USE EXISTING VM (UP TO USER)
    proxy = NetworkProxyMgr(use_proxy=use_proxy, ip_version=4, logger=None,
                            debug=True, proxy_os=NetworkProxyMgr.LINUX)

    username = 'root'
    password = '<insert password>'
    proxy._proxy_ip = '<insert proxy ip>'
    target_ip = '<insert target ip>'
    target_id = '<insert target host id>'   # For tracking purposes only

    proxy._proxy_svr = Proxy(
        username=username, password=password, id_='<insert proxy host id>')

    commands = ['ls -alF', 'hostname -I', 'exit']

    if ping:
        print "PING {0} --> {1}".format(target_ip, proxy.ping(target_ip))

    if ssh:
        response = proxy.ssh_to_target(
            target_ip=target_ip, user=username, password=password,
            proxy_user=username, proxy_pswd=password,
            proxy_ip=proxy._proxy_ip, cmds=commands)

        display_conn_info(response)
        print "CONNS:", proxy._conn_path
