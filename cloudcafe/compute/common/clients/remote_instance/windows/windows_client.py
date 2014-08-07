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

from dateutil.parser import parse
import re

from IPy import IP
from cafe.engine.clients.winrm_client import WinRMClient
from cafe.common.reporting import cclogging
from cafe.engine.clients.remote_instance.models.dir_details \
    import DirectoryDetails
from cafe.engine.clients.remote_instance.models.file_details \
    import FileDetails

from cloudcafe.compute.common.clients.ping import PingClient
from cloudcafe.compute.common.clients.remote_instance.base_client import \
    RemoteInstanceClient
from cloudcafe.compute.common.exceptions import WinRMConnectionException, \
    InvalidAddressFormat


class WindowsClient(RemoteInstanceClient):

    DEFAULT_XEN_CLIENT_PATH = 'C:\\Program Files\\Citrix\\XenTools'

    def __init__(self, ip_address, username='administrator',
                 password=None, key=None, connection_timeout=600,
                 retry_interval=10):
        self.client_log = cclogging.getLogger(
            cclogging.get_object_namespace(self.__class__))

        # Verify the IP address has a valid format
        try:
            IP(ip_address)
        except ValueError:
            raise InvalidAddressFormat(ip_address)

        # Verify the server can be pinged before attempting to connect
        PingClient.ping_until_reachable(ip_address,
                                        timeout=connection_timeout,
                                        interval_time=retry_interval)

        self.ip_address = ip_address
        self.username = username
        self.password = password

        self.client = WinRMClient(
            username=username, password=password, host=ip_address)
        connected = self.client.connect_with_retries()
        if not connected:
            raise WinRMConnectionException(ip_address=ip_address)

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
        command = ('powershell gwmi Win32_ComputerSystem '
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
            'ToDateTime((gwmi Win32_OperatingSystem).'
            'LastBootUpTime)')
        if not output.std_out:
            return None
        output = output.std_out.strip()
        last_boot = parse(output)
        now = self._get_system_current_datetime()
        diff = now - last_boot
        return diff.total_seconds()

    def get_local_users(self):
        """
        Get a list of the local user accounts on the server

        @return: A list of users
        @rtype: List of strings
        """

        command = ('powershell gwmi Win32_UserAccount')
        output = self.client.execute_command(command)
        if not output:
            return None
        raw_output = output.std_out.split('\r\n\r\n')
        raw_users = [user for user in raw_output if user]
        user_list = []
        for user in raw_users:
            user_info = self._convert_powershell_list_to_dict(user)
            user_list.append(user_info.get('Name'))
        return user_list

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

    def get_filesystem_permissions(self, path):
        """
        Returns a list of users with access to a file or directory.

        @param path: Path to the file or directory
        @type path: string
        @return: A list of users
        @rtype: List of strings
        """

        command = (
            'powershell "&{{ (Get-Acl {path}).Access | ForEach-Object '
            '{{$_.IdentityReference.ToString() }} }}"'.format(path=path))
        output = self.client.execute_command(command).std_out
        return output.splitlines() if output else None

    def get_md5sum_for_remote_file(self, file_location, file_name):
        """
        @summary: Gets the md5sum of file on the server
        @param filepath: The path name including file name
        @type filepath: String
        """
        if not file_location.endswith("\\"):
            file_location = file_location + "\\"
        command = (
            'powershell "Get-Content {file_location}{file_name} | '
            'Get-FileHash -Algorithm MD5"'.format(
                file_location=file_location, file_name=file_name))

        response = self.client.execute_command(command)
        if not response.std_out:
            raise Exception("Unable to execute remote file md5 hash")

        stdout = response.std_out.strip()
        lines = stdout.splitlines()
        try:
            data_line = lines[2]
        except:
            raise Exception(
                "Unexpected response format from remote file md5 hash")

        try:
            match = re.match("^MD5\s*(\S*)", data_line)
            groups = match.groups()
            return groups[0]
        except:
            raise Exception(
                "Unable to find md5 hash in remote file md5 hash response")

    def get_file_details(self, file_path):
        """
        Retrieves the contents of a file and its permissions.

        @param file_path: Path to the file
        @type file_path: string
        @return: File details including permissions and content
        @rtype: FileDetails
        """

        file_permissions = self.get_filesystem_permissions(path=file_path)

        file_contents = self.client.execute_command(
            'type {file_path}'.format(file_path=file_path)).std_out
        return FileDetails(
            file_permissions, file_contents.rstrip("\n"), file_path)

    def is_file_present(self, file_path):
        """
        Verifies if the given file is present.

        @param file_path: Path to the file
        @type file_path: string
        @return: True if File exists, False otherwise
        @rtype: bool
        """

        cmd = '(if exist {file_path} (echo True) else (echo False))'.format(
            file_path=file_path)
        output = self.client.execute_command(cmd)
        if not output.std_out:
            return None
        file_exists = output.std_out
        return file_exists.rstrip('\n').strip().lower() == "true"

    def mount_disk(self, source_path, destination_path):
        """
        Mounts a disk to specified destination.

        @param source_path: Path to file source
        @type source_path: string
        @param destination_path: Path to mount destination
        @type destination_path: string
        """

        command = (
            'powershell Set-Partition -DiskNumber '
            '{disk} -PartitionNumber 2 '
            '-NewDriveLetter {drive}').format(disk=source_path,
                                              drive=destination_path)
        output = self.client.execute_command(command)
        return output.std_out

    def unmount_disk(self, disk_path):
        command = (
            'powershell Set-Disk -Number {disk_path} -IsOffline $true'.format(
                disk_path=disk_path))
        return self.client.execute_command(command)

    def get_xen_user_metadata(self, xen_client_path=DEFAULT_XEN_CLIENT_PATH):
        """
        Retrieves the user-metadata section from the XenStore.

        @return: The contents of the user-metadata
        @rtype: dict
        """

        client = '{path}\\xenstore_client.exe'.format(
            path=xen_client_path)

        # Check if there is user metadata set
        command = '"{client}" dir vm-data'.format(client=client)
        output = self.client.execute_command(command)
        if not output.std_out:
            return {}

        # If user-metadata is not one of the directories returned,
        # then there is no metadata
        meta_dirs = output.std_out.splitlines()
        if 'user-metadata' not in meta_dirs:
            return {}

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

    def get_xenstore_disk_config_value(
            self, xen_client_path=DEFAULT_XEN_CLIENT_PATH):
        """
        Returns the XenStore value for disk config.

        @return: Whether the virtual machine uses auto disk config
        @rtype: bool
        """

        client = '{path}\\xenstore_client.exe'.format(
            path=xen_client_path)
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

        command = (
            'powershell New-Item -ItemType directory '
            '-Path {path}'.format(path=path))
        output = self.client.execute_command(command)
        return output.std_out if output.std_out else None

    def is_directory_present(self, directory_path):
        """
        Check if given directory exists.

        @param directory_path: Path to the directory
        @type directory_path: string
        @return: Result of directory check
        @rtype: bool
        """

        command = 'powershell Test-Path {directory_path}'.format(
            directory_path=directory_path)
        output = self.client.execute_command(command)

        if not output:
            return False
        return output.std_out.strip().lower() == 'true'

    def get_directory_details(self, dir_path):
        """
        Retrieves informational data about a directory.

        @param dir_path: Path to the directory
        @type dir_path: string
        @return: Directory details
        @rtype: DirectoryDetails
        """
        permissions = self.get_filesystem_permissions(dir_path)
        size = self._get_directory_size(dir_path)
        return DirectoryDetails(
            name=dir_path, size=size, absolute_permissions=permissions)

    def get_all_disks(self):
        """
        Returns a list of all block devices for a server.

        @return: The accessible block devices
        @rtype: dict
        """
        command = 'powershell "&{ Get-Disk | Format-List }"'
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

    def get_all_disk_details(self):
        """
        Returns all details for all block devices for a server.

        @return: The accessible block devices
        @rtype: dict
        """
        command = 'powershell "&{ Get-Disk | Format-List }"'
        output = self.client.execute_command(command)
        if not output.std_out:
            return None
        raw_output = output.std_out.split('\r\n\r\n')
        raw_disks = [disk for disk in raw_output if disk]

        disks = []
        for disk in raw_disks:
            disk_info = self._convert_powershell_list_to_dict(disk)
            disks.append(disk_info)

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
        command = (
            'powershell Set-Disk -Number {disk} '
            '-IsOffline $false').format(disk=disk)
        self.client.execute_command(command)

        command = (
            'powershell Set-Disk -Number {disk} '
            '-IsReadOnly $false').format(disk=disk)
        self.client.execute_command(command)

        command = (
            'powershell Clear-Disk -Number {disk} '
            '-RemoveData -Confirm:$false').format(disk=disk)
        self.client.execute_command(command)

        command = 'powershell Initialize-Disk -Number {disk}'.format(disk=disk)
        self.client.execute_command(command)

        command = ('powershell "&{{ New-Partition -DiskNumber {disk} '
                   '-UseMaximumSize | Format-Volume -FileSystem {disk_type} '
                   '-Confirm:$false }}').format(disk=disk,
                                                disk_type=filesystem_type)
        output = self.client.execute_command(command)
        return output.std_out

    def get_disk_fstype(self, drive_letter):
        command = (
            'powershell "Get-Volume -DriveLetter {0} | '
            'Select -ExpandProperty FileSystem"'.format(drive_letter))
        output = self.client.execute_command(command)
        return output.std_out

    def generate_mountpoint(self):
        """ Returns the next available drive letter """
        command = (
            'powershell "ls function:[c-z]: -n | ?{!(test-path $_)} '
            '| select -First 1"')

        output = self.client.execute_command(command)
        return output.std_out[0]

    @staticmethod
    def _convert_powershell_list_to_dict(response):
        data = {}
        for line in response.splitlines():
            if line and ':' in line:
                key, value = line.split(':', 1)
                if key is not None:
                    key = key.strip()
                    value = value.strip() if value else None
                    data[key] = value
                else:
                    continue
        return data

    def _get_directory_size(self, path):
        """
        Returns of the size all files under a directory

        @param path: Path to the directory
        @type path: string
        @return: The size of all files in bytes
        @rtype: FileDetails
        """

        command = (
            'powershell "&{{ (Get-ChildItem {path} -recurse | '
            'Measure-Object -property length -sum).Sum }}"').format(path=path)
        output = self.client.execute_command(command)
        if not output.std_out:
            return 0

        size_in_bytes = int(output.std_out)/8.0
        return size_in_bytes

    def _get_system_current_datetime(self):
        """
        Get the current time from the server.

        @return: The current time for the server
        @rtype: DateTime
        """

        command = 'powershell Get-Date'
        output = self.client.execute_command(command)
        if not output.std_out:
            return None
        return parse(output.std_out)
