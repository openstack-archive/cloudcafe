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

import re

from cloudcafe.networking.networks.common.constants import PortTypes
from cloudcafe.networking.networks.common.exceptions \
    import MissingDataException, UnsupportedTypeException


class Connectivity(object):
    """Networking connectivity class verifying ICMP, TCP and UDP
        connectivity across server instances.
    """

    def __init__(self, server_persona_a=None, server_persona_b=None):
        self.server_persona_a = server_persona_a
        self.server_persona_b = server_persona_b
        self.icmp = 'icmp'
        self.tcp = 'tcp'
        self.udp = 'udp'
        self.available_protocols = [self.icmp, self.tcp, self.udp]

    def verify_personas_conn(self, server_persona_a=None,
                             server_persona_b=None, port_type='pnet',
                             protocol='icmp', ip_version=4, count=None,
                             accepted_packet_loss=None, port1=None,
                             port2=None, port_range=None,
                             expected_data=None, dir_path=None,
                             file_name=None):
        """Verify ICMP/TCP/UDP connectivity from server A to server B using
        all of server's B IP addresses based on port_type (public, service,
        isolated) and version (4 or 6).

            Args:
                server_persona_a (instance): server to send packets from,
                    cloudcafe.networking.networks.personas.ServerPersona
                server_persona_b (instance): server to receive (listener),
                    cloudcafe.networking.networks.personas.ServerPersona
                port_type (str): network port type, pnet (public),
                    snet (service) or inet (isolated).
                protocol (str): protocol to check connectivity for ex.
                    icmp, tcp or udp.
                ip_version (int): 4 or 6 for IP address version.
                count (int): used by icmp checks, number of pings, for ex.
                   ping -c count (by default 3)
                accepted_packet_loss (int): used by icmp checks (ping),
                    fail if packet loss greater (default 0).
                port1 (str): open port on listener, used by TCP and/or UDP.
                port2 (str): open port on listener, ONLY used by TCP.
                port_range (str): ports to scan on listener by sender,
                    ONLY used by TCP, for ex. 442-445
                expected_data (list): in TCP, stdout from port scan by sender,
                    for ex.
                        ['442 (tcp) timed out: Operation now in progress',
                         '443 port [tcp/*] succeeded!',
                         '444 port [tcp/*] succeeded!',
                         '445 (tcp) failed: Connection refused']
                    In UDP, file content to transmit, for ex.
                    'Security Groups UDP testing'
                dir_path (str): directory path to save the file to send/receive
                    on the sender and listener. ONLY used by UDP.
                file_name (str): file name to be used for the original and
                    received files on the sender and listener. ONLY used by UDP

            Server personas will require the keypair attribute with a private
            key. And, also the ssh_username attribute, for ex. 'root'

            Returns: list of dicts. There will be one dict per server B IP
            address verified based on port type and IP version, and the dict
            will be the response of the verify_ping, verify_tcp_connectivity
            or verify_udp_connectivity method below.
        """

        if not server_persona_a:
            server_persona_a = self.server_persona_a
        if not server_persona_b:
            server_persona_b = self.server_persona_b

        # Expecting pnet, snet or inet for port type
        expected_types = [PortTypes.PUBLIC, PortTypes.SERVICE,
                          PortTypes.ISOLATED]
        if port_type not in expected_types:
            msg = 'Unexpected port type {0}, expected: {1}'.format(
                port_type, expected_types)
            raise UnsupportedTypeException(msg)

        # Expecting icmp, tcp or udp for protocol
        expected_protocols = self.available_protocols
        if protocol not in expected_protocols:
            msg = 'Unexpected protocol {0}, expected: {1}'.format(
                protocol, expected_protocols)
            raise UnsupportedTypeException(msg)

        # Getting the IP addresses based on port type and IP version
        attr_label = '{0}_fix_ipv{1}'.format(port_type, ip_version)
        ip_addresses = getattr(server_persona_b, attr_label, None)

        if ip_addresses is None:
            msg = ('Missing expected data at server persona\n'
                   'Server Persona: instance of networking.networks.personas\n'
                   'Port Types: {0}\n'
                   'Version: 4 or 6').format(expected_types)
            raise MissingDataException(msg)

        # Defining the remote client sender (FROM) server
        remote_client_a = server_persona_a.remote_client

        # Defining the remote client listener (TO) server
        if protocol == self.tcp or protocol == self.udp:
            remote_client_b = server_persona_b.remote_client
        else:
            remote_client_b = None

        # Defining the method parameters
        kw_args = dict(
            sender_client=remote_client_a, listener_client=remote_client_b,
            port_type=port_type, ip_version=ip_version, count=count,
            accepted_packet_loss=accepted_packet_loss, port1=port1,
            port2=port2, port_range=port_range, expected_data=expected_data,
            dir_path=dir_path, udp_file_name=file_name)

        # Removing params without value
        params = dict((k, v) for k, v in kw_args.iteritems() if v)

        results = []
        for ip_address in ip_addresses:

            params.update(listener_ip=ip_address)
            if protocol == self.icmp:
                result = self.verify_ping(**params)
                results.append(result)
            if protocol == self.tcp:
                result = self.verify_tcp_connectivity(**params)
                results.append(result)
            if protocol == self.udp:
                result = self.verify_udp_connectivity(**params)
                results.append(result)
        return results

    def verify_ping(self, sender_client, listener_ip, ip_version=4,
                    count=3, accepted_packet_loss=0, port_type=None):
        """Verify ICMP connectivity between two servers using the remote client

        Args:
            sender_client (instance): cloudcafe.compute.common.clients.
                remote_instance.linux.linux_client.LinuxClient
            listener_ip (str): IP address to ping
            ip_version (int): version of IP address
            count (int): number of pings, for ex. ping -c count (by default 3)
            accepted_packet_loss (int): fail if packet loss greater (default 0)
            port_type (Optional[str]): network port type, pnet (public),
                snet (service) or inet (isolated).

        Returns:
            dict with the following keys and values:
                to_ip (str): IP address to ping.
                ip_version (int): IP address (to ping) version, 4 or 6.
                sender_hostname (str): sender server hostname.
                sender_public_ip (str): sender server public IP address.
                sender_cmd (str): ping command to execute on the sender.
                sender_cmd_output (instance): sender ping command output.
                    cafe.engine.ssh.models.ssh_response.ExecResponse
                port_type (str): pnet (public), snet (service) or
                    inet (isolated).
                connection (bool): True if packet_loss less than accepted
                    packet loss, False otherwise.
                msg (str): ping message.
                packet_loss (int): packet loss from ping.
                accepted_packet_loss (int): accepted packet loss by user.

        """

        ping_packet_loss_regex = '(\d{1,3})\.?\d*\%.*loss'
        sender_hostname = sender_client.get_hostname()
        sender_public_ip = sender_client.ip_address

        if ip_version == 6:
            ping_cmd = 'ping6 -c {0} {1}'.format(count, listener_ip)
        else:
            ping_cmd = 'ping -c {0} {1}'.format(count, listener_ip)
        resp = sender_client.ssh_client.execute_command(ping_cmd)
        loss_pct_search = re.search(ping_packet_loss_regex, resp.stdout)

        result = dict(ip_version=ip_version, sender_hostname=sender_hostname,
                      port_type=port_type, sender_public_ip=sender_public_ip,
                      to_ip=listener_ip, sender_cmd=ping_cmd,
                      sender_cmd_output=resp)
        if loss_pct_search is None:
            umsg = ('Ping from {0} to {1} got unexpected output:\n{2}'
                    '').format(sender_public_ip, listener_ip, resp)
            result.update(connection=False, msg=umsg)
            return result

        loss_pct = loss_pct_search.group(0)
        index = loss_pct.find('%')
        loss_pct_num = int(loss_pct[:index])
        msg = ('Ping from {0} to {1} packet loss: {2}%. '
               'Accepted packet loss: {3}%').format(
                   sender_public_ip, listener_ip,
                   loss_pct_num, accepted_packet_loss)

        result.update(packet_loss=loss_pct_num,
                      accepted_packet_loss=accepted_packet_loss)

        # Set connection to False if packet loss greater than accepted
        if loss_pct_num > accepted_packet_loss:
            result.update(connection=False, msg=msg)
            return result

        result.update(connection=True, msg=msg)
        return result

    def verify_udp_connectivity(self, listener_client, sender_client,
                                listener_ip, port1='750', expected_data=None,
                                ip_version=4, port_type=None, dir_path='/root',
                                file_name='udp_transfer'):
        """Verify UDP port connectivity between two servers transmitting
        file contents.

        This is done enabling UDP port listening in a server (listener), with
        netcat, to store a file running a command like:
            $nc -ul 750 > received_file

        And sending a file from another server (sender), running
        a command like:
            $nc -unv 10.22.253.5 750 -w 3 < original_file

        Note: received_file and original_file can have the same name.

        Args:
            listener_client (instance): receives UDP packets (a file)
                cloudcafe.compute.common.clients.remote_instance.
                linux.linux_client.LinuxClient
            sender_client (instance): sends UDP packets (a file)
                cloudcafe.compute.common.clients.remote_instance.
                linux.linux_client.LinuxClient
            listener_ip (str): listener IP address to be used by netcat from
                the sender (public, service or isolated network IP)
            port1 (str): open port on listener and to be used by sender.
            expected_data (str): file content to transmit, for ex.
                'Security Groups UDP testing'
            ip_version (int): version of IP address
            port_type (Optional[str]): network port type, pnet (public),
                snet (service) or inet (isolated).
            dir_path (str): directory path to save the file to send/receive
                on the sender and listener.
            file_name (str): file name to be used for the original and
                received files on the sender and listener.

        Returns:
            dict with the following keys and values:
                to_ip (str): IP address for TCP.
                ip_version (int): listener_ip IP version, 4 or 6.
                listener_hostname (str): listener server hostname.
                sender_hostname (str): sender server hostname.
                listener_public_ip (str): listener server public IP address.
                sender_public_ip (str): sender server public IP address.
                listener_cmd (str): netcat command to execute on the listener.
                sender_cmd (str): netcat command to execute on the sender.
                listener_cmd_output (instance): listener netcat command output.
                    cafe.engine.ssh.models.ssh_response.ExecResponse
                sender_cmd_output (instance): sender netcat command output.
                    cafe.engine.ssh.models.ssh_response.ExecResponse
                listener_ok (bool): True for expected listener command output.
                sender_ok (bool): True for expected sender command output.
                port_type (str): pnet (public), snet (service) or
                    inet (isolated).
                connection (bool): status of UDP connection between sender and
                    listener.
                msg (str): error or failure message if needed.
                file_name (str): file name to be used for the original and
                    received files on the sender and listener.
                file_path  (str): directory path with file name of transmitted
                    file. Sent/Received file.
                file_created_at_sender (bool): if the file was successfully
                    created at the sender.
                file_created_at_listener (bool): if the file was successfully
                    created at the listener.
                file_content (str): transfered file content in listener file.
                expected_data (str): file content to send from sender file.

        """

        listener_hostname = listener_client.get_hostname()
        sender_hostname = sender_client.get_hostname()
        listener_public_ip = listener_client.ip_address
        sender_public_ip = sender_client.ip_address

        # Setting the directory path and file name of the file to transfer.
        file_path = '{0}/{1}'.format(dir_path, file_name)

        # Defining the expected data (file content) to transfer via UDP
        if not expected_data:
            expected_data = 'Security Groups UDP testing'

        # Deleting the file (to transfer) if it exists
        if sender_client.is_file_present(file_path=file_path):
            sender_client.delete_file(file_path=file_path)
        if listener_client.is_file_present(file_path=file_path):
            listener_client.delete_file(file_path=file_path)

        # Creating the file to transfer for UDP testing
        sender_client.create_file(file_name=file_name,
                                  file_content=expected_data,
                                  file_path=dir_path)

        file_created_at_sender = sender_client.is_file_present(
            file_path=file_path)

        result = dict(to_ip=listener_ip,
                      ip_version=ip_version,
                      listener_hostname=listener_hostname,
                      sender_hostname=sender_hostname,
                      listener_public_ip=listener_public_ip,
                      sender_public_ip=sender_public_ip,
                      listener_cmd=None,
                      sender_cmd=None,
                      listener_cmd_output=None,
                      sender_cmd_output=None,
                      listener_ok=None,
                      sender_ok=None,
                      port_type=port_type,
                      connection=None,
                      msg=None,
                      file_name=file_name,
                      file_path=file_path,
                      file_created_at_sender=file_created_at_sender,
                      file_created_at_listener=None,
                      file_content=None,
                      expected_data=expected_data)

        if not file_created_at_sender:
            msg = 'Unable to create transfer file at sender server'
            result.update(msg=msg)
            return result

        # Defining netcat options for the listener and sender based on version
        if ip_version == 6:
            listener_opts = '-ul -6'
            sender_opts = '-unv -6'
        else:
            listener_opts = '-ul'
            sender_opts = '-unv'

        listener_cmd = 'nc {opts} {port1} > {file_name}'.format(
            opts=listener_opts, port1=port1, file_name=file_name)
        sender_cmd = ('nc {opts} {ip_address} {port1} -w 3 < '
                      '{file_name}').format(opts=sender_opts,
                                            ip_address=listener_ip,
                                            port1=port1, file_name=file_name)

        # Setting up the listener
        listener_cmd_output = listener_client.ssh_client.execute_shell_command(
            listener_cmd)
        listener_ok = listener_cmd in listener_cmd_output.stdout

        result.update(listener_cmd=listener_cmd,
                      sender_cmd=sender_cmd,
                      listener_cmd_output=listener_cmd_output,
                      listener_ok=listener_ok)

        if not listener_ok:
            msg = 'Unexpected shell command listener output'
            result.update(msg=msg)
            return result

        sender_cmd_output = sender_client.ssh_client.execute_command(
            sender_cmd)
        sender_ok = (listener_ip in sender_cmd_output.stderr and
                     port1 in sender_cmd_output.stderr and
                     'succeeded!' in sender_cmd_output.stderr)
        result.update(sender_cmd_output=sender_cmd_output, sender_ok=sender_ok)

        if not sender_ok:
            msg = 'Unexpected shell command sender output'
            result.update(msg=msg)
            return result

        # Checking the file was created at the listener
        file_created_at_listener = listener_client.is_file_present(
            file_path=file_path)
        result.update(file_created_at_listener=file_created_at_listener)

        if not file_created_at_listener:
            msg = 'Transfer file missing at the listener server'
            result.update(msg=msg)
            return result

        # Getting the file contents in the listener
        transfered_file = listener_client.get_file_details(file_path=file_path)
        file_content = transfered_file.content
        result.update(file_content=file_content)

        if expected_data in file_content:
            result.update(connection=True)
            return result

        result.update(connection=False)
        msg = ('Unexpected transfered file content, expected data '
               'not found in transfered file contents')
        result.update(msg=msg)
        return result

    def verify_tcp_connectivity(self, listener_client, sender_client,
                                listener_ip, port1='443', port2='444',
                                port_range='443-444', expected_data=None,
                                ip_version=4, port_type=None):
        """Verify TCP port connectivity between two servers

        This is done enabling port listening in a server (listener), with
        netcat, running a command like:
            $nc -l 443 & nc -l 444

        And scanning these ports from another server (sender), running
        a command like:
            nc -nvz 10.22.253.15 442-445 -w 2

        Args:
            listener_client (instance): receives TCP packets
                cloudcafe.compute.common.clients.remote_instance.
                linux.linux_client.LinuxClient
            sender_client (instance): sends TCP packets
                cloudcafe.compute.common.clients.remote_instance.
                linux.linux_client.LinuxClient
            listener_ip (str): listener IP address to be used by netcat from
                the sender
            port1 (str): open port on listener
            port2 (str): open port on listener
            port_range (str): ports to scan on listener by sender, for ex.
                442-445
            expected_data (list): stdout from port scan by sender, for ex.
                            ['442 (tcp) timed out: Operation now in progress',
                             '443 port [tcp/*] succeeded!',
                             '444 port [tcp/*] succeeded!',
                             '445 (tcp) failed: Connection refused']
            ip_version (int): version of IP address
            port_type (Optional[str]): network port type, pnet (public),
                snet (service) or inet (isolated).

        Returns:
            dict with the following keys and values:
                to_ip (str): IP address for UDP.
                ip_version (int): listener_ip IP version, 4 or 6.
                listener_hostname (str): listener server hostname.
                sender_hostname (str): sender server hostname.
                listener_public_ip (str): listener server public IP address.
                sender_public_ip (str): sender server public IP address.
                listener_cmd (str): netcat command to execute on the listener.
                sender_cmd (str): netcat command to execute on the sender.
                listener_cmd_output (instance): listener netcat command output.
                    cafe.engine.ssh.models.ssh_response.ExecResponse
                sender_cmd_output (instance): sender netcat command output.
                    cafe.engine.ssh.models.ssh_response.ExecResponse
                listener_ok (bool): True for expected listener command output.
                port_type (str): pnet (public), snet (service) or
                    inet (isolated).
                connection (bool): status of TCP connection between sender and
                    listener.
                msg (str): error or failure message if needed.
                expected_data (list): expected_data given as input.

        """

        listener_hostname = listener_client.get_hostname()
        sender_hostname = sender_client.get_hostname()
        listener_public_ip = listener_client.ip_address
        sender_public_ip = sender_client.ip_address

        # Defining the expected data if not given (TCP port scan output)
        if not expected_data:
            expected_data = ['443 port [tcp/*] succeeded!',
                             '444 port [tcp/*] succeeded!']

        # Defining netcat options for the listener and sender based on version
        if ip_version == 6:
            listener_opts = '-l -6'
            sender_opts = '-nvz -6'
        else:
            listener_opts = '-l'
            sender_opts = '-nvz'

        listener_cmd = 'nc {opts} {port1} & nc {opts} {port2} &'.format(
            opts=listener_opts, port1=port1, port2=port2)
        sender_cmd = 'nc {opts} {ip_address} {port_range} -w 2'.format(
            opts=sender_opts, ip_address=listener_ip, port_range=port_range)

        listener_cmd_output = listener_client.ssh_client.execute_shell_command(
            listener_cmd)
        listener_ok = listener_cmd in listener_cmd_output.stdout

        result = dict(to_ip=listener_ip,
                      ip_version=ip_version,
                      listener_hostname=listener_hostname,
                      sender_hostname=sender_hostname,
                      listener_public_ip=listener_public_ip,
                      sender_public_ip=sender_public_ip,
                      listener_cmd=listener_cmd,
                      sender_cmd=sender_cmd,
                      listener_cmd_output=listener_cmd_output,
                      sender_cmd_output=None,
                      listener_ok=listener_ok,
                      port_type=port_type,
                      connection=None,
                      msg=None,
                      expected_data=expected_data)

        if not listener_ok:
            msg = 'Unexpected shell command listener output'
            result.update(msg=msg)
            return result

        sender_cmd_output = sender_client.ssh_client.execute_command(
            sender_cmd)
        result.update(sender_cmd_output=sender_cmd_output)

        for data in expected_data:
            verify_data = data in sender_cmd_output.stderr
            if not verify_data:
                msg = ('Received unexpected sender_cmd_output compared to '
                       'the expected data')
                result.update(msg=msg)
                result.update(connection=False)
                return result

        result.update(connection=True)
        return result

    def scan_tcp_port(self, sender_client, listener_ip, port1='22',
                      expected_data=None, ip_version=4, port_type=None):
        """Scan a TCP port connectivity between two servers

        Scanning is done from the sender server client to the listener IP,
        running a command like:
            nc -nvz -6 2001:4802:7800:1:be76:4eff:fe20:d235 22 -w 2

        Args:
            sender_client (instance): sends TCP packets
                cloudcafe.compute.common.clients.remote_instance.
                linux.linux_client.LinuxClient
            listener_ip (str): listener IP address to be used by netcat from
                the sender
            port1 (str): port to scan from sender on listener
            expected_data (str): stdout from port scan by sender, for ex.
                '22 port [tcp/*] succeeded!'
                or '450 (tcp) failed: Connection refused'
                or '442 (tcp) timed out: Operation now in progress'
            ip_version (int): version of IP address
            port_type (Optional[str]): network port type, pnet (public),
                snet (service) or inet (isolated).

        Returns:
            dict with the following keys and values:
                to_ip (str): IP address to use to scan.
                ip_version (int): listener_ip IP version, 4 or 6.
                sender_hostname (str): sender server hostname.
                sender_cmd (str): netcat command to execute on the sender.
                sender_cmd_output (instance): sender netcat command output.
                    cafe.engine.ssh.models.ssh_response.ExecResponse
                port_type (str): pnet (public), snet (service) or
                    inet (isolated).
                connection (bool): status of TCP connection between sender and
                    listener.
                msg (str): seuccess, error or failure message if needed.
                expected_data (str): expected_data given as input.
        """

        sender_hostname = sender_client.get_hostname()
        sender_public_ip = sender_client.ip_address

        # Defining the expected data if not given (TCP port scan output)
        if not expected_data:
            expected_data = '22 port [tcp/*] succeeded!'

        # Defining netcat options for the listener and sender based on version
        if ip_version == 6:
            sender_opts = '-nvz -6'
        else:
            sender_opts = '-nvz'

        sender_cmd = 'nc {opts} {ip_address} {port} -w 2'.format(
            opts=sender_opts, ip_address=listener_ip, port=port1)

        result = dict(to_ip=listener_ip,
                      ip_version=ip_version,
                      sender_hostname=sender_hostname,
                      sender_public_ip=sender_public_ip,
                      sender_cmd=sender_cmd,
                      sender_cmd_output=None,
                      port_type=port_type,
                      connection=None,
                      msg=None,
                      expected_data=expected_data)

        sender_cmd_output = sender_client.ssh_client.execute_command(
            sender_cmd)
        result.update(sender_cmd_output=sender_cmd_output)

        verify_data = expected_data in sender_cmd_output.stderr
        if not verify_data:
            msg = ('Received unexpected sender_cmd_output compared to '
                   'the expected data')
            result.update(msg=msg)
            result.update(connection=False)
            return result

        result.update(connection=True)
        return result
