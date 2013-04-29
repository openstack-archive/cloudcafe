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


class Constants:
    LAST_REBOOT_TIME_FORMAT = '%Y-%m-%d %H:%M'
    LAST_REBOOT_TIME_FORMAT_GENTOO = '%b %d %H:%M %Y'
    LINUX_OS_FAMILY = 'linux'
    PING_IPV4_COMMAND_LINUX = 'ping -c 3 '
    PING_IPV6_COMMAND_LINUX = 'ping6 -c 3 '
    PING_IPV4_COMMAND_WINDOWS = 'ping '
    PING_IPV6_COMMAND_WINDOWS = 'ping6 '
    PING_PACKET_LOSS_REGEX = '(\d{1,3})\.?\d*\%.*loss'
    XML_API_NAMESPACE = 'http://docs.openstack.org/compute/api/v1.1'
    XML_API_DISK_CONFIG_NAMESPACE = 'http://docs.openstack.org/compute/ext/disk_config/api/v1.1'
    XML_API_EXTENDED_STATUS_NAMESPACE = 'http://docs.openstack.org/compute/ext/extended_status/api/v1.1'
    XML_API_ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
    XML_API_RESCUE = 'http://docs.openstack.org/compute/ext/rescue/api/v1.1'
    XML_API_UNRESCUE = 'http://docs.rackspacecloud.com/servers/api/v1.1'
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATETIME_6AM_FORMAT = "%Y-%m-%d 06:00:00"
    DATETIME_0AM_FORMAT = "%Y-%m-%d 00:00:00"
    XML_HEADER = "<?xml version='1.0' encoding='UTF-8'?>"
    SERVICE_TYPE = 'cloudServersOpenStack'


class HTTPResponseCodes(object):
    NOT_FOUND = 404
    SERVER_ERROR = 500
