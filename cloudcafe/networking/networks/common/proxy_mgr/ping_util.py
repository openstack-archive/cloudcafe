from collections import OrderedDict
import re

import pexpect

from cafe.engine.ssh.models.ssh_response import ExecResponse


class PingMixin(object):

    PING_COUNT = 5
    PING_PACKET_LOSS_REGEX = r'\s*(?P<received>\d+)\s+received,'
    LINUX_PROMPT_PATTERN = r'[$#>]\s*$'

    def ping(self, target_ip, count=PING_COUNT, threshold=1, ip_version=4):
        """
        Ping a target IP (using remote proxy or local host)

        @param target_ip: IP address to ping
        @param count: Number of echo requests to issue
        @param threshold: Number of echo requests required to determine success
        @param ip_version: Version of the IP address to ping.

        @return: Boolean: Is target online?

        """
        api = self._ping_from_here
        if self.use_proxy:
            api = self._ping_from_remote_client

        output = api(target_ip, count, ip_version=ip_version)
        return self._validate_ping_response(
            ip=target_ip, response=output, threshold=threshold)

    def _ping_from_remote_client(
            self, target_ip, count=PING_COUNT, ip_version=4):
        """ Ping target from a remote host. Connects to the proxy, and then
           pings through proxy connection.

        @param target_ip:  The IP address of the target host
        @param count: Number of pings to attempt
        @param ip_version: Version of the IP address to ping.

        @return String of ping cmd output.

        """
        # Get open client connection
        connection = self.connect_to_proxy()

        # Execute ping command on remote command
        return self._ping_from_here(
            target_ip=target_ip, count=count, connection=connection,
            ip_version=ip_version)

    def _ping_from_here(
            self, target_ip, count=PING_COUNT, connection=None, ip_version=4):
        """
        Ping target from the execution (local) host

        @param target_ip:  The IP address of the target
        @param count: Number of pings to attempt
        @param connection: Active pexpect session (from self.connect_to_proxy)
        @param ip_version: Version of the IP address to ping.

        :return: ExecResponse containing data (stdin, stdout, stderr).

        """
        # Setup ping command
        ping_version_cmd = 'ping' if ip_version == 4 else 'ping6'
        ping_cmd = '{ping_version_cmd} -c {count} -v {ip}'.format(
            ip=target_ip, count=count, ping_version_cmd=ping_version_cmd)

        # Build list of potential and expected output
        expectations = OrderedDict([
            (pexpect.TIMEOUT, None),
            (self.LINUX_PROMPT_PATTERN, None)])

        # Initialize output object (same used by remote SSH/ping cmd)
        output = ExecResponse()

        # Open process and start command
        if connection is None:
            connection = pexpect.spawn(ping_cmd)
        else:
            connection.sendline(ping_cmd)

        while True:

            # Watch process output and match on specific criteria
            try:
                response = connection.expect(expectations.keys())

            # TIMEOUT, break out of loop and indicate FAILURE
            except pexpect.TIMEOUT:
                err = 'Pinging target timed out. {0} --> {1}'
                self.logger.error(err.format(
                    connection.before, connection.after))
                output.stdout = connection.before
                break

            # CONNECTION CLOSED, save output and break out of loop.
            except pexpect.EOF:
                self.logger.debug('Reached END OF FILE')
                output.stdout = connection.before
                break

            # If TIMEOUT returned by response, break out of loop and indicate
            # FAILURE...
            if response == 0:
                err = 'Pinging target timed out. {0} --> {1}'
                self.logger.error(err.format(
                    connection.before, connection.after))
                output.stdout = connection.before
                break

            # Capture output from ping.
            output.stdout = connection.before + connection.match.group()
            break

        connection.close()
        return output

    def _validate_ping_response(self, ip, response, threshold=1):
        """
        Validate ping response output.

        :param ip: IP address of target
        :param response: Output of ping cmd (should be a string)
        :param threshold: Number of ping responses required to determine
                  success

        :return: (Boolean) True = PING was successful
                e.g. - received at least one echo reply

        """
        msg = 'PING Response for {ip}:\n{resp}'.format(
                ip=ip, resp=response.stdout)
        self.logger.debug(msg)

        # Check output for number of ping replies received
        pings = re.search(self.PING_PACKET_LOSS_REGEX, response.stdout, re.I)
        target_online = False

        # If there were some number of pings replies received, make sure it is
        # greater than 0 pings.
        if pings is not None:
            pings_received = int(pings.group('received'))
            self.logger.info('Number of pings received: {rec}'.format(
                    rec=pings_received))
            target_online = pings_received >= threshold
        self.logger.info('Target online? {resp}'.format(resp=target_online))
        return target_online
