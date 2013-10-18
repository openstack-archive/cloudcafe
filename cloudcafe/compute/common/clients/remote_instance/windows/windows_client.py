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

import time
from datetime import datetime

from cafe.engine.clients.winrm_client import WinRMClient
from cafe.common.reporting import cclogging
from cafe.engine.clients.remote_instance.models.dir_details \
    import DirectoryDetails
from cafe.engine.clients.remote_instance.models.file_details \
    import FileDetails
from cloudcafe.compute.common.clients.ping import PingClient
from cloudcafe.compute.common.clients.remote_instance.base_client import \
    RemoteInstanceClient
from cloudcafe.compute.common.exceptions import ServerUnreachable


class WindowsClient(RemoteInstanceClient):

    XENSTORE_CLIENT = 'C:\\Program Files\\Citrix\\XenTools'

    def __init__(self, ip_address=None, username='administrator',
                 password=None, key=None, connection_timeout=600,
                 retry_interval=10):
        self.client_log = cclogging.getLogger(
            cclogging.get_object_namespace(self.__class__))

        if ip_address is None:
            raise ServerUnreachable("None")
        self.ip_address = ip_address
        self.username = username
        self.password = password

        # Verify the server can be pinged before attempting to connect
        start = int(time.time())
        reachable = False
        while not reachable:
            reachable = PingClient.ping(ip_address)
            if reachable:
                break
            time.sleep(retry_interval)
            if int(time.time()) - start >= connection_timeout:
                raise ServerUnreachable(ip_address)

        self.client = WinRMClient(username=username, password=password,
                                  host=ip_address)
        self.client.connect_with_retries()

    def can_authenticate(self):
        """
        Verifies that a connection was made to the remote server

        @return: Whether the connection was successful
        @rtype: bool
        """

        return self.client.is_connected()

    def get_hostname(self):
        """
        Gets the host name of the server

        @return: The host name of the server
        @rtype: string
        """

        output = self.client.execute_command('hostname')
        if output.std_out:
            return output.std_out.strip('\r\n').lower()

    def get_allocated_ram(self):
        """
        Returns the amount of RAM the server has

        @return: The RAM size in MB
        @rtype: string
        """

        command = ('powershell gwmi Win32_ComputerSystem '
                   '-Property TotalPhysicalMemory')
        output = self.client.execute_command(command)
        if not output.std_out:
            return None
        system_info = self._convert_powershell_list_to_dict(output.std_out)
        return int(system_info.get('TotalPhysicalMemory', 0))/(1024 * 1024)

    def get_disk_size(self, disk_path):
        """
        Returns the size of a given disk

        @return: The disk size in GB
        @rtype: int
        """

        disks = self.get_all_disks()
        return disks.get(disk_path)

    def get_number_of_cpus(self):
        """
        Return the number of CPUs assigned to the server

        @return: The number of CPUs a server has
        @rtype: int
        """
        command = ('powershell gwmi win32_computersystem '
                   '-Property NumberOfLogicalProcessors')
        output = self.client.execute_command(command)
        if not output.std_out:
            return None
        cpu_info = self._convert_powershell_list_to_dict(output.std_out)
        return int(cpu_info.get('NumberOfLogicalProcessors', 0))

    def get_uptime(self):
        """
        Get the uptime time of the server.

        @return: The uptime of the server in seconds
        @rtype: int
        """
        output = self.client.execute_command(
            'powershell [Management.ManagementDateTimeConverter]::'
            'ToDateTime((Get-WmiObject Win32_OperatingSystem).'
            'LastBootUpTime)')
        if not output.std_out:
            return None
        output = output.std_out.strip()
        last_boot = datetime.strptime(output, '%A, %B %d, %Y %H:%M:%S  %p')
        now = datetime.now()
        diff = now - last_boot
        return diff.seconds

    def create_file(self, file_name, file_content, file_path):
        """
        Creates a new file with the provided content.

        @param file_name: File name
        @type file_name: string
        @param file_content: File content
        @type file_content: String
        @rtype: FileDetails
        """
        self.client.execute_command(
            'echo {file_content} >> {file_path}\\{file_name}'.format(
                file_content=file_content, file_path=file_path,
                file_name=file_name))
        return FileDetails(None, file_content, file_path)

    def get_file_details(self, file_path):
        """
        Retrieves the contents of a file and its permissions.

        @param file_path: Path to the file
        @type file_path: string
        @return: File details including permissions and content
        @rtype: FileDetails
        """

        file_permissions = self.client.execute_command(
            'cacls {file_path}'.format(file_path=file_path)).std_out
        file_contents = self.client.execute_command(
            'type {file_path}'.format(file_path=file_path)).std_out
        return FileDetails(file_permissions.rstrip("\n"),
                           file_contents.rstrip("\n"), file_path)

    def is_file_present(self, file_path):
        """
        Verifies if the given file is present.

        @param file_path: Path to the file
        @type file_path: string
        @return: True if File exists, False otherwise
        @rtype: bool
        """

        command = '(if exist ' + file_path + ' (echo True) else (echo False))'
        output = self.client.execute_command(command)
        if not output.std_out:
            return None
        file_exists = output.std_out
        return file_exists.rstrip('\n') == "True"

    def mount_disk(self, source_path, destination_path):
        """
        Mounts a disk to specified destination.

        @param source_path: Path to file source
        @type source_path: string
        @param destination_path: Path to mount destination
        @type destination_path: string
        """

        raise NotImplementedError

    def get_xen_user_metadata(self):
        """
        Retrieves the user-metadata section from the XenStore.

        @return: The contents of the user-metadata
        @rtype: dict
        """

        client = '{path}\\xenstore_client.exe'.format(
            path=self.XENSTORE_CLIENT)
        command = '"{client}" dir vm-data/user-metadata'.format(client=client)
        output = self.client.execute_command(command)
        if output.std_out:
            keys = output.std_out.splitlines()
            metadata = {}
            for key in keys:
                cmd = '"{client}" read vm-data/user-metadata/{key}'.format(
                    client=client, key=key)
                output = self.client.execute_command(cmd)
                if output.std_out:
                    metadata[key] = output.std_out.replace('"', '')
            return metadata
        return {}

    def get_xenstore_disk_config_value(self):
        """
        Returns the XenStore value for disk config.

        @return: Whether the virtual machine uses auto disk config
        @rtype: bool
        """

        client = '{path}\\xenstore_client.exe'.format(
            path=self.XENSTORE_CLIENT)
        command = '"{client}" read vm-data/auto-disk-config'.format(
            client=client)

        output = self.client.execute_command(command)
        if output.std_out:
            return output.std_out.lower() == 'true'

    def create_directory(self, path):
        """
        Creates a directory at the specified path.

        @param path: Directory path
        @type path: string
        """

        raise NotImplementedError

    def is_directory_present(self, directory_path):
        """
        Check if given directory exists.

        @param directory_path: Path to the directory
        @type directory_path: string
        @return: Result of directory check
        @rtype: bool
        """

        raise NotImplementedError

    def get_directory_details(self, dir_path):
        """
        Retrieves informational data about a directory.

        @param dir_path: Path to the directory
        @type dir_path: string
        @return: Directory details
        @rtype: DirectoryDetails
        """

        raise NotImplementedError

    def get_all_disks(self):
        """
        Returns a list of all block devices for a server.

        @return: The accessible block devices
        @rtype: dict
        """
        command = 'powershell "&{ Get-Disk |  Format-List }'
        output = self.client.execute_command(command)
        if not output.std_out:
            return None
        raw_output = output.std_out.split('\r\n\r\n')
        raw_disks = [disk for disk in raw_output if disk]

        disks = {}
        for disk in raw_disks:
            disk_info = self._convert_powershell_list_to_dict(disk)
            disks[disk_info['Number']] = int(disk_info['Size'].split()[0])
        return disks

    def format_disk(self, disk, filesystem_type):
        """
        Formats a disk to the provided filesystem type.

        @param disk: The path to the disk to be formatted
        @type disk: string
        @param filesystem_type: The filesystem type to format the disk to
        @type filesystem_type: string

        @return: Output of command execution
        @rtype: string
        """

        raise NotImplementedError

    def _convert_powershell_list_to_dict(self, response):
        data = {}
        for line in response.splitlines():
            if line and ':' in line:
                key, value = line.split(':')
                if key is not None:
                    key = key.strip()
                    value = value.strip() if value else None
                    data[key] = value
                else:
                    continue
        return data
