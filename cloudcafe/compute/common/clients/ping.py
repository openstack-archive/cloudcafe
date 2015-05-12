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

import platform
import re
import time

from IPy import IP
from cafe.common.reporting import cclogging
from cafe.engine.clients.commandline import BaseCommandLineClient
from cloudcafe.compute.common.exceptions import TimeoutException


class PingClient(object):

    _log = cclogging.getLogger(__name__)

    #def __init__(self):
    #    super(PingClient, self).__init__()

    PING_IPV4_COMMAND_LINUX = 'ping -c 3'
    PING_IPV6_COMMAND_LINUX = 'ping6 -c 3'
    PING_IPV4_COMMAND_WINDOWS = 'ping'
    PING_IPV6_COMMAND_WINDOWS = 'ping -6'
    PING_PACKET_LOSS_REGEX = '(\d{1,3})\.?\d*\%.*loss'

    @classmethod
    def ping(cls, ip):
        """
        @summary: Ping a server with a IP
        @param ip: IP address to ping
        @type ip: string
        @return: True if the server was reachable, False otherwise
        @rtype: bool
        """
        address = IP(ip)
        ip_address_version = address.version()
        os_type = platform.system().lower()
        ping_ipv4 = (cls.PING_IPV4_COMMAND_WINDOWS if os_type == 'windows'
                     else cls.PING_IPV4_COMMAND_LINUX)
        ping_ipv6 = (cls.PING_IPV6_COMMAND_WINDOWS if os_type == 'windows'
                     else cls.PING_IPV6_COMMAND_LINUX)
        ping_command = ping_ipv6 if ip_address_version == 6 else ping_ipv4
        command = '{command} {address}'.format(
            command=ping_command, address=ip)
        cls._log.debug("Executing command '{command}'".format(command=command))
        cmd_client = BaseCommandLineClient()
        results = cmd_client.run_command(command)
        result = " ".join(results.standard_out)
        try:
            packet_loss_percent = re.search(
                cls.PING_PACKET_LOSS_REGEX,
                result).group(1)
        except Exception:
            cls._log.debug("Unable to ping {ip}.".format(ip=ip))
            return False
        cls._log.debug("Pinged {ip} with {packet_loss}% packet loss.".format(
            ip=ip, packet_loss=packet_loss_percent))
        return packet_loss_percent != '100'

    @classmethod
    def ping_until_reachable(cls, ip, timeout, interval_time):
        """
        @summary: Ping an IP address until it responds or a timeout
                  is reached
        @param ip: The IP address to ping (either IPv4 or IPv6)
        @type ip: string
        @param timeout: The amount of time in seconds to wait before aborting.
        @type timeout: int
        @param interval_time: The length of time in seconds to wait between
                              pings.
        @type interval_time: int

        """

        end_time = time.time() + timeout

        while time.time() < end_time:
            if PingClient.ping(ip):
                return

            time.sleep(interval_time)

        raise TimeoutException(
            "ping_until_reachable ran for {timeout} seconds and did not "
            "receive a ping response from {ip}"
            .format(timeout=timeout, ip=ip))

    @classmethod
    def ping_until_unreachable(cls, ip, timeout, interval_time):
        """
        @summary: Ping an IP address until it stops responding or a
                  timeout is reached
        @param ip: The IP address to ping (either IPv4 or IPv6)
        @type ip: string
        @param timeout: The amount of time in seconds to wait before aborting.
        @type timeout: int
        @param interval_time: The length of time in seconds to wait between
                              pings.
        @type interval_time: int

        """

        end_time = time.time() + timeout

        while time.time() < end_time:
            if not PingClient.ping(ip):
                return

            time.sleep(interval_time)

        raise TimeoutException(
            "{ip} was expected to become unreachable, but was still pingable "
            "after {timeout} seconds"
            .format(timeout=timeout, ip=ip))
